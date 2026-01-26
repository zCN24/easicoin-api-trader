"""
Easicoin API Python 客户端库 - 完整项目索引

本文件提供项目的完整导览和快速参考。
"""

# =====================================================================
# 📑 文档导览
# =====================================================================

DOCUMENTATION = {
    "README.md": {
        "描述": "完整的API文档和使用说明",
        "内容": [
            "功能特性",
            "安装说明",
            "快速开始示例",
            "API文档（所有接口）",
            "数据模型说明",
            "枚举类型说明",
            "错误处理",
            "配置和日志",
            "常见问题"
        ],
        "适合": "全面理解库的功能和使用方法",
    },
    
    "QUICKSTART.md": {
        "描述": "快速开始指南",
        "内容": [
            "安装步骤",
            "获取API密钥",
            "最简单的例子",
            "环境变量配置",
            "常见操作",
            "运行示例代码",
            "错误处理",
            "启用日志",
        ],
        "适合": "初级用户快速上手",
    },
    
    "PROJECT_SUMMARY.md": {
        "描述": "项目总结和统计",
        "内容": [
            "项目结构",
            "模块说明",
            "实现的接口",
            "认证机制",
            "主要特性",
            "统计数据",
            "改进和特点",
            "已知限制",
            "未来计划"
        ],
        "适合": "了解项目的全面情况",
    },
    
    "config_example.py": {
        "描述": "配置文件示例",
        "内容": [
            "API密钥配置",
            "连接参数",
            "WebSocket参数",
            "日志配置",
            "交易默认参数",
            "监控告警参数",
            "使用示例"
        ],
        "适合": "自定义库的行为",
    },
}

# =====================================================================
# 📁 源代码文件导览
# =====================================================================

SOURCE_CODE = {
    "easicoin_api/__init__.py": {
        "描述": "包初始化和导出",
        "导出": [
            "EasicoinAPI (主客户端)",
            "RESTClient (REST客户端)",
            "WebSocketClient (WebSocket客户端)",
            "所有数据模型",
            "所有枚举类型",
            "所有异常类",
            "认证和工具类"
        ],
        "行数": 120,
    },
    
    "easicoin_api/client.py": {
        "描述": "主客户端类",
        "主类": "EasicoinAPI",
        "功能": [
            "统一管理REST和WebSocket",
            "公共市场数据接口",
            "账户和订单接口",
            "仓位管理接口",
            "WebSocket订阅接口",
            "便利交易方法"
        ],
        "行数": 350,
    },
    
    "easicoin_api/rest.py": {
        "描述": "REST API客户端",
        "主类": "RESTClient",
        "功能": [
            "HTTP请求处理",
            "自动签名和认证",
            "自动限流",
            "6个公开接口",
            "11个私有接口",
            "错误处理"
        ],
        "行数": 850,
    },
    
    "easicoin_api/websocket.py": {
        "描述": "WebSocket客户端",
        "主类": [
            "WebSocketClient (连接管理)",
            "AsyncMessageHandler (消息处理)"
        ],
        "功能": [
            "WebSocket连接管理",
            "认证机制",
            "订阅/取消订阅",
            "消息回调",
            "自动心跳",
            "断线重连",
            "异步消息处理"
        ],
        "行数": 500,
    },
    
    "easicoin_api/auth.py": {
        "描述": "认证和签名模块",
        "主类": [
            "Signature (签名生成和验证)",
            "AuthManager (认证管理)"
        ],
        "功能": [
            "HMAC-SHA256签名",
            "时间戳处理",
            "请求头生成",
            "WebSocket认证",
            "签名验证"
        ],
        "行数": 250,
    },
    
    "easicoin_api/models.py": {
        "描述": "数据模型",
        "数据类": [
            "Instrument (交易对)",
            "Ticker (行情)",
            "OrderBook (深度)",
            "Kline (K线)",
            "Trade (交易)",
            "FundingRate (资金费率)",
            "Order (订单)",
            "Position (仓位)",
            "Wallet (余额)",
            "FeeRate (费率)",
            "WebSocketMessage (WS消息)"
        ],
        "功能": [
            "完整的类型提示",
            "默认值处理",
            "数据转换函数"
        ],
        "行数": 450,
    },
    
    "easicoin_api/enums.py": {
        "描述": "枚举类型定义",
        "枚举类": [
            "OrderSide (买/卖)",
            "OrderType (市价/限价)",
            "OrderStatus (订单状态)",
            "PositionSide (多/空)",
            "MarginMode (逐仓/全仓)",
            "KlineInterval (K线间隔)",
            "TimeInForce (有效期)",
            "WebSocketChannel (频道)"
        ],
        "功能": [
            "类型安全的参数",
            "便利函数"
        ],
        "行数": 150,
    },
    
    "easicoin_api/errors.py": {
        "描述": "异常和错误处理",
        "异常类": [
            "EasicoinException (基类)",
            "APIError (API错误)",
            "AuthenticationError (认证失败)",
            "AuthorizationError (权限不足)",
            "RateLimitError (限流)",
            "BadRequestError (请求错误)",
            "NotFoundError (未找到)",
            "ServerError (服务器错误)",
            "NetworkError (网络错误)",
            "TimeoutError (超时)",
            "InvalidSignatureError (签名错误)",
            "InvalidParameterError (参数错误)",
            "WebSocketError (WS错误)",
            "WebSocketAuthenticationError (WS认证错误)"
        ],
        "功能": [
            "自动异常映射",
            "错误信息处理"
        ],
        "行数": 150,
    },
    
    "easicoin_api/utils.py": {
        "描述": "工具函数和工具类",
        "工具类": [
            "RateLimiter (令牌桶限流)"
        ],
        "工具函数": [
            "时间戳函数 (get_timestamp_ms, get_timestamp_us)",
            "参数处理 (clean_dict, build_query_string)",
            "验证函数 (is_valid_symbol, is_valid_price)",
            "数据函数 (merge_dicts, safe_get)",
            "日志配置 (setup_logging)"
        ],
        "行数": 350,
    },
}

# =====================================================================
# 📂 示例代码导览
# =====================================================================

EXAMPLES = {
    "example_public_data.py": {
        "描述": "公开行情数据示例",
        "需要": "不需要API密钥",
        "演示": [
            "获取交易对信息",
            "获取行情数据（ticker）",
            "获取深度数据（orderbook）",
            "获取K线数据",
            "获取资金费率历史"
        ],
        "运行": "python easicoin_api/examples/example_public_data.py",
    },
    
    "example_private_api.py": {
        "描述": "私有接口示例（账户、订单、仓位）",
        "需要": "API密钥和密钥对",
        "演示": [
            "获取账户余额",
            "获取费率信息",
            "下单（买入/卖出）",
            "改单和取消订单",
            "查询活跃和历史订单",
            "管理仓位（查看、设置杠杆、切换保证金模式）"
        ],
        "运行": "python easicoin_api/examples/example_private_api.py",
        "提示": "修改代码中的 API_KEY 和 API_SECRET"
    },
    
    "example_websocket.py": {
        "描述": "WebSocket实时数据订阅示例",
        "需要": "不需要密钥（公开）或需要密钥（私有）",
        "演示": [
            "连接公开WebSocket",
            "订阅行情数据（ticker）",
            "订阅K线数据（kline）",
            "订阅深度数据（orderbook）",
            "使用回调处理消息",
            "连接私有WebSocket",
            "订阅订单和仓位更新"
        ],
        "运行": "python easicoin_api/examples/example_websocket.py",
    },
}

# =====================================================================
# 🔧 配置和依赖
# =====================================================================

PROJECT_FILES = {
    "requirements.txt": {
        "描述": "项目依赖",
        "内容": [
            "requests>=2.28.0",
            "websocket-client>=1.0.0"
        ],
        "安装": "pip install -r requirements.txt"
    },
    
    "setup.py": {
        "描述": "包安装配置",
        "功能": [
            "包管理元数据",
            "依赖声明",
            "可选的开发依赖"
        ],
        "安装": "pip install -e ."
    },
    
    ".gitignore": {
        "描述": "Git忽略文件",
        "忽略": [
            "Python缓存文件",
            "虚拟环境",
            "配置文件",
            "日志文件",
            "IDE配置"
        ]
    },
}

# =====================================================================
# 🎯 快速参考
# =====================================================================

QUICK_REFERENCE = """
【基本使用】

1. 安装库:
   pip install -r requirements.txt

2. 导入和初始化:
   from easicoin_api import EasicoinAPI
   client = EasicoinAPI(api_key="...", api_secret="...")

3. 获取行情:
   ticker = client.get_ticker("BTCUSDT")
   print(f"BTC: ${ticker.last_price}")

4. 下单:
   order = client.buy_limit("BTCUSDT", quantity=0.1, price=30000)

5. WebSocket订阅:
   client.ws_connect_public()
   client.ws_subscribe_ticker(["BTCUSDT"], callback=lambda msg: print(msg))

【常见方法】

公开行情:
  - get_instruments()          获取所有交易对
  - get_ticker(symbol)         获取行情
  - get_orderbook(symbol)      获取深度
  - get_klines(symbol, interval)  获取K线
  - get_funding_rate_history() 获取资金费率

账户操作:
  - get_wallet()               获取余额
  - get_fee_rate()             获取费率
  - get_positions()            获取仓位

订单操作:
  - create_order()             创建订单
  - buy_limit() / sell_limit() 限价买/卖
  - buy_market() / sell_market() 市价买/卖
  - cancel_order()             取消订单
  - get_open_orders()          活跃订单
  - get_order_history()        历史订单

仓位管理:
  - set_leverage()             设置杠杆
  - set_margin_mode()          切换保证金模式

WebSocket:
  - ws_connect_public()        连接公开WS
  - ws_subscribe_ticker()      订阅行情
  - ws_subscribe_kline()       订阅K线
  - ws_subscribe_orderbook()   订阅深度

【异常处理】

try:
    order = client.create_order(...)
except AuthenticationError:
    print("认证失败")
except RateLimitError:
    print("请求过于频繁")
except APIError as e:
    print(f"API错误: {e}")

【日志配置】

from easicoin_api import setup_logging
import logging

setup_logging(level=logging.DEBUG, log_file="api.log")

【环境变量】

export EASICOIN_API_KEY=your_key
export EASICOIN_API_SECRET=your_secret
"""

# =====================================================================
# 📊 项目统计
# =====================================================================

STATISTICS = """
项目规模:
  • 核心代码: 4000+ 行
  • 文档: 2000+ 行
  • 示例: 400+ 行
  • 总计: 6400+ 行

导出接口:
  • 主类: 1 (EasicoinAPI)
  • REST客户端: 1 (RESTClient)
  • WebSocket客户端: 2 (WebSocketClient, AsyncMessageHandler)
  • 数据模型: 10
  • 异常类: 14
  • 枚举类型: 8
  • 工具类: 1 (RateLimiter)
  • 工具函数: 20+

API接口:
  • 公开接口: 6
  • 私有接口: 11
  • WebSocket频道: 7

支持:
  • Python版本: 3.8+
  • 操作系统: Windows, Linux, macOS
  • 依赖库: 2 (requests, websocket-client)
"""

# =====================================================================
# 🚀 开始使用
# =====================================================================

GETTING_STARTED = """
【第1步：安装】
  pip install -r requirements.txt

【第2步：获取API密钥】
  访问 https://www.easicoin.io
  账户设置 → API密钥管理 → 创建新密钥

【第3步：运行验证脚本】
  python verify_installation.py

【第4步：运行示例】
  python easicoin_api/examples/example_public_data.py

【第5步：查看文档】
  - README.md      (完整API文档)
  - QUICKSTART.md  (快速开始指南)
  - 示例代码       (实际用法)

【第6步：开始编码】
  from easicoin_api import EasicoinAPI
  
  client = EasicoinAPI(api_key="...", api_secret="...")
  
  # 获取价格
  ticker = client.get_ticker("BTCUSDT")
  print(f"BTC: ${ticker.last_price}")
"""

# =====================================================================
# 💡 提示和建议
# =====================================================================

TIPS_AND_TRICKS = """
【安全提示】
  ✓ 从不在代码中硬编码API密钥
  ✓ 使用环境变量存储敏感信息
  ✓ 限制API密钥的权限
  ✓ 定期轮换API密钥

【性能优化】
  ✓ 使用合适的rate_limit参数避免限流
  ✓ 批量查询而不是逐个查询
  ✓ WebSocket用于实时数据，REST用于查询

【错误处理】
  ✓ 总是使用try-except捕获异常
  ✓ 记录错误日志便于调试
  ✓ 实现重试机制（特别是网络错误）

【WebSocket使用】
  ✓ 使用回调处理消息
  ✓ 适当处理断线重连
  ✓ 监控消息队列大小

【调试技巧】
  ✓ 启用DEBUG日志: setup_logging(level=logging.DEBUG)
  ✓ 检查时间戳是否准确
  ✓ 验证API密钥和密钥对
  ✓ 查看详细的错误消息
"""

# =====================================================================
# 📞 获取帮助
# =====================================================================

SUPPORT = """
【文档】
  • README.md - 完整API文档
  • QUICKSTART.md - 快速开始
  • PROJECT_SUMMARY.md - 项目概览
  • 源代码注释 - 详细的docstring

【示例代码】
  • example_public_data.py - 公开行情
  • example_private_api.py - 私有操作
  • example_websocket.py - WebSocket订阅

【官方资源】
  • 网站: https://www.easicoin.io
  • API文档: https://docs.easicoin.io
  • 帮助中心: https://easicoin.zendesk.com/hc/zh-cn
  • Telegram: https://t.me/EasiCoin_ZH
  • Discord: https://discord.gg/c8guxZzDCu

【常见问题】
  • 认证失败？检查API密钥和系统时间
  • WebSocket连接失败？检查网络和防火墙
  • 请求超时？增加timeout参数或降低rate_limit
"""

# =====================================================================
# 主函数
# =====================================================================

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print(" " * 20 + "Easicoin API Python 客户端库")
    print(" " * 25 + "完整项目索引")
    print("=" * 80)
    
    print("\n【📑 文档导览】")
    for doc, info in DOCUMENTATION.items():
        print(f"\n  {doc}")
        print(f"    描述: {info['描述']}")
        print(f"    适合: {info['适合']}")
    
    print("\n\n【📁 源代码文件（核心）】")
    for file, info in SOURCE_CODE.items():
        print(f"\n  {file}")
        print(f"    描述: {info['描述']}")
        if '主类' in info:
            if isinstance(info['主类'], list):
                print(f"    主类: {', '.join(info['主类'])}")
            else:
                print(f"    主类: {info['主类']}")
        print(f"    行数: {info['行数']}")
    
    print("\n\n【📂 示例代码】")
    for file, info in EXAMPLES.items():
        print(f"\n  {file}")
        print(f"    描述: {info['描述']}")
        print(f"    运行: {info['运行']}")
    
    print("\n\n【🎯 快速参考】")
    print(QUICK_REFERENCE)
    
    print("\n\n【🚀 开始使用】")
    print(GETTING_STARTED)
    
    print("\n\n【💡 提示和建议】")
    print(TIPS_AND_TRICKS)
    
    print("\n\n【📞 获取帮助】")
    print(SUPPORT)
    
    print("\n" + "=" * 80)
    print("项目已准备好，祝你使用愉快！🎉")
    print("=" * 80 + "\n")
