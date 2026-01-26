"""
Easicoin API 枚举类型定义模块

包含订单类型、订单方向、K线间隔等枚举定义。
"""

from enum import Enum


class OrderSide(str, Enum):
    """订单方向"""

    BUY = "buy"
    SELL = "sell"


class OrderType(str, Enum):
    """订单类型"""

    MARKET = "market"  # 市价单
    LIMIT = "limit"  # 限价单


class OrderStatus(str, Enum):
    """订单状态"""

    PENDING = "pending"  # 待提交
    LIVE = "live"  # 进行中
    CLOSED = "closed"  # 已平仓
    CANCELLED = "cancelled"  # 已取消


class PositionSide(str, Enum):
    """仓位方向"""

    LONG = "long"  # 多头
    SHORT = "short"  # 空头


class MarginMode(str, Enum):
    """保证金模式"""

    ISOLATED = "isolated"  # 逐仓
    CROSS = "cross"  # 全仓


class KlineInterval(str, Enum):
    """K线间隔"""

    MIN_1 = "1m"  # 1分钟
    MIN_5 = "5m"  # 5分钟
    MIN_15 = "15m"  # 15分钟
    MIN_30 = "30m"  # 30分钟
    HOUR_1 = "1h"  # 1小时
    HOUR_2 = "2h"  # 2小时
    HOUR_4 = "4h"  # 4小时
    HOUR_6 = "6h"  # 6小时
    HOUR_8 = "8h"  # 8小时
    HOUR_12 = "12h"  # 12小时
    DAY_1 = "1d"  # 1天
    DAY_3 = "3d"  # 3天
    WEEK_1 = "1w"  # 1周
    MONTH_1 = "1M"  # 1月


class TickerDataType(str, Enum):
    """行情数据类型"""

    LATEST = "latest"  # 最新成交
    BEST_BID_ASK = "best_bid_ask"  # 最佳买卖价


class WebSocketChannel(str, Enum):
    """WebSocket 频道名称"""

    # 公共频道
    TICKER = "ticker"  # 行情数据
    KLINE = "kline"  # K线数据
    ORDERBOOK = "orderbook"  # 深度数据
    TRADE = "trade"  # 交易数据

    # 私有频道
    ORDER = "order"  # 订单更新
    POSITION = "position"  # 仓位更新
    WALLET = "wallet"  # 余额更新


class TimeInForce(str, Enum):
    """订单有效期"""

    GTC = "GTC"  # Good-Till-Cancelled (一直有效)
    IOC = "IOC"  # Immediate-Or-Cancel (立即或取消)
    FOK = "FOK"  # Fill-Or-Kill (全部成交或全部取消)
    POST_ONLY = "post_only"  # 只作为提交单


class ReduceOnly(str, Enum):
    """仅平仓标志"""

    TRUE = "true"
    FALSE = "false"


# 便利函数
def get_all_kline_intervals():
    """获取所有可用的K线间隔"""
    return [item.value for item in KlineInterval]


def get_all_order_sides():
    """获取所有订单方向"""
    return [item.value for item in OrderSide]


def get_all_order_types():
    """获取所有订单类型"""
    return [item.value for item in OrderType]


def get_all_margin_modes():
    """获取所有保证金模式"""
    return [item.value for item in MarginMode]
