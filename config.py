# 代理设置
PROXIES = {
    'http': 'http://127.0.0.1:9910',
    'https': 'http://127.0.0.1:9910' # 迷雾通代理地址，如果你使用其他代理，填写其他代理地址
}

# API 配置
API_KEY = "your_api_key"  # 你的 API Key
SECRET_KEY = "your_secret_key"  # 你的 Secret Key
PASSPHRASE = "your_passphrase"  # 你的 Passphrase

# 交易配置
TRADE_MODE = "1"  # 0: 实盘, 1: 模拟盘

# 常用交易对
SYMBOLS = {
    "BTC-USDT": "比特币",
    "ETH-USDT": "以太坊",
    "OKB-USDT": "OKB",
} 