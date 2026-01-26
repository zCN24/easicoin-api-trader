#!/usr/bin/env python
"""
Easicoin API 客户端库 - 安装验证脚本

运行此脚本以验证库是否正确安装和配置
"""

import sys
import importlib
from pathlib import Path


def print_header(text):
    """打印标题"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def check_python_version():
    """检查Python版本"""
    print_header("检查 Python 版本")
    
    version = sys.version_info
    version_str = f"Python {version.major}.{version.minor}.{version.micro}"
    
    print(f"✓ 当前版本: {version_str}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"✗ 错误: 需要 Python 3.8 或更高版本")
        return False
    
    print(f"✓ 版本符合要求")
    return True


def check_dependencies():
    """检查依赖包"""
    print_header("检查依赖包")
    
    dependencies = {
        "requests": "REST API支持",
        "websocket": "WebSocket支持",
    }
    
    all_ok = True
    for package, description in dependencies.items():
        try:
            mod = importlib.import_module(package)
            version = getattr(mod, "__version__", "未知版本")
            print(f"✓ {package:20} {description:20} ({version})")
        except ImportError:
            print(f"✗ {package:20} {description:20} (未安装)")
            all_ok = False
    
    if not all_ok:
        print("\n提示: 运行以下命令安装缺失的依赖:")
        print("  pip install -r requirements.txt")
    
    return all_ok


def check_package_structure():
    """检查包结构"""
    print_header("检查包结构")
    
    required_files = [
        "easicoin_api/__init__.py",
        "easicoin_api/client.py",
        "easicoin_api/rest.py",
        "easicoin_api/websocket.py",
        "easicoin_api/auth.py",
        "easicoin_api/models.py",
        "easicoin_api/enums.py",
        "easicoin_api/errors.py",
        "easicoin_api/utils.py",
    ]
    
    all_ok = True
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} (未找到)")
            all_ok = False
    
    return all_ok


def check_imports():
    """检查导入"""
    print_header("检查导入")
    
    imports = [
        ("easicoin_api", "主包"),
        ("easicoin_api.client", "主客户端模块"),
        ("easicoin_api.rest", "REST客户端模块"),
        ("easicoin_api.websocket", "WebSocket模块"),
        ("easicoin_api.auth", "认证模块"),
        ("easicoin_api.models", "数据模型"),
        ("easicoin_api.enums", "枚举类型"),
        ("easicoin_api.errors", "异常类"),
        ("easicoin_api.utils", "工具函数"),
    ]
    
    all_ok = True
    for module_name, description in imports:
        try:
            module = importlib.import_module(module_name)
            print(f"✓ {module_name:30} {description}")
        except Exception as e:
            print(f"✗ {module_name:30} {description} ({str(e)})")
            all_ok = False
    
    return all_ok


def check_main_classes():
    """检查主要类"""
    print_header("检查主要类")
    
    try:
        from easicoin_api import (
            EasicoinAPI,
            RESTClient,
            WebSocketClient,
            Signature,
            AuthManager,
        )
        
        classes = [
            (EasicoinAPI, "主API客户端"),
            (RESTClient, "REST客户端"),
            (WebSocketClient, "WebSocket客户端"),
            (Signature, "签名生成器"),
            (AuthManager, "认证管理器"),
        ]
        
        for cls, description in classes:
            print(f"✓ {cls.__name__:20} {description}")
        
        return True
    except Exception as e:
        print(f"✗ 导入主要类失败: {e}")
        return False


def check_data_models():
    """检查数据模型"""
    print_header("检查数据模型")
    
    try:
        from easicoin_api import (
            Ticker,
            Order,
            Position,
            Wallet,
            OrderBook,
            Kline,
        )
        
        models = [
            (Ticker, "行情数据"),
            (Order, "订单数据"),
            (Position, "仓位数据"),
            (Wallet, "钱包/余额"),
            (OrderBook, "深度数据"),
            (Kline, "K线数据"),
        ]
        
        for model, description in models:
            print(f"✓ {model.__name__:20} {description}")
        
        return True
    except Exception as e:
        print(f"✗ 导入数据模型失败: {e}")
        return False


def check_enums():
    """检查枚举"""
    print_header("检查枚举")
    
    try:
        from easicoin_api import (
            OrderSide,
            OrderType,
            KlineInterval,
            MarginMode,
        )
        
        enums = [
            (OrderSide, "订单方向"),
            (OrderType, "订单类型"),
            (KlineInterval, "K线间隔"),
            (MarginMode, "保证金模式"),
        ]
        
        for enum, description in enums:
            values = [e.value for e in enum]
            print(f"✓ {enum.__name__:20} {description:20} ({len(values)} 个值)")
        
        return True
    except Exception as e:
        print(f"✗ 导入枚举失败: {e}")
        return False


def check_exceptions():
    """检查异常类"""
    print_header("检查异常类")
    
    try:
        from easicoin_api import (
            EasicoinException,
            APIError,
            AuthenticationError,
            RateLimitError,
            NetworkError,
            WebSocketError,
        )
        
        exceptions = [
            EasicoinException,
            APIError,
            AuthenticationError,
            RateLimitError,
            NetworkError,
            WebSocketError,
        ]
        
        for exc in exceptions:
            print(f"✓ {exc.__name__}")
        
        return True
    except Exception as e:
        print(f"✗ 导入异常类失败: {e}")
        return False


def run_simple_test():
    """运行简单功能测试"""
    print_header("运行功能测试")
    
    try:
        # 测试时间戳生成
        from easicoin_api.utils import get_timestamp_ms, get_timestamp_us
        
        ts_ms = get_timestamp_ms()
        ts_us = get_timestamp_us()
        
        print(f"✓ 时间戳生成:")
        print(f"  - 毫秒: {ts_ms}")
        print(f"  - 微秒: {ts_us}")
        
        # 测试签名生成
        from easicoin_api.auth import Signature
        
        sig = Signature.generate_signature(
            timestamp=ts_ms,
            api_key="test_key",
            api_secret="test_secret",
            recv_window=5000,
            method="GET",
            query_string="",
        )
        
        print(f"\n✓ 签名生成:")
        print(f"  - 长度: {len(sig)}")
        print(f"  - 格式: HMAC-SHA256 (十六进制)")
        
        # 测试枚举
        from easicoin_api import OrderSide, OrderType
        
        print(f"\n✓ 枚举验证:")
        print(f"  - 买入: {OrderSide.BUY.value}")
        print(f"  - 卖出: {OrderSide.SELL.value}")
        print(f"  - 市价: {OrderType.MARKET.value}")
        print(f"  - 限价: {OrderType.LIMIT.value}")
        
        # 测试错误处理
        from easicoin_api.errors import InvalidParameterError
        
        try:
            raise InvalidParameterError("测试错误")
        except InvalidParameterError as e:
            print(f"\n✓ 异常处理:")
            print(f"  - 异常类型: {type(e).__name__}")
            print(f"  - 异常消息: {str(e)}")
        
        return True
    except Exception as e:
        print(f"✗ 功能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def show_summary(results):
    """显示总结"""
    print_header("验证总结")
    
    checks = [
        ("Python版本检查", results[0]),
        ("依赖包检查", results[1]),
        ("包结构检查", results[2]),
        ("导入检查", results[3]),
        ("主类检查", results[4]),
        ("数据模型检查", results[5]),
        ("枚举检查", results[6]),
        ("异常类检查", results[7]),
        ("功能测试", results[8]),
    ]
    
    passed = sum(1 for _, result in checks if result)
    total = len(checks)
    
    print(f"\n通过: {passed}/{total}\n")
    
    for name, result in checks:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"  {status:8} {name}")
    
    print()
    
    if all(results):
        print("🎉 所有检查都通过了！")
        print("\n接下来:")
        print("  1. 查看 QUICKSTART.md 了解如何使用")
        print("  2. 运行示例代码: python easicoin_api/examples/example_public_data.py")
        print("  3. 设置你的API密钥并进行实际操作")
        return True
    else:
        print("⚠️  有些检查未通过，请检查错误消息")
        print("\n获取帮助:")
        print("  - 查看 README.md")
        print("  - 查看 QUICKSTART.md")
        print("  - 重新安装: pip install -r requirements.txt")
        return False


def main():
    """主函数"""
    print("\n")
    print(" " * 70)
    print("  Easicoin API Python 客户端库 - 安装验证")
    print(" " * 70)
    
    results = [
        check_python_version(),
        check_dependencies(),
        check_package_structure(),
        check_imports(),
        check_main_classes(),
        check_data_models(),
        check_enums(),
        check_exceptions(),
        run_simple_test(),
    ]
    
    success = show_summary(results)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
