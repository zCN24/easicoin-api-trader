# 快速开始指南

## 1. 安装

### 方法 A: 使用 pip

```bash
pip install -r requirements.txt
```

### 方法 B: 开发安装

```bash
pip install -e .
```

## 2. 获取API密钥

1. 访问 https://www.easicoin.io
2. 登录你的账户
3. 进入账户设置 > API密钥管理
4. 创建新的API密钥对
5. 复制 API Key 和 API Secret

**安全提示**:
- 永远不要在代码中硬编码API密钥
- 使用环境变量存储敏感信息
- 限制API密钥的权限（仅勾选需要的权限）

## 3. 最简单的例子

### 获取BTC价格（无需密钥）

```python
from easicoin_api import RESTClient

client = RESTClient()
ticker = client.get_ticker("BTCUSDT")
print(f"BTC价格: ${ticker.last_price}")
```

### 下单（需要密钥）

```python
import os
from easicoin_api import EasicoinAPI

# 从环境变量读取密钥
api_key = os.getenv("EASICOIN_API_KEY")
api_secret = os.getenv("EASICOIN_API_SECRET")

client = EasicoinAPI(api_key=api_key, api_secret=api_secret)

# 限价买入
order = client.buy_limit("BTCUSDT", quantity=0.1, price=30000)
print(f"订单已创建: {order.order_id}")
```

## 4. 设置环境变量

### Windows

```cmd
set EASICOIN_API_KEY=your_api_key_here
set EASICOIN_API_SECRET=your_api_secret_here
```

### Linux / Mac

```bash
export EASICOIN_API_KEY=your_api_key_here
export EASICOIN_API_SECRET=your_api_secret_here
```

### Python代码中设置

```python
import os

os.environ["EASICOIN_API_KEY"] = "your_api_key_here"
os.environ["EASICOIN_API_SECRET"] = "your_api_secret_here"
```

## 5. 常见操作

### 查看账户余额

```python
from easicoin_api import EasicoinAPI

client = EasicoinAPI(api_key=api_key, api_secret=api_secret)

# 获取USDT余额
wallets = client.get_wallet()
if "USDT" in wallets:
    usdt = wallets["USDT"]
    print(f"USDT余额: {usdt.free}")
```

### 查看持仓

```python
# 获取所有持仓
positions = client.get_positions()
for pos in positions:
    print(f"{pos.symbol}: {pos.side} {pos.quantity} @ ${pos.entry_price}")
```

### 获取历史K线

```python
# 获取最近10个1小时K线
klines = client.get_klines("BTCUSDT", interval="1h", limit=10)
for kline in klines:
    print(f"收盘价: ${kline.close}, 成交量: {kline.volume}")
```

### 订阅实时行情

```python
# 连接WebSocket
client.ws_connect_public()

def on_ticker(msg):
    print(f"{msg.symbol}: ${msg.data['last_price']}")

# 订阅BTCUSDT行情
client.ws_subscribe_ticker(["BTCUSDT"], callback=on_ticker)

import time
time.sleep(10)  # 监听10秒

client.close()
```

## 6. 运行示例

本项目包含三个完整的示例文件：

### 示例1: 获取公开行情

```bash
python easicoin_api/examples/example_public_data.py
```

这个示例展示:
- 获取交易对信息
- 获取最新行情
- 获取深度数据
- 获取K线数据
- 获取资金费率

### 示例2: 私有操作

```bash
python easicoin_api/examples/example_private_api.py
```

这个示例展示:
- 获取账户余额
- 获取费率信息
- 下单（买/卖）
- 改单和取消订单
- 查看活跃订单和历史订单
- 管理仓位和杠杆

**需要修改**:
- 在代码中设置你的 `API_KEY` 和 `API_SECRET`

### 示例3: WebSocket实时数据

```bash
python easicoin_api/examples/example_websocket.py
```

这个示例展示:
- 连接公开WebSocket
- 订阅行情、K线、深度数据
- 使用回调处理实时数据
- 连接私有WebSocket（可选）
- 订阅订单和仓位更新

## 7. 错误处理

```python
from easicoin_api import EasicoinAPI, AuthenticationError, RateLimitError

client = EasicoinAPI(api_key=api_key, api_secret=api_secret)

try:
    order = client.create_order("BTCUSDT", "buy", "limit", 0.1, 30000)
except AuthenticationError as e:
    print(f"认证失败，请检查API密钥: {e}")
except RateLimitError as e:
    print(f"请求过于频繁，请稍候: {e}")
except Exception as e:
    print(f"其他错误: {e}")
```

## 8. 启用调试日志

```python
from easicoin_api import EasicoinAPI, setup_logging
import logging

# 启用DEBUG级别的日志
setup_logging(level=logging.DEBUG, log_file="easicoin_debug.log")

client = EasicoinAPI(api_key=api_key, api_secret=api_secret)
```

## 9. 下一步

- 📖 查看完整的 [API文档](README.md)
- 📁 浏览 [示例代码](easicoin_api/examples/)
- 🐛 报告问题或建议改进
- ⭐ 如果你觉得有用，请给个star

## 支持

遇到问题？

1. 检查 [FAQ](#faq) 部分
2. 查看 [API文档](README.md)
3. 查看示例代码
4. 联系Easicoin支持: https://easicoin.zendesk.com/hc/zh-cn

---

祝你交易顺利！🚀
