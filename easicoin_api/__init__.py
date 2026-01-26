"""
Easicoin API Python客户端库

一个完整的、生产级别的Python API客户端，用于Easicoin交易所的期货交易。
支持REST API和WebSocket实时数据流。

基本使用:
    from easicoin_api import EasicoinAPI
    
    # 初始化客户端
    client = EasicoinAPI(api_key="your_key", api_secret="your_secret")
    
    # REST API示例
    instruments = client.get_instruments()
    ticker = client.get_ticker("BTCUSDT")
    
    # 订单示例
    order = client.buy_limit("BTCUSDT", quantity=0.1, price=30000)
    
    # WebSocket示例
    client.ws_connect_public()
    client.ws_subscribe_ticker(["BTCUSDT"], callback=lambda msg: print(msg))

文档: https://docs.easicoin.io
"""

__version__ = "1.0.0"
__author__ = "Easicoin Developer"

# 主客户端
from .client import EasicoinAPI

# 数据模型
from .models import (
    Instrument,
    Ticker,
    OrderBook,
    Kline,
    Trade,
    FundingRate,
    Order,
    Position,
    Wallet,
    FeeRate,
    WebSocketMessage,
)

# 枚举类型
from .enums import (
    OrderSide,
    OrderType,
    OrderStatus,
    PositionSide,
    MarginMode,
    KlineInterval,
    TimeInForce,
    WebSocketChannel,
)

# 异常类
from .errors import (
    EasicoinException,
    APIError,
    AuthenticationError,
    AuthorizationError,
    RateLimitError,
    BadRequestError,
    NotFoundError,
    ServerError,
    ServiceUnavailableError,
    NetworkError,
    TimeoutError,
    InvalidSignatureError,
    InvalidParameterError,
    WebSocketError,
    WebSocketAuthenticationError,
)

# 认证和工具
from .auth import Signature, AuthManager
from .rest import RESTClient
from .websocket import WebSocketClient, AsyncMessageHandler
from .utils import (
    RateLimiter,
    get_timestamp_ms,
    get_timestamp_us,
    setup_logging,
    clean_dict,
    build_query_string,
)

__all__ = [
    # Main client
    "EasicoinAPI",
    # Models
    "Instrument",
    "Ticker",
    "OrderBook",
    "Kline",
    "Trade",
    "FundingRate",
    "Order",
    "Position",
    "Wallet",
    "FeeRate",
    "WebSocketMessage",
    # Enums
    "OrderSide",
    "OrderType",
    "OrderStatus",
    "PositionSide",
    "MarginMode",
    "KlineInterval",
    "TimeInForce",
    "WebSocketChannel",
    # Exceptions
    "EasicoinException",
    "APIError",
    "AuthenticationError",
    "AuthorizationError",
    "RateLimitError",
    "BadRequestError",
    "NotFoundError",
    "ServerError",
    "ServiceUnavailableError",
    "NetworkError",
    "TimeoutError",
    "InvalidSignatureError",
    "InvalidParameterError",
    "WebSocketError",
    "WebSocketAuthenticationError",
    # Auth and utilities
    "Signature",
    "AuthManager",
    "RESTClient",
    "WebSocketClient",
    "AsyncMessageHandler",
    "RateLimiter",
    "get_timestamp_ms",
    "get_timestamp_us",
    "setup_logging",
    "clean_dict",
    "build_query_string",
]
