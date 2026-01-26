"""
Easicoin API 示例 - 公共行情数据

演示如何获取公开的市场数据（无需API密钥）
"""

from easicoin_api import EasicoinAPI, RESTClient


def example_get_instruments():
    """获取所有交易对信息"""
    print("\n=== 获取交易对信息 ===")
    client = RESTClient()  # 公开数据不需要密钥
    
    instruments = client.get_instruments()
    print(f"总共 {len(instruments)} 个交易对")
    
    # 显示前5个
    for inst in instruments[:5]:
        print(f"  {inst.symbol}: "
              f"价格精度={inst.price_precision}, "
              f"数量精度={inst.quantity_precision}, "
              f"杠杆={inst.leverage}x")


def example_get_ticker():
    """获取行情数据"""
    print("\n=== 获取行情数据 ===")
    client = RESTClient()
    
    symbol = "BTCUSDT"
    ticker = client.get_ticker(symbol)
    
    print(f"{symbol}:")
    print(f"  最新价: ${ticker.last_price}")
    print(f"  买价: ${ticker.bid_price}")
    print(f"  卖价: ${ticker.ask_price}")
    if ticker.high_price:
        print(f"  24h最高: ${ticker.high_price}")
        print(f"  24h最低: ${ticker.low_price}")
    if ticker.volume:
        print(f"  24h成交量: {ticker.volume} BTC")


def example_get_orderbook():
    """获取深度数据"""
    print("\n=== 获取深度数据 ===")
    client = RESTClient()
    
    symbol = "BTCUSDT"
    orderbook = client.get_orderbook(symbol, limit=5)
    
    print(f"{symbol} 深度 (前5档):")
    print(f"  买单:")
    for price, qty in orderbook.bids[:5]:
        print(f"    ${price} x {qty}")
    print(f"  卖单:")
    for price, qty in orderbook.asks[:5]:
        print(f"    ${price} x {qty}")


def example_get_klines():
    """获取K线数据"""
    print("\n=== 获取K线数据 ===")
    client = RESTClient()
    
    symbol = "BTCUSDT"
    interval = "1h"
    
    klines = client.get_klines(symbol, interval, limit=5)
    
    print(f"{symbol} {interval} K线 (最新5根):")
    for kline in klines[-5:]:
        print(f"  时间: {kline.timestamp}, "
              f"开:{kline.open:.2f}, "
              f"高:{kline.high:.2f}, "
              f"低:{kline.low:.2f}, "
              f"收:{kline.close:.2f}, "
              f"量:{kline.volume:.2f}")


def example_get_funding_rate():
    """获取资金费率历史"""
    print("\n=== 获取资金费率历史 ===")
    client = RESTClient()
    
    symbol = "BTCUSDT"
    funding_rates = client.get_funding_rate_history(symbol, limit=5)
    
    print(f"{symbol} 资金费率历史 (最新5条):")
    for fr in funding_rates[-5:]:
        print(f"  时间: {fr.funding_timestamp}, "
              f"费率: {fr.funding_rate * 100:.4f}%, "
              f"下一费率: {fr.next_funding_rate * 100:.4f}%")


if __name__ == "__main__":
    print("=" * 60)
    print("Easicoin API 示例 - 公共行情数据")
    print("=" * 60)
    
    try:
        example_get_instruments()
        example_get_ticker()
        example_get_orderbook()
        example_get_klines()
        example_get_funding_rate()
        
        print("\n" + "=" * 60)
        print("所有示例执行完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
