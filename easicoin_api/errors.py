"""
Easicoin API 异常和错误处理模块

定义所有自定义异常类，用于处理API调用中的各种错误情况。
"""


class EasicoinException(Exception):
    """Easicoin API 基础异常类"""

    def __init__(self, message: str, code: int = None, response: dict = None):
        """
        初始化异常

        Args:
            message: 错误消息
            code: 错误代码
            response: 完整的API响应体
        """
        self.message = message
        self.code = code
        self.response = response
        super().__init__(self.message)

    def __str__(self):
        if self.code:
            return f"[{self.code}] {self.message}"
        return self.message


class APIError(EasicoinException):
    """API返回错误响应"""

    pass


class AuthenticationError(EasicoinException):
    """认证失败错误 (401)"""

    pass


class AuthorizationError(EasicoinException):
    """权限不足错误 (403)"""

    pass


class RateLimitError(EasicoinException):
    """请求速率限制错误 (429)"""

    pass


class BadRequestError(EasicoinException):
    """请求参数错误 (400)"""

    pass


class NotFoundError(EasicoinException):
    """资源未找到 (404)"""

    pass


class ServerError(EasicoinException):
    """服务器内部错误 (500)"""

    pass


class ServiceUnavailableError(EasicoinException):
    """服务暂时不可用 (503)"""

    pass


class NetworkError(EasicoinException):
    """网络连接错误"""

    pass


class TimeoutError(EasicoinException):
    """请求超时"""

    pass


class InvalidSignatureError(EasicoinException):
    """签名生成或验证失败"""

    pass


class InvalidParameterError(EasicoinException):
    """无效的参数"""

    pass


class WebSocketError(EasicoinException):
    """WebSocket 连接错误"""

    pass


class WebSocketAuthenticationError(EasicoinException):
    """WebSocket 认证失败"""

    pass


def handle_api_error(status_code: int, response: dict = None, message: str = None) -> None:
    """
    根据HTTP状态码和响应体抛出相应的异常

    Args:
        status_code: HTTP 状态码
        response: API 响应体
        message: 自定义错误消息

    Raises:
        对应的异常类
    """
    error_msg = message or (response.get("msg") if response else None) or "Unknown error"

    if status_code == 400:
        raise BadRequestError(error_msg, status_code, response)
    elif status_code == 401:
        raise AuthenticationError(error_msg, status_code, response)
    elif status_code == 403:
        raise AuthorizationError(error_msg, status_code, response)
    elif status_code == 404:
        raise NotFoundError(error_msg, status_code, response)
    elif status_code == 429:
        raise RateLimitError(error_msg, status_code, response)
    elif status_code >= 500:
        if status_code == 503:
            raise ServiceUnavailableError(error_msg, status_code, response)
        raise ServerError(error_msg, status_code, response)
    else:
        raise APIError(error_msg, status_code, response)
