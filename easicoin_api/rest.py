"""
Easicoin API REST客户端模块

实现所有REST API接口调用。
Base URL: https://api.easicoin.io
公共接口: /futures/public/v1/...
私有接口: /futures/private/v1/...
"""

import logging
import time
from typing import Optional, Dict, Any, List
import requests
from requests.exceptions import RequestException, Timeout, ConnectionError

from .auth import AuthManager, Signature
from .errors import (
    handle_api_error,
    NetworkError,
    TimeoutError as EasicoinTimeoutError,
    InvalidParameterError,
)
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
)
from .enums import OrderSide, OrderType, KlineInterval, MarginMode
from .utils import (
    RateLimiter,
    get_timestamp_ms,
    clean_dict,
    build_query_string,
    is_valid_symbol,
    safe_get,
)

logger = logging.getLogger(__name__)


class RESTClient:
    """Easicoin REST API 客户端"""

    BASE_URL = "https://api.easicoin.io"
    PUBLIC_PREFIX = "/futures/public/v1"
    PRIVATE_PREFIX = "/futures/private/v1"

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        recv_window: int = 5000,
        timeout: int = 30,
        rate_limit: float = 10,
    ):
        """
        初始化REST客户端

        Args:
            api_key: API密钥（可选，用于私有接口）
            api_secret: API密钥对应的secret（可选，用于私有接口）
            recv_window: 接收窗口（毫秒），默认5000
            timeout: 请求超时时间（秒），默认30
            rate_limit: 每秒最大请求数，默认10
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.recv_window = recv_window
        self.timeout = timeout

        self.auth_manager = AuthManager(api_key, api_secret, recv_window) if api_key else None
        self.rate_limiter = RateLimiter(rate=rate_limit, period=1.0)

        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Easicoin-Python-API-Client/1.0"})

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        signed: bool = False,
    ) -> Dict[str, Any]:
        """
        发送HTTP请求

        Args:
            method: HTTP方法 (GET/POST/PUT/DELETE)
            endpoint: API端点（不含BaseURL）
            params: 查询参数
            data: 请求体（JSON）
            signed: 是否需要签名

        Returns:
            API响应的data部分

        Raises:
            各种异常
        """
        # 限流
        self.rate_limiter.wait()

        # 构建完整URL
        url = self.BASE_URL + endpoint

        # 参数处理
        params = clean_dict(params) if params else {}
        data = clean_dict(data) if data else None

        headers = {"Content-Type": "application/json"}

        # 签名处理
        if signed:
            if not self.auth_manager:
                raise InvalidParameterError("API key and secret required for signed requests")

            query_string = build_query_string(params)
            auth_headers = self.auth_manager.sign_request(
                method=method, query_string=query_string, body=data
            )
            headers.update(auth_headers)

        try:
            logger.debug(f"{method} {url} params={params} data={data}")

            if method.upper() == "GET":
                response = self.session.get(
                    url, params=params, headers=headers, timeout=self.timeout
                )
            elif method.upper() == "POST":
                response = self.session.post(
                    url, params=params, json=data, headers=headers, timeout=self.timeout
                )
            elif method.upper() == "PUT":
                response = self.session.put(
                    url, params=params, json=data, headers=headers, timeout=self.timeout
                )
            elif method.upper() == "DELETE":
                response = self.session.delete(
                    url, params=params, json=data, headers=headers, timeout=self.timeout
                )
            else:
                raise InvalidParameterError(f"Unsupported HTTP method: {method}")

            # 检查HTTP状态码
            if response.status_code != 200:
                try:
                    error_data = response.json()
                except:
                    error_data = None

                handle_api_error(
                    response.status_code,
                    error_data,
                    f"HTTP {response.status_code}: {response.text}",
                )

            # 解析响应
            resp_json = response.json()
            logger.debug(f"Response: {resp_json}")

            # 检查API返回码
            code = resp_json.get("code", 0)
            if code != 0:
                handle_api_error(code, resp_json, resp_json.get("msg", "Unknown error"))

            return resp_json.get("data", {})

        except (Timeout, ConnectionError) as e:
            logger.error(f"Request timeout or connection error: {e}")
            raise EasicoinTimeoutError(f"Request failed: {str(e)}")
        except RequestException as e:
            logger.error(f"Request failed: {e}")
            raise NetworkError(f"Request failed: {str(e)}")

    # ==================== 公共接口（无需认证） ====================

    def get_instruments(self) -> List[Instrument]:
        """
        获取交易对信息列表

        Returns:
            Instrument列表
        """
        data = self._request("GET", f"{self.PUBLIC_PREFIX}/instruments")
        instruments = []
        for item in data if isinstance(data, list) else data.get("instruments", []):
            instruments.append(
                Instrument(
                    symbol=item.get("symbol"),
                    base_currency=item.get("base_currency"),
                    quote_currency=item.get("quote_currency"),
                    price_precision=item.get("price_precision", 2),
                    quantity_precision=item.get("quantity_precision", 4),
                    min_price=float(item.get("min_price", 0)),
                    max_price=float(item.get("max_price", 999999)),
                    min_quantity=float(item.get("min_quantity", 0.001)),
                    max_quantity=float(item.get("max_quantity", 1000000)),
                    taker_fee=float(item.get("taker_fee", 0.0005)),
                    maker_fee=float(item.get("maker_fee", 0.0002)),
                    leverage=item.get("leverage", 1),
                    is_perpetual=item.get("is_perpetual", True),
                    status=item.get("status", "active"),
                )
            )
        return instruments

    def get_ticker(self, symbol: str) -> Ticker:
        """
        获取行情数据

        Args:
            symbol: 交易对 (BTCUSDT)

        Returns:
            Ticker对象
        """
        if not is_valid_symbol(symbol):
            raise InvalidParameterError(f"Invalid symbol: {symbol}")

        params = {"symbol": symbol}
        data = self._request("GET", f"{self.PUBLIC_PREFIX}/market/ticker", params=params)

        return Ticker(
            symbol=data.get("symbol"),
            last_price=float(data.get("last_price", 0)),
            bid_price=float(data.get("bid_price", 0)),
            ask_price=float(data.get("ask_price", 0)),
            high_price=float(data.get("high_price")) if data.get("high_price") else None,
            low_price=float(data.get("low_price")) if data.get("low_price") else None,
            open_price=float(data.get("open_price")) if data.get("open_price") else None,
            volume=float(data.get("volume")) if data.get("volume") else None,
            quote_volume=float(data.get("quote_volume"))
            if data.get("quote_volume")
            else None,
            timestamp=data.get("timestamp"),
        )

    def get_orderbook(
        self, symbol: str, limit: int = 20
    ) -> OrderBook:
        """
        获取深度数据

        Args:
            symbol: 交易对
            limit: 深度档位数 (default: 20, max: 100)

        Returns:
            OrderBook对象
        """
        if not is_valid_symbol(symbol):
            raise InvalidParameterError(f"Invalid symbol: {symbol}")

        if limit < 1 or limit > 100:
            raise InvalidParameterError("Limit must be between 1 and 100")

        params = {"symbol": symbol, "limit": limit}
        data = self._request("GET", f"{self.PUBLIC_PREFIX}/market/orderbook", params=params)

        return OrderBook(
            symbol=data.get("symbol"),
            bids=data.get("bids", []),
            asks=data.get("asks", []),
            timestamp=data.get("timestamp"),
        )

    def get_klines(
        self,
        symbol: str,
        interval: str,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: int = 500,
    ) -> List[Kline]:
        """
        获取K线数据

        Args:
            symbol: 交易对
            interval: K线间隔 (1m, 5m, 15m, 1h, 4h, 1d, 1w, 1M)
            start_time: 开始时间戳(ms)
            end_time: 结束时间戳(ms)
            limit: 返回条数 (default: 500, max: 1000)

        Returns:
            Kline列表
        """
        if not is_valid_symbol(symbol):
            raise InvalidParameterError(f"Invalid symbol: {symbol}")

        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit,
        }
        if start_time:
            params["startTime"] = start_time
        if end_time:
            params["endTime"] = end_time

        data = self._request("GET", f"{self.PUBLIC_PREFIX}/market/kline", params=params)

        klines = []
        for item in data if isinstance(data, list) else data.get("klines", []):
            klines.append(
                Kline(
                    timestamp=item[0],
                    open=float(item[1]),
                    high=float(item[2]),
                    low=float(item[3]),
                    close=float(item[4]),
                    volume=float(item[5]),
                    quote_volume=float(item[6]),
                )
            )
        return klines

    def get_mark_price_klines(
        self,
        symbol: str,
        interval: str,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: int = 500,
    ) -> List[Kline]:
        """
        获取标记价格K线

        Args:
            symbol: 交易对
            interval: K线间隔
            start_time: 开始时间戳(ms)
            end_time: 结束时间戳(ms)
            limit: 返回条数

        Returns:
            Kline列表
        """
        if not is_valid_symbol(symbol):
            raise InvalidParameterError(f"Invalid symbol: {symbol}")

        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit,
        }
        if start_time:
            params["startTime"] = start_time
        if end_time:
            params["endTime"] = end_time

        data = self._request(
            "GET", f"{self.PUBLIC_PREFIX}/market/mark-price-kline", params=params
        )

        klines = []
        for item in data if isinstance(data, list) else data.get("klines", []):
            klines.append(
                Kline(
                    timestamp=item[0],
                    open=float(item[1]),
                    high=float(item[2]),
                    low=float(item[3]),
                    close=float(item[4]),
                    volume=float(item[5]),
                    quote_volume=float(item[6]),
                )
            )
        return klines

    def get_funding_rate_history(
        self,
        symbol: str,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: int = 100,
    ) -> List[FundingRate]:
        """
        获取资金费率历史

        Args:
            symbol: 交易对
            start_time: 开始时间戳(ms)
            end_time: 结束时间戳(ms)
            limit: 返回条数

        Returns:
            FundingRate列表
        """
        if not is_valid_symbol(symbol):
            raise InvalidParameterError(f"Invalid symbol: {symbol}")

        params = {"symbol": symbol, "limit": limit}
        if start_time:
            params["startTime"] = start_time
        if end_time:
            params["endTime"] = end_time

        data = self._request(
            "GET", f"{self.PUBLIC_PREFIX}/market/funding-rate-history", params=params
        )

        funding_rates = []
        for item in data if isinstance(data, list) else data.get("funding_rates", []):
            funding_rates.append(
                FundingRate(
                    symbol=item.get("symbol"),
                    funding_rate=float(item.get("funding_rate", 0)),
                    funding_timestamp=item.get("funding_timestamp", 0),
                    next_funding_rate=float(item.get("next_funding_rate"))
                    if item.get("next_funding_rate")
                    else None,
                    next_funding_timestamp=item.get("next_funding_timestamp"),
                )
            )
        return funding_rates

    # ==================== 私有接口（需要认证） ====================

    def get_wallet(self) -> Dict[str, Wallet]:
        """
        获取账户余额

        Returns:
            {货币: Wallet对象} 字典
        """
        data = self._request("GET", f"{self.PRIVATE_PREFIX}/account/wallet", signed=True)

        wallets = {}
        for currency, balance_info in data.items():
            wallets[currency] = Wallet(
                currency=currency,
                free=float(balance_info.get("free", 0)),
                locked=float(balance_info.get("locked", 0)),
            )
        return wallets

    def get_fee_rate(self, symbol: Optional[str] = None) -> FeeRate:
        """
        获取费率信息

        Args:
            symbol: 交易对（可选，不指定则返回全局费率）

        Returns:
            FeeRate对象
        """
        params = {}
        if symbol:
            params["symbol"] = symbol

        data = self._request("GET", f"{self.PRIVATE_PREFIX}/account/fee-rate", params=params, signed=True)

        return FeeRate(
            symbol=data.get("symbol"),
            maker_fee=float(data.get("maker_fee", 0)),
            taker_fee=float(data.get("taker_fee", 0)),
        )

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
        """
        创建订单

        Args:
            symbol: 交易对
            side: 方向 (buy/sell)
            order_type: 订单类型 (market/limit)
            quantity: 数量
            price: 价格（limit单必需）
            time_in_force: 有效期 (GTC/IOC/FOK/post_only)
            reduce_only: 是否仅平仓
            post_only: 是否仅提交单
            client_id: 客户端订单ID

        Returns:
            Order对象
        """
        data = {
            "symbol": symbol,
            "side": side,
            "order_type": order_type,
            "quantity": quantity,
        }
        if price is not None:
            data["price"] = price
        if time_in_force:
            data["time_in_force"] = time_in_force
        if reduce_only:
            data["reduce_only"] = reduce_only
        if post_only:
            data["post_only"] = post_only
        if client_id:
            data["client_id"] = client_id

        resp_data = self._request(
            "POST", f"{self.PRIVATE_PREFIX}/order/create", data=data, signed=True
        )

        return Order(
            order_id=resp_data.get("order_id"),
            symbol=resp_data.get("symbol"),
            order_type=resp_data.get("order_type"),
            side=resp_data.get("side"),
            price=float(resp_data.get("price", 0)),
            quantity=float(resp_data.get("quantity", 0)),
            filled_quantity=float(resp_data.get("filled_quantity", 0)),
            status=resp_data.get("status"),
            created_at=resp_data.get("created_at"),
            updated_at=resp_data.get("updated_at"),
        )

    def replace_order(
        self,
        order_id: str,
        quantity: Optional[float] = None,
        price: Optional[float] = None,
    ) -> Order:
        """
        改单

        Args:
            order_id: 订单ID
            quantity: 新数量
            price: 新价格

        Returns:
            Order对象
        """
        data = {"order_id": order_id}
        if quantity is not None:
            data["quantity"] = quantity
        if price is not None:
            data["price"] = price

        resp_data = self._request(
            "POST", f"{self.PRIVATE_PREFIX}/order/replace", data=data, signed=True
        )

        return Order(
            order_id=resp_data.get("order_id"),
            symbol=resp_data.get("symbol"),
            order_type=resp_data.get("order_type"),
            side=resp_data.get("side"),
            price=float(resp_data.get("price", 0)),
            quantity=float(resp_data.get("quantity", 0)),
            filled_quantity=float(resp_data.get("filled_quantity", 0)),
            status=resp_data.get("status"),
        )

    def cancel_order(self, order_id: str) -> Order:
        """
        取消订单

        Args:
            order_id: 订单ID

        Returns:
            Order对象
        """
        data = {"order_id": order_id}

        resp_data = self._request(
            "POST", f"{self.PRIVATE_PREFIX}/order/cancel", data=data, signed=True
        )

        return Order(
            order_id=resp_data.get("order_id"),
            symbol=resp_data.get("symbol"),
            order_type=resp_data.get("order_type"),
            side=resp_data.get("side"),
            price=float(resp_data.get("price", 0)),
            quantity=float(resp_data.get("quantity", 0)),
            filled_quantity=float(resp_data.get("filled_quantity", 0)),
            status=resp_data.get("status"),
        )

    def cancel_all_orders(self, symbol: Optional[str] = None) -> List[Order]:
        """
        批量取消订单

        Args:
            symbol: 交易对（可选，不指定则取消所有订单）

        Returns:
            Order列表
        """
        data = {}
        if symbol:
            data["symbol"] = symbol

        resp_data = self._request(
            "POST", f"{self.PRIVATE_PREFIX}/order/cancel-all", data=data, signed=True
        )

        orders = []
        for order_info in resp_data if isinstance(resp_data, list) else resp_data.get(
            "orders", []
        ):
            orders.append(
                Order(
                    order_id=order_info.get("order_id"),
                    symbol=order_info.get("symbol"),
                    order_type=order_info.get("order_type"),
                    side=order_info.get("side"),
                    price=float(order_info.get("price", 0)),
                    quantity=float(order_info.get("quantity", 0)),
                    filled_quantity=float(order_info.get("filled_quantity", 0)),
                    status=order_info.get("status"),
                )
            )
        return orders

    def get_open_orders(self, symbol: Optional[str] = None) -> List[Order]:
        """
        获取活跃订单

        Args:
            symbol: 交易对（可选）

        Returns:
            Order列表
        """
        params = {}
        if symbol:
            params["symbol"] = symbol

        data = self._request(
            "GET", f"{self.PRIVATE_PREFIX}/order/open", params=params, signed=True
        )

        orders = []
        for order_info in data if isinstance(data, list) else data.get("orders", []):
            orders.append(
                Order(
                    order_id=order_info.get("order_id"),
                    symbol=order_info.get("symbol"),
                    order_type=order_info.get("order_type"),
                    side=order_info.get("side"),
                    price=float(order_info.get("price", 0)),
                    quantity=float(order_info.get("quantity", 0)),
                    filled_quantity=float(order_info.get("filled_quantity", 0)),
                    status=order_info.get("status"),
                    created_at=order_info.get("created_at"),
                    updated_at=order_info.get("updated_at"),
                )
            )
        return orders

    def get_order_history(
        self,
        symbol: Optional[str] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: int = 100,
    ) -> List[Order]:
        """
        获取历史订单

        Args:
            symbol: 交易对（可选）
            start_time: 开始时间戳(ms)
            end_time: 结束时间戳(ms)
            limit: 返回条数

        Returns:
            Order列表
        """
        params = {"limit": limit}
        if symbol:
            params["symbol"] = symbol
        if start_time:
            params["startTime"] = start_time
        if end_time:
            params["endTime"] = end_time

        data = self._request(
            "GET", f"{self.PRIVATE_PREFIX}/order/history", params=params, signed=True
        )

        orders = []
        for order_info in data if isinstance(data, list) else data.get("orders", []):
            orders.append(
                Order(
                    order_id=order_info.get("order_id"),
                    symbol=order_info.get("symbol"),
                    order_type=order_info.get("order_type"),
                    side=order_info.get("side"),
                    price=float(order_info.get("price", 0)),
                    quantity=float(order_info.get("quantity", 0)),
                    filled_quantity=float(order_info.get("filled_quantity", 0)),
                    status=order_info.get("status"),
                    created_at=order_info.get("created_at"),
                    updated_at=order_info.get("updated_at"),
                    fee=float(order_info.get("fee")) if order_info.get("fee") else None,
                )
            )
        return orders

    def get_positions(self, symbol: Optional[str] = None) -> List[Position]:
        """
        获取持仓列表

        Args:
            symbol: 交易对（可选）

        Returns:
            Position列表
        """
        params = {}
        if symbol:
            params["symbol"] = symbol

        data = self._request(
            "GET", f"{self.PRIVATE_PREFIX}/position/list", params=params, signed=True
        )

        positions = []
        for pos_info in data if isinstance(data, list) else data.get("positions", []):
            positions.append(
                Position(
                    symbol=pos_info.get("symbol"),
                    side=pos_info.get("side"),
                    quantity=float(pos_info.get("quantity", 0)),
                    entry_price=float(pos_info.get("entry_price", 0)),
                    current_price=float(pos_info.get("current_price", 0)),
                    mark_price=float(pos_info.get("mark_price"))
                    if pos_info.get("mark_price")
                    else None,
                    leverage=int(pos_info.get("leverage", 1)),
                    margin=float(pos_info.get("margin", 0)),
                    margin_mode=pos_info.get("margin_mode", "isolated"),
                    liquidation_price=float(pos_info.get("liquidation_price"))
                    if pos_info.get("liquidation_price")
                    else None,
                    unrealised_pnl=float(pos_info.get("unrealised_pnl"))
                    if pos_info.get("unrealised_pnl")
                    else None,
                    realised_pnl=float(pos_info.get("realised_pnl"))
                    if pos_info.get("realised_pnl")
                    else None,
                    roi=float(pos_info.get("roi")) if pos_info.get("roi") else None,
                )
            )
        return positions

    def set_leverage(self, symbol: str, leverage: int) -> Dict[str, Any]:
        """
        设置杠杆

        Args:
            symbol: 交易对
            leverage: 杠杆倍数

        Returns:
            设置结果
        """
        data = {"symbol": symbol, "leverage": leverage}

        return self._request(
            "POST", f"{self.PRIVATE_PREFIX}/position/leverage", data=data, signed=True
        )

    def set_margin_mode(self, symbol: str, margin_mode: str) -> Dict[str, Any]:
        """
        切换保证金模式

        Args:
            symbol: 交易对
            margin_mode: 保证金模式 (isolated/cross)

        Returns:
            切换结果
        """
        data = {"symbol": symbol, "margin_mode": margin_mode}

        return self._request(
            "POST", f"{self.PRIVATE_PREFIX}/position/margin-mode", data=data, signed=True
        )

    def close(self) -> None:
        """关闭会话"""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
