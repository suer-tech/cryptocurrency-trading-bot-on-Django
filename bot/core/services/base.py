from core.services.api_keys import api_key, secret_key

from binance.client import Client
from binance.um_futures import UMFutures

import numpy as np
import json


index = ['BTCUSDT', 'ETHUSDT', 'UNIUSDT', 'AAVEUSDT', 'BCHUSDT', 'ETCUSDT', 'XRPUSDT', 'BNBUSDT',
                 'ADAUSDT', 'DOTUSDT', 'LINKUSDT', 'XLMUSDT', 'LTCUSDT', 'VETUSDT', 'DOGEUSDT', 'ATOMUSDT']

pair_txt_list = ['BTCETH.txt', 'UNIAAVE.txt', 'BCHETC.txt', 'XRPBNB.txt', 'ADADOT.txt', 'LINKXLM.txt', 'LTCVET.txt', 'DOGEATOM.txt']


index_a = []
index_b = []

btceth_proc = 50
alt_proc = 50

lever_btc_eth = 30
lever = 10
# -----------------------------------------------------------------------------------------------------
um_futures_client = UMFutures(key=api_key, secret=secret_key)
client = Client(api_key, secret_key)


def divisionsAB(a, b, division):

    for cryptos in index:
        side = a
        if (index.index(cryptos) + 10) % 2 != 0:
            side = b
        sides = {
            'sym': cryptos,
            'side': side
        }
        division.append(sides)

def create_profitA_list():
    # проверяем  есть ли данные по предыдущим прибылям, если нет создадим новые массивы
    try:
        with open('my_txt/profitA.txt', 'r') as fr:
            profitA_list = json.load(fr)
    except json.decoder.JSONDecodeError as err:
        profitA_list = [{'number_pos': 0, 'max_profit': "0"}]
    except FileNotFoundError as err:
        with open('my_txt/profitA.txt', 'w') as fw:
            profitA_list = [{'number_pos': 0, 'max_profit': "0"}]
            json.dump(profitA_list, fw)
    return profitA_list

def create_profitB_list():
    try:
        with open('my_txt/profitB.txt', 'r') as fr:
            profitB_list = json.load(fr)
    except json.decoder.JSONDecodeError as err:
        profitB_list = [{'number_pos': 0, 'max_profit': "0"}]
    except FileNotFoundError as err:
        with open('my_txt/profitB.txt', 'w') as fw:
            profitB_list = [{'number_pos': 0, 'max_profit': "0"}]
            json.dump(profitB_list, fw)
    return profitB_list

def create_equity_list():
    # проверяем  есть ли данные по предыдущим equity, если нет создадим новые массивы
    try:
        with open('my_txt/equity.txt', 'r') as fr:
            equity_list = json.load(fr)
    except json.decoder.JSONDecodeError as err:
        with open('my_txt/equity.txt', 'w') as fw:
            equity_list = [40]
            json.dump(equity_list, fw)
    except FileNotFoundError as err:
        with open('my_txt/equity.txt', 'w') as fw:
            equity_list = [40]
            json.dump(equity_list, fw)
    return equity_list

def create_lossA_list():
    # проверяем  есть ли данные по предыдущим убыткам, если нет создадим новые массивы
    try:
        with open('my_txt/lossA.txt', 'r') as fr:
            lossA_list = json.load(fr)
    except json.decoder.JSONDecodeError as err:
        lossA_list = [{'number_pos': 0, 'max_loss': "0"}]
    except FileNotFoundError as err:
        with open('my_txt/lossA.txt', 'w') as fw:
            pass
        lossA_list = [{'number_pos': 0, 'max_loss': "0"}]
    return lossA_list

def create_lossB_list():
    try:
        with open('my_txt/lossB.txt', 'r') as fr:
            lossB_list = json.load(fr)
    except json.decoder.JSONDecodeError as err:
        lossB_list = [{'number_pos': 0, 'max_loss': "0"}]
    except FileNotFoundError as err:
        with open('my_txt/lossB.txt', 'w') as fw:
            pass
        lossB_list = [{'number_pos': 0, 'max_loss': "0"}]
    return lossB_list