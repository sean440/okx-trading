# 代理设置
PROXIES = {
    'http': 'http://127.0.0.1:9910',  # 根据实际情况修改代理地址
    'https': 'http://127.0.0.1:9910'  # 根据实际情况修改代理地址
}

# API 配置
API_KEY = "your_api_key"      # 替换为你的 API Key
SECRET_KEY = "your_secret_key"  # 替换为你的 Secret Key
PASSPHRASE = "your_passphrase"  # 替换为你的 Passphrase

# 交易配置
TRADE_MODE = "1"  # 0: 实盘, 1: 模拟盘

# 常用交易对
SYMBOLS = {
    "BTC-USDT": "比特币",
    "ETH-USDT": "以太坊",
    "OKB-USDT": "OKB",
} 