"""
Easicoin API 认证签名模块

实现HMAC-SHA256签名机制，用于API认证。
基于最新的API文档规范：
- 待签名字符串 = timestamp + api_key + recv_window + (GET: queryString 或 POST: JSON body字符串)
- 使用HMAC-SHA256，secret作为key，输出十六进制字符串（小写）
- Access-Sign头为签名结果
"""

import hmac
import hashlib
import json
import logging
from typing import Optional, Dict, Any
from urllib.parse import urlencode

from .utils import get_timestamp_ms, build_query_string
from .errors import InvalidSignatureError

logger = logging.getLogger(__name__)


class Signature:
    """签名生成和验证类"""

    @staticmethod
    def generate_signature(
        timestamp: int,
        api_key: str,
        api_secret: str,
        recv_window: int,
        method: str = "GET",
        query_string: str = "",
        body: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        生成API请求签名

        根据Easicoin API文档的签名算法：
        待签名字符串 = timestamp + api_key + recv_window + (GET: queryString 或 POST: JSON body字符串)

        Args:
            timestamp: 时间戳（毫秒）
            api_key: API密钥
            api_secret: API密钥对应的secret
            recv_window: 接收窗口（毫秒），默认5000
            method: HTTP方法 (GET/POST)
            query_string: 查询字符串（GET请求）
            body: 请求体（POST请求）

        Returns:
            十六进制签名字符串（小写）

        Raises:
            InvalidSignatureError: 如果签名生成失败
        """
        try:
            # 构建待签名字符串
            if method.upper() == "GET":
                # GET请求：使用查询字符串
                body_str = query_string
            else:
                # POST请求：使用JSON格式的body
                body_str = json.dumps(body) if body else ""

            # 时间戳必须是整数
            message = f"{timestamp}{api_key}{recv_window}{body_str}"

            logger.debug(f"Message to sign: {message}")

            # 使用HMAC-SHA256签名
            signature = hmac.new(
                api_secret.encode("utf-8"), message.encode("utf-8"), hashlib.sha256
            ).hexdigest()

            logger.debug(f"Generated signature: {signature}")
            return signature

        except Exception as e:
            logger.error(f"Failed to generate signature: {e}")
            raise InvalidSignatureError(f"Signature generation failed: {str(e)}")

    @staticmethod
    def build_auth_headers(
        api_key: str,
        api_secret: str,
        method: str = "GET",
        query_string: str = "",
        body: Optional[Dict[str, Any]] = None,
        recv_window: int = 5000,
    ) -> Dict[str, str]:
        """
        构建认证请求头

        Args:
            api_key: API密钥
            api_secret: API密钥对应的secret
            method: HTTP方法
            query_string: 查询字符串
            body: 请求体
            recv_window: 接收窗口（毫秒）

        Returns:
            认证头字典
        """
        timestamp = get_timestamp_ms()

        signature = Signature.generate_signature(
            timestamp=timestamp,
            api_key=api_key,
            api_secret=api_secret,
            recv_window=recv_window,
            method=method,
            query_string=query_string,
            body=body,
        )

        return {
            "Access-Key": api_key,
            "Access-Sign": signature,
            "Access-Timestamp": str(timestamp),
            "Recv-Window": str(recv_window),
            "Content-Type": "application/json",
        }

    @staticmethod
    def build_websocket_auth_message(api_key: str, api_secret: str) -> Dict[str, Any]:
        """
        构建WebSocket认证消息

        Args:
            api_key: API密钥
            api_secret: API密钥对应的secret

        Returns:
            认证消息字典
        """
        timestamp = get_timestamp_ms()
        recv_window = 5000

        # WebSocket认证签名
        message = f"{timestamp}{api_key}{recv_window}"
        signature = hmac.new(
            api_secret.encode("utf-8"), message.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        return {
            "op": "auth",
            "args": {
                "apiKey": api_key,
                "timestamp": timestamp,
                "sign": signature,
            },
        }

    @staticmethod
    def verify_signature(
        timestamp: int,
        api_key: str,
        api_secret: str,
        recv_window: int,
        signature: str,
        method: str = "GET",
        query_string: str = "",
        body: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        验证签名（用于服务端校验）

        Args:
            timestamp: 时间戳
            api_key: API密钥
            api_secret: API密钥对应的secret
            recv_window: 接收窗口
            signature: 要验证的签名
            method: HTTP方法
            query_string: 查询字符串
            body: 请求体

        Returns:
            签名是否有效
        """
        expected_signature = Signature.generate_signature(
            timestamp=timestamp,
            api_key=api_key,
            api_secret=api_secret,
            recv_window=recv_window,
            method=method,
            query_string=query_string,
            body=body,
        )

        # 使用恒定时间比较来防止时序攻击
        return hmac.compare_digest(signature, expected_signature)


class AuthManager:
    """认证管理器"""

    def __init__(self, api_key: str, api_secret: str, recv_window: int = 5000):
        """
        初始化认证管理器

        Args:
            api_key: API密钥
            api_secret: API密钥对应的secret
            recv_window: 接收窗口（毫秒），默认5000
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.recv_window = recv_window

    def sign_request(
        self,
        method: str = "GET",
        query_string: str = "",
        body: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, str]:
        """
        为请求签名

        Args:
            method: HTTP方法
            query_string: 查询字符串
            body: 请求体

        Returns:
            认证头字典
        """
        return Signature.build_auth_headers(
            api_key=self.api_key,
            api_secret=self.api_secret,
            method=method,
            query_string=query_string,
            body=body,
            recv_window=self.recv_window,
        )

    def get_websocket_auth_message(self) -> Dict[str, Any]:
        """
        获取WebSocket认证消息

        Returns:
            认证消息字典
        """
        return Signature.build_websocket_auth_message(
            api_key=self.api_key, api_secret=self.api_secret
        )
