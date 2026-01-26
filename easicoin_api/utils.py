"""
Easicoin API 工具函数模块

包含时间戳、参数处理、限流等工具函数。
"""

import time
import logging
from datetime import datetime
from typing import Any, Dict, Optional
from threading import Lock

logger = logging.getLogger(__name__)


class RateLimiter:
    """简单的请求限流器 (令牌桶算法)"""

    def __init__(self, rate: float = 10, period: float = 1.0):
        """
        初始化限流器

        Args:
            rate: 单位时间内允许的最大请求数
            period: 时间周期（秒）
        """
        self.rate = rate  # 请求数
        self.period = period  # 秒
        self.tokens = rate  # 当前可用令牌数
        self.last_update = time.time()
        self.lock = Lock()

    def acquire(self, tokens: int = 1) -> float:
        """
        获取令牌，必要时阻塞

        Args:
            tokens: 需要的令牌数

        Returns:
            等待时间（秒）
        """
        with self.lock:
            now = time.time()
            elapsed = now - self.last_update

            # 补充令牌
            self.tokens = min(self.rate, self.tokens + elapsed * self.rate / self.period)
            self.last_update = now

            if self.tokens >= tokens:
                self.tokens -= tokens
                return 0.0
            else:
                # 需要等待的时间
                wait_time = (tokens - self.tokens) * self.period / self.rate
                self.tokens = 0
                return wait_time

    def wait(self, tokens: int = 1) -> None:
        """
        获取令牌，必要时阻塞

        Args:
            tokens: 需要的令牌数
        """
        wait_time = self.acquire(tokens)
        if wait_time > 0:
            logger.debug(f"Rate limit: waiting {wait_time:.2f}s")
            time.sleep(wait_time)


def get_timestamp_ms() -> int:
    """
    获取当前UTC时间戳（毫秒）

    Returns:
        UTC时间戳（毫秒）
    """
    return int(time.time() * 1000)


def get_timestamp_us() -> int:
    """
    获取当前UTC时间戳（微秒）

    Returns:
        UTC时间戳（微秒）
    """
    return int(time.time() * 1_000_000)


def timestamp_to_datetime(timestamp_ms: int) -> datetime:
    """
    将毫秒时间戳转换为datetime对象

    Args:
        timestamp_ms: 毫秒时间戳

    Returns:
        datetime 对象
    """
    return datetime.utcfromtimestamp(timestamp_ms / 1000)


def clean_dict(data: Dict[str, Any], remove_none: bool = True) -> Dict[str, Any]:
    """
    清理字典，移除None值和空字符串

    Args:
        data: 输入字典
        remove_none: 是否移除None值

    Returns:
        清理后的字典
    """
    if remove_none:
        return {k: v for k, v in data.items() if v is not None and v != ""}
    return {k: v for k, v in data.items() if v != ""}


def build_query_string(params: Optional[Dict[str, Any]]) -> str:
    """
    构建查询字符串

    Args:
        params: 参数字典

    Returns:
        查询字符串 (不含前缀 ?)
    """
    if not params:
        return ""

    # 排序参数以确保一致性
    sorted_params = sorted(params.items())
    query_parts = []

    for key, value in sorted_params:
        if value is not None:
            query_parts.append(f"{key}={value}")

    return "&".join(query_parts)


def format_number(value: Any, decimal_places: Optional[int] = None) -> str:
    """
    格式化数字为字符串

    Args:
        value: 数值
        decimal_places: 小数位数，None表示不限制

    Returns:
        格式化后的字符串
    """
    if isinstance(value, (int, float)):
        if decimal_places is not None:
            return f"{value:.{decimal_places}f}"
        else:
            return str(value)
    return str(value)


def is_valid_symbol(symbol: str) -> bool:
    """
    检验交易对符号格式

    Args:
        symbol: 交易对 (如 BTCUSDT)

    Returns:
        是否有效
    """
    if not isinstance(symbol, str) or len(symbol) < 3:
        return False
    # 基础验证：字母和数字组成，至少包含一个币种和一个计价货币
    return symbol.isupper() and symbol.isalnum()


def is_valid_order_quantity(quantity: float, min_qty: Optional[float] = None) -> bool:
    """
    检验订单数量有效性

    Args:
        quantity: 数量
        min_qty: 最小数量

    Returns:
        是否有效
    """
    if quantity <= 0:
        return False
    if min_qty is not None and quantity < min_qty:
        return False
    return True


def is_valid_price(price: float, min_price: Optional[float] = None) -> bool:
    """
    检验价格有效性

    Args:
        price: 价格
        min_price: 最小价格

    Returns:
        是否有效
    """
    if price <= 0:
        return False
    if min_price is not None and price < min_price:
        return False
    return True


def merge_dicts(*dicts) -> Dict[str, Any]:
    """
    合并多个字典

    Args:
        *dicts: 多个字典

    Returns:
        合并后的字典
    """
    result = {}
    for d in dicts:
        if d:
            result.update(d)
    return result


def safe_get(data: Dict, key: str, default: Any = None) -> Any:
    """
    安全地从字典中获取值

    Args:
        data: 字典
        key: 键，支持点号分隔 (如 'user.name')
        default: 默认值

    Returns:
        值或默认值
    """
    if not data:
        return default

    keys = key.split(".")
    value = data

    for k in keys:
        if isinstance(value, dict):
            value = value.get(k)
        else:
            return default

        if value is None:
            return default

    return value if value is not None else default


def setup_logging(level: int = logging.INFO, log_file: Optional[str] = None) -> None:
    """
    设置日志配置

    Args:
        level: 日志级别
        log_file: 日志文件路径，None表示仅输出到控制台
    """
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(console_handler)

    # 文件处理器
    if log_file:
        try:
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
        except Exception as e:
            logger.error(f"Failed to create log file: {e}")
