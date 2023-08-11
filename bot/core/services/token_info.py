import requests
import time

class Info:
    try:
        def __init__(self, sym):
            self.sym = sym
            self.url_price = 'https://fapi.binance.com/fapi/v1/ticker/price?symbol=' + self.sym
            self.price = requests.get(self.url_price)
            self.data_price = self.price.json()
            self.lastprice = self.data_price['price']
    except requests.exceptions.JSONDecodeError as err:
        time.sleep(2)