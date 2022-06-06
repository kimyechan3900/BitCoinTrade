import time
import pyupbit
import datetime

access_key="MBYNWE0iBq0KCvj0fU93s9ZJDkro763R1M9ciOuk"
secret_key="IeXwk81Q59LSYoEBGtqWlGLrDxuq13rkgUqJN0oe"

upbit=pyupbit.Upbit(access_key,secret_key)

def get_plussell_target(ticker):
    df=pyupbit.get_ohlcv(ticker)
    yesterday=df.iloc[-2]

    today_open=yesterday['close']*1.1
    return today_open

def get_minussell_target(ticker):
    df=pyupbit.get_ohlcv(ticker)
    yesterday=df.iloc[-2]
    today_open=yesterday['close']
    return today_open
def get_target_price(ticker):# 목표가 설정
    df = pyupbit.get_ohlcv(ticker)
    yesterday = df.iloc[-2]
 
    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    target = today_open + (yesterday_high - yesterday_low) * 0.5
    return target

def buy_crypto_currency(ticker):#코인 매수
    krw = pyupbit.get_balance(ticker)[2]
    orderbook = pyupbit.get_orderbook(ticker)
    sell_price = orderbook['asks'][0]['price']   
    unit = krw/float(sell_price)
    upbit.buy_market_order(ticker, unit)

def sell_crypto_currency(ticker):#코인 매도
    unit = pyupbit.get_balance(ticker)[0]
    upbit.sell_market_order(ticker, unit)

def get_yesterday_ma5(ticker):#5일 이동평균선 
    df = pyupbit.get_ohlcv(ticker)
    close = df['close']
    ma = close.rolling(5).mean()
    return ma[-2]



now = datetime.datetime.now()
mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
target_price = get_target_price("KRW-BTC")

while True:
   now = datetime.datetime.now()
   if mid < now < mid + datetime.timedelta(seconds=10) : 
       print("정각입니다. 매도타임입니다.")
       target_price = get_target_price("KRW-BTC")
       mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
       ma5=get_yesterday_ma5("KRW-BTC")
       sell_crypto_currency("KRW-BTC")

   current_price = pyupbit.get_current_price("KRW-BTC")#목표가 계산 함수
   plussell_target_price=get_plussell_target("KRW-BTC")
   minussell_target_price=get_minussell_target("KRW-BTC")

   if((current_price>plussell_target_price) or (current_price<minussell_target_price)): #시가10%이상이거나 시가이하로 떨어지면 매도
    sell_crypto_currency("KRW-BTC")
   if(current_price>target_price):
    buy_crypto_currency("KRW-BTC")

   time.sleep(1)