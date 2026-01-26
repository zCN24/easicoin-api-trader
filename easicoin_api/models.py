"""
Easicoin API 响应数据模型

使用dataclass定义API响应的数据结构，可选支持Pydantic。
"""

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Union
from datetime import datetime


@dataclass
class Instrument:
    """交易对信息"""

    symbol: str  # 交易对符号 (BTCUSDT)
    base_currency: str  # 基础货币 (BTC)
    quote_currency: str  # 报价货币 (USDT)
    price_precision: int  # 价格精度
    quantity_precision: int  # 数量精度
    min_price: float  # 最小价格
    max_price: float  # 最大价格
    min_quantity: float  # 最小数量
    max_quantity: float  # 最大数量
    taker_fee: float  # Taker费率
    maker_fee: float  # Maker费率
    leverage: int = 1  # 最大杠杆
    is_perpetual: bool = True  # 是否永续合约
    status: str = "active"  # 交易对状态


@dataclass
class Ticker:
    """行情数据"""

    symbol: str  # 交易对
    last_price: float  # 最新价格
    bid_price: float  # 买一价
    ask_price: float  # 卖一价
    high_price: Optional[float] = None  # 24h最高价
    low_price: Optional[float] = None  # 24h最低价
    open_price: Optional[float] = None  # 24h开盘价
    volume: Optional[float] = None  # 24h成交量 (基础货币)
    quote_volume: Optional[float] = None  # 24h成交额 (报价货币)
    timestamp: Optional[int] = None  # 服务器时间戳 (ms)


@dataclass
class OrderBook:
    """深度数据"""

    symbol: str  # 交易对
    bids: List[List[float]] = field(default_factory=list)  # 买单 [[价格, 数量], ...]
    asks: List[List[float]] = field(default_factory=list)  # 卖单 [[价格, 数量], ...]
    timestamp: Optional[int] = None  # 服务器时间戳 (ms)


@dataclass
class Kline:
    """K线数据"""

    timestamp: int  # K线开始时间 (ms)
    open: float  # 开盘价
    high: float  # 最高价
    low: float  # 最低价
    close: float  # 收盘价
    volume: float  # 成交量 (基础货币)
    quote_volume: float  # 成交额 (报价货币)


@dataclass
class Trade:
    """成交数据"""

    trade_id: str  # 交易ID
    symbol: str  # 交易对
    price: float  # 成交价
    quantity: float  # 成交量
    buyer_id: Optional[str] = None  # 买方ID
    seller_id: Optional[str] = None  # 卖方ID
    is_buyer_maker: bool = False  # 买方是否为主动方
    timestamp: Optional[int] = None  # 成交时间 (ms)


@dataclass
class FundingRate:
    """资金费率数据"""

    symbol: str  # 交易对
    funding_rate: float  # 资金费率
    funding_timestamp: int  # 资金费时间 (ms)
    next_funding_rate: Optional[float] = None  # 下一个资金费率
    next_funding_timestamp: Optional[int] = None  # 下一个资金费时间 (ms)


@dataclass
class Order:
    """订单数据"""

    order_id: str  # 订单ID
    symbol: str  # 交易对
    order_type: str  # 订单类型 (market/limit)
    side: str  # 订单方向 (buy/sell)
    price: float  # 订单价格
    quantity: float  # 订单数量
    filled_quantity: float  # 已成交数量
    status: str  # 订单状态
    created_at: Optional[int] = None  # 创建时间 (ms)
    updated_at: Optional[int] = None  # 更新时间 (ms)
    fee: Optional[float] = None  # 手续费
    time_in_force: Optional[str] = None  # 有效期
    reduce_only: bool = False  # 仅平仓
    post_only: bool = False  # 仅提交


@dataclass
class Position:
    """仓位数据"""

    symbol: str  # 交易对
    side: str  # 仓位方向 (long/short)
    quantity: float  # 持仓数量
    entry_price: float  # 开仓平均价格
    current_price: float  # 当前价格
    mark_price: Optional[float] = None  # 标记价格
    leverage: int = 1  # 杠杆
    margin: float = 0  # 保证金
    margin_mode: str = "isolated"  # 保证金模式
    liquidation_price: Optional[float] = None  # 清算价格
    unrealised_pnl: Optional[float] = None  # 未实现盈亏
    realised_pnl: Optional[float] = None  # 已实现盈亏
    roi: Optional[float] = None  # ROI


@dataclass
class Wallet:
    """账户余额数据"""

    currency: str  # 货币
    free: float  # 可用余额
    locked: float  # 冻结余额

    @property
    def total(self) -> float:
        """总余额"""
        return self.free + self.locked


@dataclass
class FeeRate:
    """费率数据"""

    symbol: Optional[str] = None  # 交易对，None表示全局费率
    maker_fee: float = 0.0  # Maker费率
    taker_fee: float = 0.0  # Taker费率


@dataclass
class WebSocketMessage:
    """WebSocket消息"""

    type: str  # 消息类型 (auth, subscribe, unsubscribe, data, etc.)
    data: Dict[str, Any] = field(default_factory=dict)  # 消息数据
    channel: Optional[str] = None  # 频道名称
    symbol: Optional[str] = None  # 交易对
    timestamp: Optional[int] = None  # 时间戳


def dict_to_dataclass(cls, data: Dict[str, Any]):
    """
    将字典转换为dataclass实例

    Args:
        cls: dataclass类
        data: 字典数据

    Returns:
        dataclass实例
    """
    if not isinstance(data, dict):
        return data

    # 获取dataclass字段
    field_names = {f.name for f in cls.__dataclass_fields__.values()}

    # 过滤出有效字段
    kwargs = {k: v for k, v in data.items() if k in field_names}

    return cls(**kwargs)


def dataclass_to_dict(obj) -> Dict[str, Any]:
    """
    将dataclass实例转换为字典

    Args:
        obj: dataclass实例

    Returns:
        字典
    """
    if hasattr(obj, "__dataclass_fields__"):
        return asdict(obj)
    return obj


# 响应包装器
@dataclass
class APIResponse:
    """API通用响应包装"""

    code: int  # 状态码
    msg: str  # 消息
    data: Any = None  # 数据


@dataclass
class PaginatedResponse:
    """分页响应"""

    data: List[Any] = field(default_factory=list)  # 数据列表
    page: int = 1  # 当前页
    limit: int = 10  # 每页数量
    total: int = 0  # 总数


# 便利函数
def create_wallet_from_response(currency: str, response: Dict[str, Any]) -> Wallet:
    """从API响应创建Wallet对象"""
    return Wallet(
        currency=currency,
        free=float(response.get("free", 0)),
        locked=float(response.get("locked", 0)),
    )


def create_order_from_response(response: Dict[str, Any]) -> Order:
    """从API响应创建Order对象"""
    return Order(
        order_id=response.get("order_id"),
        symbol=response.get("symbol"),
        order_type=response.get("order_type"),
        side=response.get("side"),
        price=float(response.get("price", 0)),
        quantity=float(response.get("quantity", 0)),
        filled_quantity=float(response.get("filled_quantity", 0)),
        status=response.get("status"),
        created_at=response.get("created_at"),
        updated_at=response.get("updated_at"),
        fee=float(response.get("fee")) if response.get("fee") else None,
        time_in_force=response.get("time_in_force"),
        reduce_only=response.get("reduce_only", False),
        post_only=response.get("post_only", False),
    )


def create_position_from_response(response: Dict[str, Any]) -> Position:
    """从API响应创建Position对象"""
    return Position(
        symbol=response.get("symbol"),
        side=response.get("side"),
        quantity=float(response.get("quantity", 0)),
        entry_price=float(response.get("entry_price", 0)),
        current_price=float(response.get("current_price", 0)),
        mark_price=float(response.get("mark_price")) if response.get("mark_price") else None,
        leverage=int(response.get("leverage", 1)),
        margin=float(response.get("margin", 0)),
        margin_mode=response.get("margin_mode", "isolated"),
        liquidation_price=float(response.get("liquidation_price"))
        if response.get("liquidation_price")
        else None,
        unrealised_pnl=float(response.get("unrealised_pnl"))
        if response.get("unrealised_pnl")
        else None,
        realised_pnl=float(response.get("realised_pnl"))
        if response.get("realised_pnl")
        else None,
        roi=float(response.get("roi")) if response.get("roi") else None,
    )
