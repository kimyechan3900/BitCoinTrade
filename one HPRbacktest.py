import pyupbit
import numpy as np

df = pyupbit.get_ohlcv("KRW-XRP",count=205)

df['ma5'] = df['close'].rolling(window=5).mean().shift(1)
df['range'] = (df['high'] - df['low']) * 0.6
df['target'] = df['open'] + df['range'].shift(1)
#df['bull'] = df['open'] > df['ma5']
#df['bull'] where 첫줄

fee = 0.00032
df['ror'] = np.where((df['high'] > df['target']),
                  df['close'] / df['target'] - fee,
                  1)
print(df)

df['hpr'] = df['ror'].cumprod()
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
print("MDD: ", df['dd'].max(),"%")
print("HPR: ", df['hpr'][-2])