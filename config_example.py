"""
Easicoin API 配置示例

复制此文件为 config.py 并填入你的实际API密钥
"""

# =======================================
# API 密钥配置
# =======================================

# 从 https://www.easicoin.io 获取你的API密钥
API_KEY = "your_api_key_here"
API_SECRET = "your_api_secret_here"

# =======================================
# 连接参数
# =======================================

# 接收窗口（毫秒），默认5000
RECV_WINDOW = 5000

# 请求超时（秒），默认30
TIMEOUT = 30

# 每秒最大请求数，默认10
RATE_LIMIT = 10

# =======================================
# WebSocket 参数
# =======================================

# 心跳间隔（秒），默认30
WS_PING_INTERVAL = 30

# 心跳超时（秒），默认10
WS_PING_TIMEOUT = 10

# 最大重连次数，默认5
WS_MAX_RECONNECT_ATTEMPTS = 5

# 重连延迟（秒），默认1.0
WS_RECONNECT_DELAY = 1.0

# =======================================
# 日志配置
# =======================================

import logging

# 日志级别：DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL = logging.INFO

# 日志文件路径（None表示不记录到文件，仅输出到控制台）
LOG_FILE = "easicoin_api.log"

# =======================================
# 交易参数（默认值）
# =======================================

# 默认杠杆
DEFAULT_LEVERAGE = 1

# 默认保证金模式：isolated（逐仓）或 cross（全仓）
DEFAULT_MARGIN_MODE = "isolated"

# 默认时间在力：GTC, IOC, FOK, post_only
DEFAULT_TIME_IN_FORCE = "GTC"

# =======================================
# 监控和告警参数
# =======================================

# 仓位盈亏告警阈值（美元）
POSITION_PNL_ALERT_THRESHOLD = -500  # 亏损超过500美元时告警

# 最大持仓数量告警
MAX_OPEN_POSITIONS_ALERT = 10

# WebSocket 断连告警延迟（秒）
WS_DISCONNECT_ALERT_DELAY = 60

# =======================================
# 使用示例
# =======================================

if __name__ == "__main__":
    from easicoin_api import EasicoinAPI, setup_logging
    
    # 配置日志
    setup_logging(level=LOG_LEVEL, log_file=LOG_FILE)
    
    # 初始化客户端
    client = EasicoinAPI(
        api_key=API_KEY,
        api_secret=API_SECRET,
        recv_window=RECV_WINDOW,
        timeout=TIMEOUT,
        rate_limit=RATE_LIMIT,
    )
    
    try:
        # 获取余额
        wallets = client.get_wallet()
        print("账户余额:")
        for currency, wallet in wallets.items():
            if wallet.total > 0:
                print(f"  {currency}: {wallet.total}")
    except Exception as e:
        print(f"错误: {e}")
    finally:
        client.close()
