from okx.api.market import Market
from config import PROXIES, API_KEY, SECRET_KEY, PASSPHRASE, TRADE_MODE
import json
from datetime import datetime, timedelta
import pandas as pd
import time
import os

class MarketData:
    def __init__(self):
        """初始化市场数据类"""
        self.market = Market(
            key=API_KEY,
            secret=SECRET_KEY,
            passphrase=PASSPHRASE,
            flag=TRADE_MODE,
            proxies=PROXIES
        )
        # 设置历史数据存储路径
        self.data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "historical_data")
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

    def get_ticker(self, symbol):
        """获取单个交易对的最新行情
        
        Args:
            symbol: 交易对，例如 "BTC-USDT"
            
        Returns:
            dict: 包含行情数据的字典
        """
        try:
            result = self.market.get_ticker(instId=symbol)
            return result
        except Exception as e:
            print(f"获取 {symbol} 行情失败: {e}")
            return None

    def get_tickers(self, inst_type="SPOT"):
        """获取所有交易对的最新行情
        
        Args:
            inst_type: 产品类型，例如 "SPOT"（现货）, "SWAP"（永续）等
            
        Returns:
            dict: 包含所有交易对行情的字典
        """
        try:
            result = self.market.get_tickers(instType=inst_type)
            return result
        except Exception as e:
            print(f"获取行情列表失败: {e}")
            return None

    def get_kline(self, symbol, bar='1m', limit='100'):
        """获取K线数据
        
        Args:
            symbol: 交易对
            bar: K线周期，可选值：1m, 3m, 5m, 15m, 30m, 1H, 2H, 4H, 6H, 12H, 1D, 1W, 1M
            limit: 获取的K线数量，最大1000
        """
        try:
            result = self.market.get_candles(
                instId=symbol,
                bar=bar,
                limit=limit
            )
            return result
        except Exception as e:
            print(f"获取K线数据失败: {e}")
            return None

    def get_history_data(self, symbol, days, bar='1m'):
        """获取历史数据
        
        Args:
            symbol: 交易对
            days: 获取的天数
            bar: K线周期
        """
        try:
            # 使用当前时间
            end_time = datetime.now()
            start_time = end_time - timedelta(days=days)
            
            print(f"获取历史数据: {symbol}, 从 {start_time} 到 {end_time}")
            
            # 使用分页方式获取数据
            all_data = []
            limit = '1000'  # 每次获取1000条数据
            
            # 使用after参数进行分页
            after = None
            while True:
                result = self.market.get_candles(
                    instId=symbol,
                    bar=bar,
                    limit=limit,
                    after=after
                )
                
                if not result or result.get("code") != "0" or not result.get("data"):
                    break
                
                data = result["data"]
                all_data.extend(data)
                print(f"已获取 {len(all_data)} 条历史数据")
                
                # 检查是否已经获取到足够的数据
                if len(data) < 1000:  # 如果返回的数据少于1000条，说明已经到达最早的数据
                    break
                    
                # 获取最后一条数据的时间戳作为下一次请求的after参数
                after = data[-1][0]  # 时间戳在第一个位置
                
                # 检查是否已经获取到指定天数之前的数据
                oldest_time = datetime.fromtimestamp(int(data[-1][0])/1000)
                if oldest_time < start_time:
                    break
                    
                # 添加请求间隔，避免触发频率限制
                time.sleep(0.5)
            
            return {"code": "0", "data": all_data}
                
        except Exception as e:
            print(f"获取历史数据失败: {e}")
            return None

    def print_market_data(self, symbol):
        """打印市场数据
        
        Args:
            symbol: 交易对，例如 "BTC-USDT"
        """
        result = self.get_ticker(symbol)
        if result and result.get("code") == "0":
            data = result["data"][0]
            print(f"\n=== {symbol} 市场数据 ===")
            print(f"最新价格: {data['last']}")
            print(f"24h最高: {data['high24h']}")
            print(f"24h最低: {data['low24h']}")
            print(f"24h成交量: {data['vol24h']}")
            print(f"卖一价: {data['askPx']}")
            print(f"买一价: {data['bidPx']}")
        else:
            print(f"获取 {symbol} 市场数据失败")

    def print_kline_data(self, symbol, bar='1m', limit='5'):
        """打印K线数据
        
        Args:
            symbol: 交易对
            bar: K线周期
            limit: 获取的K线数量
        """
        result = self.get_kline(symbol, bar, limit)
        if result and result.get("code") == "0":
            print(f"\n=== {symbol} K线数据 ({bar}) ===")
            for candle in result["data"]:
                ts = datetime.fromtimestamp(int(candle[0])/1000)
                print(f"时间: {ts}")
                print(f"开盘价: {candle[1]}")
                print(f"最高价: {candle[2]}")
                print(f"最低价: {candle[3]}")
                print(f"收盘价: {candle[4]}")
                print(f"成交量: {candle[5]}")
                print("------------------------")
        else:
            print(f"获取 {symbol} K线数据失败")

    def save_history_data(self, symbol, days, bar='1m'):
        """保存历史数据到CSV文件
        
        Args:
            symbol: 交易对
            days: 获取的天数
            bar: K线周期
        """
        result = self.get_history_data(symbol, days, bar)
        if result and result.get("code") == "0":
            # 构建文件名
            filename = os.path.join(self.data_path, f"{symbol.replace('-', '_')}_{bar}_{days}d.csv")
            
            # 转换数据为DataFrame
            data = []
            for candle in result["data"]:
                try:
                    ts = datetime.fromtimestamp(int(candle[0])/1000)
                    data.append({
                        "timestamp": ts,
                        "open": float(candle[1]),
                        "high": float(candle[2]),
                        "low": float(candle[3]),
                        "close": float(candle[4]),
                        "volume": float(candle[5])
                    })
                except (ValueError, IndexError) as e:
                    print(f"数据转换错误: {e}")
                    continue
            
            if data:
                df = pd.DataFrame(data)
                try:
                    df.to_csv(filename, index=False, encoding='utf-8')
                    print(f"历史数据已保存到: {filename}")
                    print(f"共保存 {len(data)} 条记录")
                except Exception as e:
                    print(f"保存文件失败: {e}")
            else:
                print("没有有效数据可保存")
        else:
            print(f"获取 {symbol} 历史数据失败") 