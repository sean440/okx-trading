from market_data import MarketData
from trading import Trading
from config import SYMBOLS
import time

def market_data_menu():
    """市场数据菜单"""
    market = MarketData()
    
    while True:
        print("\n=== 市场数据功能 ===")
        print("1. 获取实时行情")
        print("2. 获取K线数据")
        print("3. 获取并保存历史数据")
        print("4. 返回主菜单")
        
        choice = input("\n请选择功能: ")
        
        if choice == "1":
            symbol = input("请输入交易对 (例如: BTC-USDT): ")
            market.print_market_data(symbol)
            
        elif choice == "2":
            symbol = input("请输入交易对 (例如: BTC-USDT): ")
            bar = input("请输入K线周期 (例如: 1m, 5m, 15m, 1H, 4H, 1D): ")
            limit = input("请输入获取的K线数量: ")
            market.print_kline_data(symbol, bar, limit)
            
        elif choice == "3":
            symbol = input("请输入交易对 (例如: BTC-USDT): ")
            days = int(input("请输入获取的天数: "))
            bar = input("请输入K线周期 (例如: 1m, 5m, 15m, 1H, 4H, 1D): ")
            market.save_history_data(symbol, days, bar)
            
        elif choice == "4":
            break
            
        else:
            print("无效的选择，请重试")

def trading_menu():
    """交易功能菜单"""
    trading = Trading()
    while True:
        print("\n=== 交易功能 ===")
        print("1. 查看账户余额")
        print("2. 下单")
        print("3. 查看活跃订单")
        print("4. 取消订单")
        print("5. 返回主菜单")
        
        choice = input("\n请选择功能: ")
        
        if choice == '1':
            trading.print_balance()
        elif choice == '2':
            symbol = input("请输入交易对(例如: BTC-USDT): ")
            side = input("请输入买卖方向(buy/sell): ")
            order_type = input("请输入订单类型(market/limit): ")
            size = input("请输入交易数量: ")
            price = None
            if order_type == 'limit':
                price = input("请输入价格: ")
            trading.place_order(symbol, side, order_type, size, price)
        elif choice == '3':
            symbol = input("请输入交易对(例如: BTC-USDT): ")
            trading.print_orders(symbol)
        elif choice == '4':
            symbol = input("请输入交易对(例如: BTC-USDT): ")
            order_id = input("请输入订单ID: ")
            trading.cancel_order(symbol, order_id)
        elif choice == '5':
            break
        else:
            print("无效的选择，请重试")

def main():
    """主菜单"""
    while True:
        print("\n=== OKX交易程序 ===")
        print("1. 市场数据功能")
        print("2. 交易功能")
        print("3. 退出程序")
        
        choice = input("\n请选择功能: ")
        
        if choice == "1":
            market_data_menu()
        elif choice == "2":
            trading_menu()
        elif choice == "3":
            print("正在退出程序...")
            break
        else:
            print("无效的选择，请重试")

if __name__ == "__main__":
    main() 