from okx.api.account import Account
from okx.api.trade import Trade
from config import PROXIES, API_KEY, SECRET_KEY, PASSPHRASE, TRADE_MODE
import time
from datetime import datetime

class Trading:
    def __init__(self):
        """初始化交易类"""
        self.account = Account(
            key=API_KEY,
            secret=SECRET_KEY,
            passphrase=PASSPHRASE,
            flag=TRADE_MODE,
            proxies=PROXIES
        )
        self.trade = Trade(
            key=API_KEY,
            secret=SECRET_KEY,
            passphrase=PASSPHRASE,
            flag=TRADE_MODE,
            proxies=PROXIES
        )

    def get_balance(self):
        """获取账户余额"""
        try:
            result = self.account.get_balance()
            return result
        except Exception as e:
            print(f"获取账户余额失败: {e}")
            return None

    def place_order(self, symbol, side, order_type, size, price=None):
        """下单
        
        Args:
            symbol: 交易对
            side: 买卖方向，buy/sell
            order_type: 订单类型，market/limit
            size: 交易数量
            price: 限价单价格，市价单不需要
        """
        try:
            params = {
                'instId': symbol,
                'tdMode': 'cash',  # 现货交易
                'side': side,
                'ordType': order_type,
                'sz': str(size)
            }
            
            if order_type == 'limit':
                params['px'] = str(price)
            
            result = self.trade.set_order(**params)
            return result
        except Exception as e:
            print(f"下单失败: {e}")
            return None

    def cancel_order(self, symbol, order_id):
        """撤销订单"""
        try:
            result = self.trade.set_cancel_order(instId=symbol, ordId=order_id)
            return result
        except Exception as e:
            print(f"撤销订单失败: {e}")
            return None

    def get_orders(self, symbol):
        """获取当前订单"""
        try:
            result = self.trade.get_orders_pending(instId=symbol)
            return result
        except Exception as e:
            print(f"获取订单失败: {e}")
            return None

    def print_balance(self):
        """打印账户余额"""
        result = self.get_balance()
        if result and result.get('code') == '0':
            print("\n=== 账户余额 ===")
            for balance in result['data'][0]['details']:
                if float(balance['availBal']) > 0:
                    print(f"币种: {balance['ccy']}")
                    print(f"可用余额: {balance['availBal']}")
                    print(f"冻结余额: {balance['frozenBal']}")
                    print(f"总余额: {balance['cashBal']}")
                    print("------------------------")
        else:
            print("获取账户余额失败")

    def print_orders(self, symbol):
        """打印订单信息"""
        result = self.get_orders(symbol)
        if result and result.get('code') == '0':
            print(f"\n=== {symbol} 当前订单 ===")
            for order in result['data']:
                print(f"订单ID: {order['ordId']}")
                print(f"订单类型: {order['ordType']}")
                print(f"买卖方向: {order['side']}")
                print(f"价格: {order['px']}")
                print(f"数量: {order['sz']}")
                print(f"状态: {order['state']}")
                print(f"创建时间: {datetime.fromtimestamp(int(order['cTime'])/1000).strftime('%Y-%m-%d %H:%M:%S')}")
                print("------------------------")
        else:
            print("获取订单失败") 