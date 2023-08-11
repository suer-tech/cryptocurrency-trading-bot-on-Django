from core.services.token_info import Info

import ccxt

from .api_keys import *
from .balances import balance
from .base import index, lever_btc_eth, lever, btceth_proc, alt_proc, um_futures_client


# Задаем плечи-----------------------------------------------------------------------------
def leverg(index):
    for sym in index:
        if sym == 'BTCUSDT' or sym == 'ETHUSDT':
            leverage = lever_btc_eth
        else:
            leverage = lever

        sym_list = list(sym)
        sym_list.insert(-4, '/')
        sym = ''.join(sym_list)
        sym = str(sym)

        binance = ccxt.binance({
            "options": {"defaultType": "future"},
            "timeout": 30000,
            "apiKey": api_key,
            "secret": secret_key,
            "enableRateLimit": True,
        })

        binance.load_markets()  # load markets to get the market id from a unified symbol
        market = binance.markets[sym]
        binance.fapiPrivate_post_leverage({
            "symbol": market['id'],  # convert a unified CCXT symbol to an exchange-specific market id
            # "symbol": "BTCUSDT",  # same thing, note there's no slash in the exchange-specific id
            "leverage": leverage,
        })

def marja(sym):
    marj = (balance-balance/100*10)
    marj_ab = marj / 2
    marj_proc = marj_ab / 100
    sum_alt = len(index) - 2
    if sym == 'BTCUSDT' or sym == 'ETHUSDT':
        marj_btceth = marj_proc * btceth_proc
        marj_btceth = marj_btceth / 2
        marj_btceth = marj_btceth * lever_btc_eth
        return marj_btceth
    else:
        marj_alt = marj_proc * alt_proc
        marj_alt = marj_alt / sum_alt
        marj_alt = marj_alt * lever
        return marj_alt

def lots(sym):
    marj = marja(sym)
    price = Info(sym).lastprice
    print(sym)
    if sym == 'BTCUSDT' or sym == 'ETHUSDT':
        lot = f"{marj / float(price):.{3}f}"
        print(marj)

    elif sym == 'DOTUSDT' or sym == 'AAVEUSDT' or sym == 'XRPUSDT':
        lot = f"{marj / float(price):.{1}f}"
        print(marj)

    elif sym == 'ADAUSDT' or sym == 'UNIUSDT' or sym == 'XLMUSDT' or sym == 'VETUSDT' or sym == 'DOGEUSDT':
        lot = round(marj / float(price))
        print(marj)

    elif sym == 'LINKUSDT' or sym == 'BNBUSDT' or sym == 'ETCUSDT' or sym == 'ATOMUSDT':
        lot = f"{marj / float(price):.{2}f}"
        print(marj)

    elif sym == 'BCHUSDT' or sym == 'BNBUSDT' or sym == 'LTCUSDT':
        lot = f"{marj / float(price):.{3}f}"
        print(marj)

    return lot

def trade(sym, pos_side):
    side = 'SELL'
    if pos_side == "LONG":
        side = 'BUY'
    params = {
        'symbol': sym,
        'side': side,
        'positionSide': pos_side,
        'type': 'MARKET',
        'quantity': lots(sym),
    }
    um_futures_client.new_order(**params)