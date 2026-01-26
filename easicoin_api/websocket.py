"""
Easicoin API WebSocket 客户端模块

实现WebSocket连接、认证、订阅、心跳和自动重连等功能。
公共: wss://ws.easicoin.io/contract/public/v1
私有: wss://ws.easicoin.io/contract/private/v1
"""

import json
import time
import logging
import threading
from typing import Optional, Dict, Any, Callable, List
from queue import Queue, Empty
from collections import defaultdict

try:
    import websocket
except ImportError:
    raise ImportError("websocket-client is required. Install it with: pip install websocket-client")

from .auth import Signature
from .models import WebSocketMessage
from .errors import WebSocketError, WebSocketAuthenticationError
from .utils import get_timestamp_ms

logger = logging.getLogger(__name__)


class WebSocketClient:
    """Easicoin WebSocket 客户端"""

    PUBLIC_WS_URL = "wss://ws.easicoin.io/contract/public/v1"
    PRIVATE_WS_URL = "wss://ws.easicoin.io/contract/private/v1"

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        is_private: bool = False,
        ping_interval: int = 30,
        ping_timeout: int = 10,
        max_reconnect_attempts: int = 5,
        reconnect_delay: float = 1.0,
    ):
        """
        初始化WebSocket客户端

        Args:
            api_key: API密钥（私有连接必需）
            api_secret: API密钥对应的secret（私有连接必需）
            is_private: 是否为私有连接
            ping_interval: 心跳间隔（秒）
            ping_timeout: 心跳超时（秒）
            max_reconnect_attempts: 最大重连次数
            reconnect_delay: 重连延迟（秒）
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.is_private = is_private
        self.ping_interval = ping_interval
        self.ping_timeout = ping_timeout
        self.max_reconnect_attempts = max_reconnect_attempts
        self.reconnect_delay = reconnect_delay

        self.ws_url = self.PRIVATE_WS_URL if is_private else self.PUBLIC_WS_URL
        self.ws = None
        self.is_connected = False
        self.is_authenticated = False
        self.reconnect_count = 0

        # 消息队列和回调
        self.message_queue = Queue()
        self.callbacks = defaultdict(list)  # {channel: [callback, ...]}

        # 线程管理
        self.thread = None
        self.running = False
        self.lock = threading.Lock()

    def connect(self) -> bool:
        """
        连接到WebSocket服务器

        Returns:
            是否连接成功
        """
        if self.is_connected:
            logger.warning("Already connected")
            return True

        try:
            logger.info(f"Connecting to {self.ws_url}")

            self.ws = websocket.WebSocketApp(
                self.ws_url,
                on_message=self._on_message,
                on_error=self._on_error,
                on_close=self._on_close,
                on_open=self._on_open,
                ping_interval=self.ping_interval,
                ping_timeout=self.ping_timeout,
            )

            self.running = True
            self.thread = threading.Thread(target=self._run_forever, daemon=True)
            self.thread.start()

            # 等待连接建立
            time.sleep(1)
            return self.is_connected

        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            return False

    def disconnect(self) -> None:
        """断开连接"""
        self.running = False
        if self.ws:
            self.ws.close()
            self.is_connected = False
            self.is_authenticated = False

    def _run_forever(self) -> None:
        """运行WebSocket连接"""
        try:
            self.ws.run_forever()
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
            self._attempt_reconnect()

    def _on_open(self, ws) -> None:
        """连接打开回调"""
        logger.info("WebSocket connected")
        self.is_connected = True
        self.reconnect_count = 0

        # 私有连接需要认证
        if self.is_private and self.api_key and self.api_secret:
            self._authenticate()

    def _on_message(self, ws, message: str) -> None:
        """接收消息回调"""
        try:
            data = json.loads(message)
            logger.debug(f"Received message: {data}")

            # 解析消息
            msg = self._parse_message(data)

            # 处理认证响应
            if msg.type == "auth":
                if data.get("code") == 0:
                    logger.info("WebSocket authenticated successfully")
                    self.is_authenticated = True
                else:
                    logger.error(f"Authentication failed: {data.get('msg')}")
                    raise WebSocketAuthenticationError(data.get("msg", "Authentication failed"))
                return

            # 处理订阅确认
            if msg.type == "subscribe":
                logger.debug(f"Subscribed to {msg.channel}")
                return

            # 处理数据消息
            if msg.type == "data":
                self.message_queue.put(msg)

                # 触发回调
                if msg.channel in self.callbacks:
                    for callback in self.callbacks[msg.channel]:
                        try:
                            callback(msg)
                        except Exception as e:
                            logger.error(f"Callback error: {e}")

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse message: {e}")
        except Exception as e:
            logger.error(f"Message processing error: {e}")

    def _on_error(self, ws, error) -> None:
        """错误回调"""
        logger.error(f"WebSocket error: {error}")

    def _on_close(self, ws, close_status_code, close_msg) -> None:
        """关闭回调"""
        logger.info(f"WebSocket closed: {close_status_code} - {close_msg}")
        self.is_connected = False
        self.is_authenticated = False

        if self.running:
            self._attempt_reconnect()

    def _attempt_reconnect(self) -> None:
        """尝试重新连接"""
        if not self.running:
            return

        if self.reconnect_count >= self.max_reconnect_attempts:
            logger.error(f"Max reconnect attempts ({self.max_reconnect_attempts}) reached")
            self.running = False
            return

        wait_time = self.reconnect_delay * (2 ** self.reconnect_count)
        logger.info(f"Reconnecting in {wait_time}s (attempt {self.reconnect_count + 1})")

        time.sleep(wait_time)
        self.reconnect_count += 1

        if self.connect():
            logger.info("Reconnected successfully")
        else:
            self._attempt_reconnect()

    def _authenticate(self) -> None:
        """进行WebSocket认证"""
        if not self.ws or not self.is_connected:
            logger.warning("Not connected")
            return

        auth_msg = Signature.build_websocket_auth_message(self.api_key, self.api_secret)
        logger.debug(f"Sending auth message: {auth_msg}")
        self.ws.send(json.dumps(auth_msg))

    def _parse_message(self, data: Dict[str, Any]) -> WebSocketMessage:
        """解析WebSocket消息"""
        msg = WebSocketMessage(
            type=data.get("type", "data"),
            data=data.get("data", {}),
            channel=data.get("channel"),
            symbol=data.get("symbol"),
            timestamp=data.get("timestamp"),
        )
        return msg

    def subscribe(
        self,
        channel: str,
        symbols: Optional[List[str]] = None,
        callback: Optional[Callable[[WebSocketMessage], None]] = None,
    ) -> bool:
        """
        订阅频道

        Args:
            channel: 频道名称 (ticker, kline, orderbook, trade, order, position, wallet)
            symbols: 交易对列表（可选）
            callback: 消息回调函数

        Returns:
            是否订阅成功
        """
        if not self.is_connected:
            logger.error("Not connected")
            return False

        # 如果是私有频道且未认证，先认证
        if self.is_private and not self.is_authenticated:
            logger.warning("Not authenticated, authenticating...")
            self._authenticate()
            time.sleep(1)  # 等待认证完成

        # 注册回调
        if callback:
            self.callbacks[channel].append(callback)

        # 构建订阅消息
        subscribe_msg = {
            "op": "subscribe",
            "args": {
                "channel": channel,
            },
        }
        if symbols:
            subscribe_msg["args"]["symbols"] = symbols

        logger.debug(f"Subscribing to {channel}: {subscribe_msg}")
        try:
            self.ws.send(json.dumps(subscribe_msg))
            return True
        except Exception as e:
            logger.error(f"Failed to subscribe: {e}")
            return False

    def unsubscribe(self, channel: str, symbols: Optional[List[str]] = None) -> bool:
        """
        取消订阅

        Args:
            channel: 频道名称
            symbols: 交易对列表（可选）

        Returns:
            是否取消订阅成功
        """
        if not self.is_connected:
            logger.error("Not connected")
            return False

        # 移除回调
        if channel in self.callbacks:
            del self.callbacks[channel]

        # 构建取消订阅消息
        unsubscribe_msg = {
            "op": "unsubscribe",
            "args": {
                "channel": channel,
            },
        }
        if symbols:
            unsubscribe_msg["args"]["symbols"] = symbols

        logger.debug(f"Unsubscribing from {channel}")
        try:
            self.ws.send(json.dumps(unsubscribe_msg))
            return True
        except Exception as e:
            logger.error(f"Failed to unsubscribe: {e}")
            return False

    def get_message(self, timeout: Optional[float] = 1.0) -> Optional[WebSocketMessage]:
        """
        获取消息（非阻塞）

        Args:
            timeout: 超时时间（秒）

        Returns:
            WebSocketMessage 或 None
        """
        try:
            return self.message_queue.get(timeout=timeout)
        except Empty:
            return None

    def add_callback(
        self, channel: str, callback: Callable[[WebSocketMessage], None]
    ) -> None:
        """
        添加消息回调

        Args:
            channel: 频道名称
            callback: 回调函数
        """
        self.callbacks[channel].append(callback)

    def remove_callback(
        self, channel: str, callback: Callable[[WebSocketMessage], None]
    ) -> None:
        """
        移除消息回调

        Args:
            channel: 频道名称
            callback: 回调函数
        """
        if channel in self.callbacks and callback in self.callbacks[channel]:
            self.callbacks[channel].remove(callback)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()


# 便利函数用于异步消息处理
class AsyncMessageHandler:
    """异步消息处理器"""

    def __init__(self, ws_client: WebSocketClient):
        """
        初始化异步处理器

        Args:
            ws_client: WebSocket客户端实例
        """
        self.ws_client = ws_client
        self.running = False
        self.thread = None

    def start(self) -> None:
        """启动消息处理线程"""
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self._process_messages, daemon=True)
        self.thread.start()
        logger.info("Message handler started")

    def stop(self) -> None:
        """停止消息处理线程"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("Message handler stopped")

    def _process_messages(self) -> None:
        """处理消息线程"""
        while self.running:
            msg = self.ws_client.get_message(timeout=1.0)
            if msg:
                logger.debug(f"Processing message: {msg.channel}")
