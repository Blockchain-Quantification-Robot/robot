import ccxt
print("ccxt版本：")
print(ccxt.exchanges)  # 输出ccxt支持的所有交易所

# exchange = ccxt.binance()  # 创建Binance交易所实例
# markets = exchange.load_markets()  # 获取Binance所有交易对信息
# print(markets)  # 打印交易对信息

# ticker = exchange.fetch_ticker('BTC/USDT')  # 获取 BTC/USDT 的最新市场数据
# print(ticker)  # 打印价格信息

# # 定义交易对符号
# symbol = 'BTC/USDT'
# # 定义时间帧，例如1小时
# timeframe = '1h'
# # 定义K线条数，例如100条
# limit = 100

# K_data = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
# print(K_data)
apikey = "这里根据申请api时的内容填写"
secretkey = "这里根据申请api时的内容填写"
password="这里根据申请api时的内容填写"

okx=ccxt.okx({
    'apiKey':apikey,
    'secret':secretkey,
    'password':password
})

#由于现在直接访问okex会被墙，需要通过代理的方式访问，若是国外服务器则不需要下面的这几行代码
okx.proxies={
    'http': 'socks5://127.0.0.1:10801',
    'https': 'socks5://127.0.0.1:10801',
}
order_symbol='ETH/USDT'
ETH_info=okx.fetch_ticker(order_symbol)
print(ETH_info)