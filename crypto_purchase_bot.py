import json
import hmac
import hashlib
import time
import requests
import base64
from requests.auth import AuthBase
from datetime import datetime
import config

#get config variables
API_KEY = config.API_KEY
API_SECRET = config.API_SECRET
API_PASS = config.API_PASS

bitcoin_buy = config.bitcoin_buy
ethereum_buy = config.ethereum_buy
cardano_buy = config.cardano_buy
algorand_buy = config.algorand_buy

bitcoin_buy_amount = config.bitcoin_buy_amount
ethereum_buy_amount = config.ethereum_buy_amount
cardano_buy_amount = config.cardano_buy_amount
algorand_buy_amount = config.algorand_buy_amount

buy_times = config.buy_times

# Create custom authentication for Exchange
class CoinbaseExchangeAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        message = timestamp + request.method.upper() + request.path_url + (str(request.body) or '')
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message.encode('utf-8'), hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest()).decode()

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request

api_url = 'https://api.pro.coinbase.com/'

last_day = datetime.now().day - 1
_buy_times = buy_times[:]

print("Bot runnning...")
print("Current day: {}".format(last_day))
print("Purchasing will start on: {}".format((last_day + 1)) + " at hour " + str(_buy_times[0]))

while True:
    now = datetime.now()
    buy = False
    
    #print('\r{0}:{1}'.format(now.hour, now.minute, now.second), end="\r")

    if now.day != last_day and now.hour in _buy_times:   
        _buy_times.remove(now.hour)
        buy = True
        
        if len(_buy_times) == 0:
            last_day = now.day
            _buy_times = buy_times[:]
            print("Day completed. Next buy is at {} at hour {}".format(last_day + 1, _buy_times[0]))
    
    if buy:

        #buy stuff
        auth = CoinbaseExchangeAuth(API_KEY, API_SECRET, API_PASS)

        if bitcoin_buy:
            order = {
                'type' : 'market',
                'side': 'buy',
                'product_id': 'BTC-USD',
                'funds': bitcoin_buy_amount,
            }

            r = requests.post(api_url + 'orders', json=order, auth=auth)
            print(r.json())
            print('-'*100)
            print('')

        if ethereum_buy:
            order = {
                'type' : 'market',
                'side': 'buy',
                'product_id': 'ETH-USD',
                'funds': ethereum_buy_amount,
            }

            r = requests.post(api_url + 'orders', json=order, auth=auth)
            print(r.json())
            print('-'*100)
            print('')
            
        if cardano_buy:
            order = {
                'type' : 'market',
                'side': 'buy',
                'product_id': 'ADA-USD',
                'funds': cardano_buy_amount,
            }

            r = requests.post(api_url + 'orders', json=order, auth=auth)
            print(r.json())
            print('-'*100)
            print('')
            
        if algorand_buy:
            order = {
                'type' : 'market',
                'side': 'buy',
                'product_id': 'ALGO-USD',
                'funds': algorand_buy_amount,
            }

            r = requests.post(api_url + 'orders', json=order, auth=auth)
            print(r.json())
            print('-'*100)
            print('')
    else:
        time.sleep(1)
