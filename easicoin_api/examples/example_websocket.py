"""
Easicoin API 示例 - WebSocket 实时数据

演示如何连接WebSocket并订阅实时行情、深度、交易等数据
"""

import time
from easicoin_api import EasicoinAPI, WebSocketClient


def example_public_websocket():
    """公开WebSocket示例（无需认证）"""
    print("\n=== 公开WebSocket示例 ===")
    
    # 创建公开WebSocket客户端
    ws = WebSocketClient(is_private=False)
    
    # 定义回调函数
    def on_ticker(msg):
        data = msg.data
        print(f"[TICKER] {msg.symbol}: "
              f"价格=${data.get('last_price', 'N/A')}, "
              f"买=${data.get('bid_price', 'N/A')}, "
              f"卖=${data.get('ask_price', 'N/A')}")
    
    def on_kline(msg):
        data = msg.data
        print(f"[KLINE] {msg.symbol}: "
              f"开=${data.get('open', 'N/A')}, "
              f"收=${data.get('close', 'N/A')}, "
              f"量={data.get('volume', 'N/A')}")
    
    def on_orderbook(msg):
        data = msg.data
        bids = data.get('bids', [])
        asks = data.get('asks', [])
        if bids and asks:
            print(f"[ORDERBOOK] {msg.symbol}: "
                  f"买[0]=${bids[0][0]}x{bids[0][1]}, "
                  f"卖[0]=${asks[0][0]}x{asks[0][1]}")
    
    try:
        # 连接
        print("连接到公开WebSocket...")
        if not ws.connect():
            print("连接失败！")
            return
        
        time.sleep(2)  # 等待连接建立
        
        # 订阅行情数据
        print("\n订阅行情数据...")
        ws.subscribe("ticker", symbols=["BTCUSDT", "ETHUSDT"], callback=on_ticker)
        
        # 订阅K线数据（1小时）
        print("订阅K线数据...")
        ws.subscribe("kline_1h", symbols=["BTCUSDT"], callback=on_kline)
        
        # 订阅深度数据
        print("订阅深度数据...")
        ws.subscribe("orderbook", symbols=["BTCUSDT"], callback=on_orderbook)
        
        # 接收数据
        print("\n接收实时数据 (10秒)...")
        start_time = time.time()
        while time.time() - start_time < 10:
            msg = ws.get_message(timeout=1.0)
            # 消息已通过回调处理
            time.sleep(0.1)
        
        # 取消订阅
        print("\n取消订阅...")
        ws.unsubscribe("ticker", symbols=["BTCUSDT"])
        
    except Exception as e:
        print(f"错误: {e}")
    finally:
        ws.disconnect()
        print("断开连接")


def example_easyticoin_api_websocket():
    """使用EasicoinAPI客户端的WebSocket示例"""
    print("\n=== 使用EasicoinAPI的WebSocket示例 ===")
    
    client = EasicoinAPI(api_key="", api_secret="")
    
    def on_ticker_update(msg):
        print(f"[TICKER UPDATE] {msg.channel} - {msg.symbol}")
        print(f"  数据: {msg.data}")
    
    try:
        # 连接公开WebSocket
        print("连接公开WebSocket...")
        if not client.ws_connect_public():
            print("连接失败！")
            return
        
        time.sleep(1)
        
        # 订阅行情
        print("订阅BTCUSDT行情...")
        client.ws_subscribe_ticker(["BTCUSDT"], callback=on_ticker_update)
        
        # 接收数据
        print("\n接收实时数据 (5秒)...")
        start_time = time.time()
        while time.time() - start_time < 5:
            msg = client.ws_get_message(is_private=False, timeout=1.0)
            if msg:
                print(f"收到消息: {msg.channel} - {msg.symbol}")
        
    except Exception as e:
        print(f"错误: {e}")
    finally:
        client.close()
        print("断开连接")


def example_private_websocket():
    """私有WebSocket示例（需要认证）"""
    print("\n=== 私有WebSocket示例 ===")
    
    # *** 重要: 替换为你的实际API密钥和密钥对 ***
    API_KEY = "your_api_key_here"
    API_SECRET = "your_api_secret_here"
    
    if API_KEY == "your_api_key_here":
        print("错误: 请设置你的API密钥和密钥对！")
        return
    
    ws = WebSocketClient(
        api_key=API_KEY,
        api_secret=API_SECRET,
        is_private=True
    )
    
    def on_order_update(msg):
        data = msg.data
        print(f"[ORDER] {data.get('symbol')}: "
              f"ID={data.get('order_id')}, "
              f"状态={data.get('status')}, "
              f"已成交={data.get('filled_quantity')}")
    
    def on_position_update(msg):
        data = msg.data
        print(f"[POSITION] {data.get('symbol')}: "
              f"方向={data.get('side')}, "
              f"数量={data.get('quantity')}, "
              f"盈亏=${data.get('unrealised_pnl')}")
    
    def on_wallet_update(msg):
        data = msg.data
        print(f"[WALLET] 余额更新:")
        for currency, balance in data.items():
            print(f"  {currency}: 可用={balance.get('free')}, 冻结={balance.get('locked')}")
    
    try:
        # 连接
        print("连接到私有WebSocket...")
        if not ws.connect():
            print("连接失败！")
            return
        
        time.sleep(2)  # 等待连接和认证
        
        if not ws.is_authenticated:
            print("认证失败！")
            return
        
        print("认证成功！")
        
        # 订阅私有频道
        print("\n订阅私有频道...")
        ws.subscribe("order", callback=on_order_update)
        ws.subscribe("position", callback=on_position_update)
        ws.subscribe("wallet", callback=on_wallet_update)
        
        # 接收数据
        print("\n接收私有数据 (15秒)...")
        start_time = time.time()
        while time.time() - start_time < 15:
            msg = ws.get_message(timeout=1.0)
            # 消息已通过回调处理
            time.sleep(0.1)
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        ws.disconnect()
        print("断开连接")


def main():
    """主函数"""
    print("=" * 60)
    print("Easicoin API 示例 - WebSocket 实时数据")
    print("=" * 60)
    
    # 1. 公开WebSocket示例
    try:
        example_public_websocket()
    except Exception as e:
        print(f"公开WebSocket示例错误: {e}")
    
    time.sleep(2)
    
    # 2. 使用EasicoinAPI的WebSocket示例
    try:
        example_easyticoin_api_websocket()
    except Exception as e:
        print(f"EasicoinAPI WebSocket示例错误: {e}")
    
    time.sleep(2)
    
    # 3. 私有WebSocket示例（注释，需要真实API密钥）
    # try:
    #     example_private_websocket()
    # except Exception as e:
    #     print(f"私有WebSocket示例错误: {e}")
    
    print("\n" + "=" * 60)
    print("WebSocket示例完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
