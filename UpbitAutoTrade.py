import time
import pyupbit
import datetime

access_key="MBYNWE0iBq0KCvj0fU93s9ZJDkro763R1M9ciOuk"
secret_key="IeXwk81Q59LSYoEBGtqWlGLrDxuq13rkgUqJN0oe"

upbit=pyupbit.Upbit(access_key,secret_key)

def get_target_price(ticker):# 목표가 설정
    df = pyupbit.get_ohlcv(ticker)
    yesterday = df.iloc[-2]
 
    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    target = today_open + (yesterday_high - yesterday_low) *0.6
    return target

def get_balance(ticker): #잔고 조회
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def buy_crypto_currency(ticker):#코인 매수
    krw = upbit.get_balance(ticker)[2]
    orderbook = pyupbit.get_orderbook(ticker)
    sell_price = orderbook['asks'][0]['price']   
    unit = krw/float(sell_price)
    upbit.buy_market_order(ticker, unit)

def sell_crypto_currency(ticker):#코인 매도
    unit = upbit.get_balance(ticker)[0]
    upbit.sell_market_order(ticker, unit)



now = datetime.datetime.now()
mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
target_price = get_target_price("KRW-XRP")
while True:
   now = datetime.datetime.now()
   print(mid)
   print("Working...")
   XRPbalance=get_balance("XRP")
   print(target_price)
   print(XRPbalance)
   TF=False
   if(XRPbalance>1):
       TF=True
   else:
       TF=False
    

   if ((mid < now < mid + datetime.timedelta(seconds=10)) and TF==True) : #12시 정각되었을때 알고리즘
       print("It's 12 o'clock right now. Let's start selling coin")
       target_price = get_target_price("KRW-XRP")
       mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
       if(XRPbalance>1):
            upbit.sell_market_order("KRW-XRP",XRPbalance*0.9995)
            print("Sell Coin")
            TF=False
       #sell_crypto_currency("KRW-XRP")
       #TF=False

   current_price = pyupbit.get_current_price("KRW-XRP")#현재가 얻어오기

   if(TF==True):
       print("TF is true")
       if((current_price>(target_price*1.1)) or (current_price<(target_price*0.97))): #수익 10% 익절,손익 -3% 손절
           if(XRPbalance>1):
               upbit.sell_market_order("KRW-XRP",XRPbalance*0.9995)
               print("Sell Coin")
               print(now)
               TF=False

   if(current_price>target_price):  #매수
       KRWbalance=get_balance("KRW")
       if (KRWbalance>5000):
           upbit.buy_market_order("KRW-XRP",KRWbalance*0.9995)
           print("Buy Coin")
           TF=True
       #buy_crypto_currency("KRW-XRP")
   time.sleep(3)
