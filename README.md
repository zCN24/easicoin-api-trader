# Easicoin API Python客户端库

一个完整的、生产级别的Python API客户端库，用于**Easicoin交易所**的期货交易。支持REST API和WebSocket实时数据流。

**版本**: 1.0.0  
**文档**: https://www.easicoin.io/api-doc/zh-CN/common/Info

## 功能特性

✅ **完整的REST API支持**
- 公共行情接口（无需认证）：交易对、行情、深度、K线、资金费率等
- 私有账户接口（需认证）：余额、下单、改单、撤单、仓位管理等
- 自动限流和重试机制
- 完整的类型提示和文档

✅ **WebSocket实时数据**
- 公共数据流：ticker、kline、orderbook、trade
- 私有数据流：order、position、wallet（需认证）
- 自动心跳、断线重连、订阅管理
- 灵活的回调机制

✅ **安全认证**
- HMAC-SHA256签名算法（按最新API文档）
- 自动时间戳处理和签名生成
- WebSocket认证支持

✅ **开发友好**
- 完整的错误处理和自定义异常
- 日志支持
- 丰富的示例代码
- Dataclass数据模型

## 安装

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

或者手动安装：

```bash
pip install requests websocket-client
```

### 2. 导入使用

```python
from easicoin_api import EasicoinAPI

# 初始化客户端
client = EasicoinAPI(api_key="your_key", api_secret="your_secret")
```

## 快速开始

### 获取公开行情数据（无需密钥）

```python
from easicoin_api import RESTClient

client = RESTClient()

# 获取交易对信息
instruments = client.get_instruments()

# 获取行情
ticker = client.get_ticker("BTCUSDT")
print(f"BTC最新价: ${ticker.last_price}")

# 获取K线
klines = client.get_klines("BTCUSDT", interval="1h", limit=10)
for kline in klines:
    print(f"K线: 开={kline.open}, 收={kline.close}, 量={kline.volume}")

# 获取深度
orderbook = client.get_orderbook("BTCUSDT", limit=10)
print(f"买一: ${orderbook.bids[0][0]}")
print(f"卖一: ${orderbook.asks[0][0]}")
```

### 账户操作和下单

```python
from easicoin_api import EasicoinAPI

client = EasicoinAPI(api_key="your_key", api_secret="your_secret")

# 获取余额
wallets = client.get_wallet()
for currency, wallet in wallets.items():
    print(f"{currency}: 可用={wallet.free}, 冻结={wallet.locked}")

# 查询当前仓位
positions = client.get_positions()
for pos in positions:
    print(f"{pos.symbol}: {pos.side} {pos.quantity} @ ${pos.entry_price}")

# 限价买入
order = client.buy_limit("BTCUSDT", quantity=0.1, price=30000)
print(f"订单ID: {order.order_id}, 状态: {order.status}")

# 限价卖出
order = client.sell_limit("BTCUSDT", quantity=0.1, price=40000)

# 取消订单
client.cancel_order(order.order_id)

# 设置杠杆
client.set_leverage("BTCUSDT", leverage=10)

# 切换保证金模式
client.set_margin_mode("BTCUSDT", margin_mode="isolated")
```

### WebSocket实时数据订阅

```python
from easicoin_api import EasicoinAPI

client = EasicoinAPI(api_key="your_key", api_secret="your_secret")

# 连接公开WebSocket
client.ws_connect_public()

# 定义回调函数
def on_ticker(msg):
    print(f"收到行情: {msg.symbol} - 价格={msg.data['last_price']}")

# 订阅行情
client.ws_subscribe_ticker(["BTCUSDT", "ETHUSDT"], callback=on_ticker)

# 接收消息
import time
time.sleep(5)  # 接收5秒的数据

# 断开连接
client.close()
```

### 私有数据流订阅

```python
from easicoin_api import EasicoinAPI

client = EasicoinAPI(api_key="your_key", api_secret="your_secret")

# 连接私有WebSocket（需认证）
client.ws_connect_private()

def on_order(msg):
    print(f"订单更新: {msg.data}")

def on_position(msg):
    print(f"仓位更新: {msg.data}")

# 订阅私有数据
client.ws_subscribe_order(callback=on_order)
client.ws_subscribe_position(callback=on_position)

import time
time.sleep(10)

client.close()
```

## API 文档

### 主客户端类 (EasicoinAPI)

#### 公开行情接口

- `get_instruments() -> List[Instrument]` - 获取所有交易对信息
- `get_ticker(symbol: str) -> Ticker` - 获取行情数据
- `get_orderbook(symbol: str, limit: int = 20) -> OrderBook` - 获取深度数据
- `get_klines(symbol: str, interval: str, start_time: int = None, end_time: int = None, limit: int = 500) -> List[Kline]` - 获取K线数据
- `get_mark_price_klines(...)` - 获取标记价格K线
- `get_funding_rate_history(...)` - 获取资金费率历史

#### 账户接口

- `get_wallet() -> Dict[str, Wallet]` - 获取余额
- `get_fee_rate(symbol: str = None) -> FeeRate` - 获取费率

#### 订单接口

- `create_order(symbol, side, order_type, quantity, price=None, ...)` - 创建订单
- `replace_order(order_id, quantity=None, price=None)` - 改单
- `cancel_order(order_id)` - 取消订单
- `cancel_all_orders(symbol=None)` - 批量取消订单
- `get_open_orders(symbol=None)` - 获取活跃订单
- `get_order_history(symbol=None, start_time=None, end_time=None, limit=100)` - 获取历史订单

#### 仓位接口

- `get_positions(symbol=None) -> List[Position]` - 获取仓位列表
- `set_leverage(symbol, leverage)` - 设置杠杆
- `set_margin_mode(symbol, margin_mode)` - 切换保证金模式

#### 便利方法

- `buy_market(symbol, quantity, reduce_only=False)` - 市价买入
- `sell_market(symbol, quantity, reduce_only=False)` - 市价卖出
- `buy_limit(symbol, quantity, price, ...)` - 限价买入
- `sell_limit(symbol, quantity, price, ...)` - 限价卖出

#### WebSocket接口

- `ws_connect_public() -> bool` - 连接公开WebSocket
- `ws_connect_private() -> bool` - 连接私有WebSocket
- `ws_subscribe_ticker(symbols, callback=None)` - 订阅行情
- `ws_subscribe_kline(symbols, interval, callback=None)` - 订阅K线
- `ws_subscribe_orderbook(symbols, callback=None)` - 订阅深度
- `ws_subscribe_trade(symbols, callback=None)` - 订阅交易
- `ws_subscribe_order(symbols=None, callback=None)` - 订阅订单更新
- `ws_subscribe_position(symbols=None, callback=None)` - 订阅仓位更新
- `ws_subscribe_wallet(callback=None)` - 订阅余额更新
- `ws_get_message(is_private=False, timeout=1.0)` - 获取WebSocket消息

## 数据模型

所有API响应都转换为typed dataclass对象，提供完整的类型检查：

```python
@dataclass
class Ticker:
    symbol: str
    last_price: float
    bid_price: float
    ask_price: float
    high_price: Optional[float] = None
    low_price: Optional[float] = None
    volume: Optional[float] = None
    timestamp: Optional[int] = None

@dataclass
class Order:
    order_id: str
    symbol: str
    order_type: str
    side: str
    price: float
    quantity: float
    filled_quantity: float
    status: str
    # ... 更多字段

@dataclass
class Position:
    symbol: str
    side: str
    quantity: float
    entry_price: float
    current_price: float
    leverage: int = 1
    margin: float = 0
    # ... 更多字段
```

## 枚举类型

便利的枚举定义了所有可用的参数值：

```python
from easicoin_api import OrderSide, OrderType, KlineInterval, MarginMode

# 订单方向
OrderSide.BUY, OrderSide.SELL

# 订单类型
OrderType.MARKET, OrderType.LIMIT

# K线间隔
KlineInterval.MIN_1, KlineInterval.MIN_5, KlineInterval.HOUR_1, KlineInterval.DAY_1

# 保证金模式
MarginMode.ISOLATED, MarginMode.CROSS
```

## 错误处理

完整的异常层级提供精细的错误处理：

```python
from easicoin_api import (
    EasicoinException,
    APIError,
    AuthenticationError,
    RateLimitError,
    InvalidParameterError,
    NetworkError,
    TimeoutError,
)

try:
    order = client.create_order("BTCUSDT", "buy", "limit", 0.1, 30000)
except AuthenticationError as e:
    print(f"认证失败: {e}")
except RateLimitError as e:
    print(f"请求过于频繁: {e}")
except InvalidParameterError as e:
    print(f"参数错误: {e}")
except EasicoinException as e:
    print(f"API错误: {e}")
```

## 配置和日志

### 配置限流

```python
from easicoin_api import EasicoinAPI

# 设置每秒最多10个请求
client = EasicoinAPI(
    api_key="...",
    api_secret="...",
    rate_limit=10,  # 每秒请求数
)
```

### 启用日志

```python
from easicoin_api import setup_logging
import logging

# 设置日志级别为DEBUG
setup_logging(level=logging.DEBUG, log_file="easicoin.log")

client = EasicoinAPI(api_key="...", api_secret="...")
```

## 示例代码

查看 `examples/` 目录下的完整示例：

1. **example_public_data.py** - 公开行情数据获取
2. **example_private_api.py** - 私有接口使用（账户、订单、仓位）
3. **example_websocket.py** - WebSocket实时数据订阅

运行示例：

```bash
python examples/example_public_data.py
python examples/example_private_api.py
python examples/example_websocket.py
```

## 项目结构

```
easicoin_api/
├── __init__.py           # 包初始化，导出主类和常用对象
├── client.py             # 主客户端类 (EasicoinAPI)
├── rest.py               # REST API客户端 (RESTClient)
├── websocket.py          # WebSocket客户端 (WebSocketClient)
├── auth.py               # 认证和签名模块
├── models.py             # 数据模型 (dataclass)
├── enums.py              # 枚举类型定义
├── errors.py             # 异常类定义
├── utils.py              # 工具函数 (限流、时间戳等)
└── examples/
    ├── example_public_data.py   # 公开行情示例
    ├── example_private_api.py   # 私有API示例
    └── example_websocket.py     # WebSocket示例
```

## API认证说明

### 签名算法（HMAC-SHA256）

根据Easicoin最新API文档，签名生成方式如下：

```
待签名字符串 = timestamp + api_key + recv_window + (GET: queryString 或 POST: JSON body)
签名 = HMAC-SHA256(secret, 待签名字符串) -> 十六进制(小写)

请求头:
- Access-Key: API密钥
- Access-Sign: 签名结果
- Access-Timestamp: 时间戳(毫秒, UTC)
- Recv-Window: 接收窗口(毫秒, 默认5000)
- Content-Type: application/json
```

该库已自动处理所有签名逻辑，用户无需手动操作。

### WebSocket认证

私有WebSocket连接会在建立后自动进行认证，使用相同的HMAC-SHA256算法。

## 限制和注意事项

1. **API调用限制**：默认每秒10个请求，可通过`rate_limit`参数调整
2. **时间同步**：确保本地系统时间与服务器时间差异不超过1秒
3. **WebSocket心跳**：默认30秒发送一次ping帧
4. **重连机制**：断开连接时自动尝试重连（最多5次）

## 常见问题

### 1. 认证失败

**问题**: `AuthenticationError: Signature generation failed`

**解决**:
- 检查API密钥和密钥对是否正确
- 确保系统时间准确（与UTC对齐）
- 检查网络连接

### 2. WebSocket连接失败

**问题**: `WebSocketError: Connection refused`

**解决**:
- 检查网络连接
- 确保没有防火墙阻止WebSocket连接
- 检查api_key和api_secret是否正确（私有连接）

### 3. 请求超时

**问题**: `TimeoutError: Request failed`

**解决**:
- 增加timeout参数: `EasicoinAPI(..., timeout=60)`
- 检查网络连接
- 降低rate_limit以减少并发请求

## 贡献

欢迎提交issue和pull request！

## 许可证

MIT License

## 支持

- 官网: https://www.easicoin.io
- 帮助中心: https://easicoin.zendesk.com/hc/zh-cn
- API文档: https://www.easicoin.io/api-doc/zh-CN/common/Info
---

**最后更新**: 2026年1月26日
