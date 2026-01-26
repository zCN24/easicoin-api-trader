"""
Easicoin API 主客户端类

集成REST和WebSocket接口，提供统一的API访问入口。
"""

import logging
from typing import Optional, Dict, Any, List, Callable

from .rest import RESTClient
from .websocket import WebSocketClient, AsyncMessageHandler
from .auth import AuthManager
from .models import (
    Instrument,
    Ticker,
    OrderBook,
    Kline,
    FundingRate,
    Order,
    Position,
    Wallet,
    FeeRate,
)
from .enums import OrderSide, OrderType, KlineInterval
from .utils import setup_logging

logger = logging.getLogger(__name__)


class EasicoinAPI:
    """
    Easicoin API 主客户端

    统一管理REST API和WebSocket连接，提供完整的API访问功能。
    """

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        recv_window: int = 5000,
        timeout: int = 30,
        rate_limit: float = 10,
        enable_logging: bool = True,
        log_level: int = logging.INFO,
    ):
        """
        初始化Easicoin API客户端

        Args:
            api_key: API密钥
            api_secret: API密钥对应的secret
            recv_window: 接收窗口（毫秒），默认5000
            timeout: 请求超时时间（秒），默认30
            rate_limit: 每秒最大请求数，默认10
            enable_logging: 是否启用日志，默认True
            log_level: 日志级别，默认INFO
        """
        self.api_key = api_key
        self.api_secret = api_secret

        # 启用日志
        if enable_logging:
            setup_logging(level=log_level)

        # 初始化REST客户端
        self.rest_client = RESTClient(
            api_key=api_key,
            api_secret=api_secret,
            recv_window=recv_window,
            timeout=timeout,
            rate_limit=rate_limit,
        )

        # 初始化WebSocket客户端
        self.ws_public = WebSocketClient(is_private=False)
        self.ws_private = WebSocketClient(
            api_key=api_key, api_secret=api_secret, is_private=True
        )

        # 消息处理器
        self.message_handler = None

        logger.info("Easicoin API client initialized")

    # ==================== 公共市场数据接口 ====================

    def get_instruments(self) -> List[Instrument]:
        """获取所有交易对信息"""
        return self.rest_client.get_instruments()

    def get_ticker(self, symbol: str) -> Ticker:
        """获取行情数据"""
        return self.rest_client.get_ticker(symbol)

    def get_orderbook(self, symbol: str, limit: int = 20) -> OrderBook:
        """获取深度数据"""
        return self.rest_client.get_orderbook(symbol, limit)

    def get_klines(
        self,
        symbol: str,
        interval: str,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: int = 500,
    ) -> List[Kline]:
        """获取K线数据"""
        return self.rest_client.get_klines(symbol, interval, start_time, end_time, limit)

    def get_mark_price_klines(
        self,
        symbol: str,
        interval: str,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: int = 500,
    ) -> List[Kline]:
        """获取标记价格K线"""
        return self.rest_client.get_mark_price_klines(
            symbol, interval, start_time, end_time, limit
        )

    def get_funding_rate_history(
        self,
        symbol: str,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: int = 100,
    ) -> List[FundingRate]:
        """获取资金费率历史"""
        return self.rest_client.get_funding_rate_history(symbol, start_time, end_time, limit)

    # ==================== 账户和订单接口 ====================

    def get_wallet(self) -> Dict[str, Wallet]:
        """获取账户余额"""
        return self.rest_client.get_wallet()

    def get_fee_rate(self, symbol: Optional[str] = None) -> FeeRate:
        """获取费率信息"""
        return self.rest_client.get_fee_rate(symbol)

    def create_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None,
        time_in_force: Optional[str] = None,
        reduce_only: bool = False,
        post_only: bool = False,
        client_id: Optional[str] = None,
    ) -> Order:
        """创建订单"""
        return self.rest_client.create_order(
            symbol,
            side,
            order_type,
            quantity,
            price,
            time_in_force,
            reduce_only,
            post_only,
            client_id,
        )

    def replace_order(
        self,
        order_id: str,
        quantity: Optional[float] = None,
        price: Optional[float] = None,
    ) -> Order:
        """改单"""
        return self.rest_client.replace_order(order_id, quantity, price)

    def cancel_order(self, order_id: str) -> Order:
        """取消订单"""
        return self.rest_client.cancel_order(order_id)

    def cancel_all_orders(self, symbol: Optional[str] = None) -> List[Order]:
        """批量取消订单"""
        return self.rest_client.cancel_all_orders(symbol)

    def get_open_orders(self, symbol: Optional[str] = None) -> List[Order]:
        """获取活跃订单"""
        return self.rest_client.get_open_orders(symbol)

    def get_order_history(
        self,
        symbol: Optional[str] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: int = 100,
    ) -> List[Order]:
        """获取历史订单"""
        return self.rest_client.get_order_history(symbol, start_time, end_time, limit)

    # ==================== 仓位接口 ====================

    def get_positions(self, symbol: Optional[str] = None) -> List[Position]:
        """获取持仓列表"""
        return self.rest_client.get_positions(symbol)

    def set_leverage(self, symbol: str, leverage: int) -> Dict[str, Any]:
        """设置杠杆"""
        return self.rest_client.set_leverage(symbol, leverage)

    def set_margin_mode(self, symbol: str, margin_mode: str) -> Dict[str, Any]:
        """切换保证金模式"""
        return self.rest_client.set_margin_mode(symbol, margin_mode)

    # ==================== WebSocket 接口 ====================

    def ws_connect_public(self) -> bool:
        """连接公共WebSocket"""
        logger.info("Connecting to public WebSocket...")
        return self.ws_public.connect()

    def ws_connect_private(self) -> bool:
        """连接私有WebSocket"""
        logger.info("Connecting to private WebSocket...")
        return self.ws_private.connect()

    def ws_disconnect_public(self) -> None:
        """断开公共WebSocket"""
        logger.info("Disconnecting from public WebSocket...")
        self.ws_public.disconnect()

    def ws_disconnect_private(self) -> None:
        """断开私有WebSocket"""
        logger.info("Disconnecting from private WebSocket...")
        self.ws_private.disconnect()

    def ws_subscribe_ticker(
        self,
        symbols: List[str],
        callback: Optional[Callable] = None,
    ) -> bool:
        """订阅行情数据"""
        logger.info(f"Subscribing to ticker for {symbols}")
        return self.ws_public.subscribe("ticker", symbols=symbols, callback=callback)

    def ws_subscribe_kline(
        self,
        symbols: List[str],
        interval: str,
        callback: Optional[Callable] = None,
    ) -> bool:
        """订阅K线数据"""
        logger.info(f"Subscribing to kline for {symbols} ({interval})")
        return self.ws_public.subscribe(
            f"kline_{interval}", symbols=symbols, callback=callback
        )

    def ws_subscribe_orderbook(
        self,
        symbols: List[str],
        callback: Optional[Callable] = None,
    ) -> bool:
        """订阅深度数据"""
        logger.info(f"Subscribing to orderbook for {symbols}")
        return self.ws_public.subscribe("orderbook", symbols=symbols, callback=callback)

    def ws_subscribe_trade(
        self,
        symbols: List[str],
        callback: Optional[Callable] = None,
    ) -> bool:
        """订阅成交数据"""
        logger.info(f"Subscribing to trade for {symbols}")
        return self.ws_public.subscribe("trade", symbols=symbols, callback=callback)

    def ws_subscribe_order(
        self,
        symbols: Optional[List[str]] = None,
        callback: Optional[Callable] = None,
    ) -> bool:
        """订阅订单更新"""
        logger.info("Subscribing to order updates")
        return self.ws_private.subscribe("order", symbols=symbols, callback=callback)

    def ws_subscribe_position(
        self,
        symbols: Optional[List[str]] = None,
        callback: Optional[Callable] = None,
    ) -> bool:
        """订阅仓位更新"""
        logger.info("Subscribing to position updates")
        return self.ws_private.subscribe("position", symbols=symbols, callback=callback)

    def ws_subscribe_wallet(
        self,
        callback: Optional[Callable] = None,
    ) -> bool:
        """订阅余额更新"""
        logger.info("Subscribing to wallet updates")
        return self.ws_private.subscribe("wallet", callback=callback)

    def ws_unsubscribe(
        self,
        channel: str,
        symbols: Optional[List[str]] = None,
        is_private: bool = False,
    ) -> bool:
        """取消订阅"""
        ws = self.ws_private if is_private else self.ws_public
        logger.info(f"Unsubscribing from {channel}")
        return ws.unsubscribe(channel, symbols=symbols)

    def ws_get_message(
        self, is_private: bool = False, timeout: float = 1.0
    ):
        """获取WebSocket消息"""
        ws = self.ws_private if is_private else self.ws_public
        return ws.get_message(timeout=timeout)

    def ws_add_callback(
        self, channel: str, callback: Callable, is_private: bool = False
    ) -> None:
        """添加WebSocket回调"""
        ws = self.ws_private if is_private else self.ws_public
        ws.add_callback(channel, callback)

    # ==================== 便利方法 ====================

    def buy_market(
        self,
        symbol: str,
        quantity: float,
        reduce_only: bool = False,
    ) -> Order:
        """市价买入"""
        return self.create_order(
            symbol=symbol,
            side=OrderSide.BUY.value,
            order_type=OrderType.MARKET.value,
            quantity=quantity,
            reduce_only=reduce_only,
        )

    def sell_market(
        self,
        symbol: str,
        quantity: float,
        reduce_only: bool = False,
    ) -> Order:
        """市价卖出"""
        return self.create_order(
            symbol=symbol,
            side=OrderSide.SELL.value,
            order_type=OrderType.MARKET.value,
            quantity=quantity,
            reduce_only=reduce_only,
        )

    def buy_limit(
        self,
        symbol: str,
        quantity: float,
        price: float,
        time_in_force: str = "GTC",
        post_only: bool = False,
    ) -> Order:
        """限价买入"""
        return self.create_order(
            symbol=symbol,
            side=OrderSide.BUY.value,
            order_type=OrderType.LIMIT.value,
            quantity=quantity,
            price=price,
            time_in_force=time_in_force,
            post_only=post_only,
        )

    def sell_limit(
        self,
        symbol: str,
        quantity: float,
        price: float,
        time_in_force: str = "GTC",
        post_only: bool = False,
    ) -> Order:
        """限价卖出"""
        return self.create_order(
            symbol=symbol,
            side=OrderSide.SELL.value,
            order_type=OrderType.LIMIT.value,
            quantity=quantity,
            price=price,
            time_in_force=time_in_force,
            post_only=post_only,
        )

    def close(self) -> None:
        """关闭所有连接"""
        logger.info("Closing API client...")
        self.ws_disconnect_public()
        self.ws_disconnect_private()
        self.rest_client.close()
        if self.message_handler:
            self.message_handler.stop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
