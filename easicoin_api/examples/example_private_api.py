"""
Easicoin API 示例 - 私有接口（账户、订单、仓位）

演示如何进行账户操作、下单、查询仓位等（需要API密钥）
"""

from easicoin_api import EasicoinAPI, OrderSide, OrderType


def example_get_wallet(client: EasicoinAPI):
    """获取账户余额"""
    print("\n=== 获取账户余额 ===")
    
    wallets = client.get_wallet()
    
    print("账户余额:")
    for currency, wallet in sorted(wallets.items()):
        if wallet.total > 0:
            print(f"  {currency}:")
            print(f"    可用: {wallet.free}")
            print(f"    冻结: {wallet.locked}")
            print(f"    总计: {wallet.total}")


def example_get_fee_rate(client: EasicoinAPI):
    """获取费率信息"""
    print("\n=== 获取费率信息 ===")
    
    # 全局费率
    global_fee = client.get_fee_rate()
    print(f"全局费率:")
    print(f"  Maker: {global_fee.maker_fee * 100:.4f}%")
    print(f"  Taker: {global_fee.taker_fee * 100:.4f}%")
    
    # 单个交易对费率
    symbol_fee = client.get_fee_rate("BTCUSDT")
    print(f"\n{symbol_fee.symbol} 费率:")
    print(f"  Maker: {symbol_fee.maker_fee * 100:.4f}%")
    print(f"  Taker: {symbol_fee.taker_fee * 100:.4f}%")


def example_place_orders(client: EasicoinAPI):
    """下单示例"""
    print("\n=== 下单示例 ===")
    
    symbol = "BTCUSDT"
    
    try:
        # 示例1: 限价买入
        print(f"\n1. 限价买入 {symbol}")
        order1 = client.buy_limit(
            symbol=symbol,
            quantity=0.001,
            price=35000,
            time_in_force="GTC",
        )
        print(f"  订单ID: {order1.order_id}")
        print(f"  状态: {order1.status}")
        print(f"  价格: ${order1.price}")
        print(f"  数量: {order1.quantity} BTC")
        
        # 示例2: 限价卖出
        print(f"\n2. 限价卖出 {symbol}")
        order2 = client.sell_limit(
            symbol=symbol,
            quantity=0.001,
            price=40000,
            time_in_force="GTC",
        )
        print(f"  订单ID: {order2.order_id}")
        print(f"  状态: {order2.status}")
        print(f"  价格: ${order2.price}")
        print(f"  数量: {order2.quantity} BTC")
        
        # 示例3: 市价单（需要真实资金，这里仅演示）
        print(f"\n3. 市价买入示例（已注释，避免意外交易）")
        # order3 = client.buy_market(symbol=symbol, quantity=0.001)
        
        return [order1, order2]
        
    except Exception as e:
        print(f"  下单失败: {e}")
        return []


def example_manage_orders(client: EasicoinAPI, orders: list):
    """管理订单（改单、取消）"""
    if not orders:
        print("\n=== 没有订单可操作 ===")
        return
    
    print("\n=== 管理订单 ===")
    
    # 改单
    if len(orders) > 0:
        order = orders[0]
        print(f"\n1. 改单示例")
        print(f"  原订单ID: {order.order_id}")
        try:
            # 改价格
            modified = client.replace_order(
                order_id=order.order_id,
                price=36000,  # 新价格
            )
            print(f"  新价格: ${modified.price}")
        except Exception as e:
            print(f"  改单失败: {e}")
    
    # 获取活跃订单
    print(f"\n2. 查询活跃订单")
    try:
        open_orders = client.get_open_orders()
        print(f"  总计: {len(open_orders)} 个活跃订单")
        for order in open_orders[:5]:
            print(f"    {order.order_id}: {order.side} "
                  f"{order.quantity} @ ${order.price} ({order.status})")
    except Exception as e:
        print(f"  查询失败: {e}")
    
    # 获取历史订单
    print(f"\n3. 查询历史订单")
    try:
        history = client.get_order_history(limit=5)
        print(f"  最近5个订单:")
        for order in history[:5]:
            print(f"    {order.order_id}: {order.side} "
                  f"{order.quantity} @ ${order.price} ({order.status})")
    except Exception as e:
        print(f"  查询失败: {e}")
    
    # 取消订单
    if len(orders) > 0:
        order = orders[0]
        print(f"\n4. 取消订单示例")
        print(f"  订单ID: {order.order_id}")
        try:
            cancelled = client.cancel_order(order.order_id)
            print(f"  状态: {cancelled.status}")
        except Exception as e:
            print(f"  取消失败: {e}")


def example_positions(client: EasicoinAPI):
    """查看和管理仓位"""
    print("\n=== 仓位管理 ===")
    
    try:
        # 获取所有仓位
        positions = client.get_positions()
        print(f"\n1. 当前仓位 (总计: {len(positions)})")
        
        for pos in positions:
            if pos.quantity > 0:
                pnl_str = f"+${pos.unrealised_pnl:.2f}" if pos.unrealised_pnl and pos.unrealised_pnl > 0 else f"-${abs(pos.unrealised_pnl):.2f}" if pos.unrealised_pnl else "N/A"
                print(f"  {pos.symbol} ({pos.side}):")
                print(f"    数量: {pos.quantity}")
                print(f"    开仓价: ${pos.entry_price}")
                print(f"    当前价: ${pos.current_price}")
                print(f"    杠杆: {pos.leverage}x")
                print(f"    未实现盈亏: {pnl_str}")
        
        # 设置杠杆（示例）
        print(f"\n2. 设置杠杆示例")
        symbol = "BTCUSDT"
        try:
            result = client.set_leverage(symbol, leverage=10)
            print(f"  {symbol} 杠杆已设置为 10x")
        except Exception as e:
            print(f"  设置杠杆失败: {e}")
        
        # 切换保证金模式（示例）
        print(f"\n3. 切换保证金模式示例")
        try:
            result = client.set_margin_mode(symbol, margin_mode="isolated")
            print(f"  {symbol} 保证金模式已切换为逐仓")
        except Exception as e:
            print(f"  切换保证金模式失败: {e}")
            
    except Exception as e:
        print(f"  查询仓位失败: {e}")


def main():
    """主函数"""
    print("=" * 60)
    print("Easicoin API 示例 - 私有接口")
    print("=" * 60)
    
    # *** 重要: 替换为你的实际API密钥和密钥对 ***
    API_KEY = "your_api_key_here"
    API_SECRET = "your_api_secret_here"
    
    if API_KEY == "your_api_key_here":
        print("\n错误: 请在代码中设置你的API密钥和密钥对！")
        print("位置: API_KEY 和 API_SECRET 变量")
        return
    
    # 初始化客户端
    client = EasicoinAPI(api_key=API_KEY, api_secret=API_SECRET)
    
    try:
        # 1. 获取账户信息
        example_get_wallet(client)
        
        # 2. 获取费率信息
        example_get_fee_rate(client)
        
        # 3. 下单示例
        orders = example_place_orders(client)
        
        # 4. 管理订单
        example_manage_orders(client, orders)
        
        # 5. 查看和管理仓位
        example_positions(client)
        
        print("\n" + "=" * 60)
        print("所有示例执行完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        client.close()


if __name__ == "__main__":
    main()
