import pandas as pd
import numpy as np
import talib
import okx.PublicData as PublicData
import okx.MarketData as MarketData
from flask import Flask, jsonify


flag = "0"  # 实盘:0 , 模拟盘：1
# 将 PublicAPI 改为 PublicData
publicDataAPI = PublicData.PublicAPI(flag=flag)
marketDataAPI = MarketData.MarketAPI(flag=flag)


# 获取交易产品基础信息
result = marketDataAPI.get_mark_price_candlesticks(
    instId="BTC-USD-SWAP",
    bar = "1D"
)

# 根据result返回的数据构建DataFrame
data = pd.DataFrame(result['data'], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

# 将'close'列转换为浮点数类型
data['close'] = data['close'].astype(float)

# 计算指标
close = data['close']
data['SMA_20'] = talib.SMA(close, timeperiod=20)
data['RSI_14'] = talib.RSI(close, timeperiod=14)
data['MACD'], data['MACD_Signal'], data['MACD_Hist'] = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
data['UpperBand'], data['MiddleBand'], data['LowerBand'] = talib.BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)

# 确保所有用于比较的列都是浮点数类型
numeric_columns = ['close', 'RSI_14', 'UpperBand', 'LowerBand']
for col in numeric_columns:
    data[col] = data[col].astype(float)

# 定义买入/卖出信号
data['Buy_Signal'] = np.where((data['RSI_14'] < 30) & (data['close'] < data['LowerBand']), 1, 0)
data['Sell_Signal'] = np.where((data['RSI_14'] > 70) & (data['close'] > data['UpperBand']), -1, 0)

# 综合买入/卖出信号
data['Signal'] = data['Buy_Signal'] + data['Sell_Signal']

# 创建Flask应用
app = Flask(__name__)

# 定义GET请求的/test接口
@app.route('/', methods=['GET'])
def test():
    # 将DataFrame转换为字典，然后返回JSON格式的响应数据
    return jsonify(data.to_dict(orient='records'))

# 运行应用，绑定到端口8080
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
