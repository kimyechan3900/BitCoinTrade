import time
import pyupbit
import datetime

access_key="MBYNWE0iBq0KCvj0fU93s9ZJDkro763R1M9ciOuk"
secret_key="IeXwk81Q59LSYoEBGtqWlGLrDxuq13rkgUqJN0oe"

upbit=pyupbit.Upbit(access_key,secret_key)

def get_plussell_target(ticker):
    df=pyupbit.get_ohlcv(ticker)
    yesterday=df.iloc[-2]

    target=yesterday['close']*1.14# 10%익절
    return target

def get_minussell_target(ticker):
    df=pyupbit.get_ohlcv(ticker)
    yesterday=df.iloc[-2]
    target=yesterday['close']
    return target
def get_target_price(ticker):# 목표가 설정
    df = pyupbit.get_ohlcv(ticker)
    yesterday = df.iloc[-2]
 
    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    target = today_open + (yesterday_high - yesterday_low) * 0.6
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


TF=False #매수 매도 기준
now = datetime.datetime.now()
mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
target_price = get_target_price("KRW-XRP")

while True:
   now = datetime.datetime.now()
   print("Working...")
   if mid < now < mid + datetime.timedelta(seconds=10) : #12시 정각되었을때 알고리즘
       print("It's 12 o'clock right now. Let's start selling coin")
       target_price = get_target_price("KRW-XRP")
       mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
       ma5=get_yesterday_ma5("KRW-XRP")
       sell_crypto_currency("KRW-XRP")

   current_price = pyupbit.get_current_price("KRW-XRP")#현재가 얻어오기
   plussell_target_price=get_plussell_target("KRW-XRP")
   minussell_target_price=get_minussell_target("KRW-XRP")
   if(TF==True):
       print("TF is true")
       if((current_price>plussell_target_price) or (current_price<minussell_target_price)): #시가10%이상이거나 시가이하로 떨어지면 매도
            sell_crypto_currency("KRW-XRP")
            print("Sell Coin")
            TF=False
   if(current_price>target_price):
       buy_crypto_currency("KRW-XRP")
       print("Buy Coin")
       TF=True

   time.sleep(3)
