import json

from .base import index
from .open import lots, leverg, trade
from .pnl_info import ProfitCalculator

from .pos_info import create_array_pos_b, create_array_pos_a

calculator = ProfitCalculator()

def double(pos_ab, distance, number_double):
    pos_a = create_array_pos_a()
    pos_b = create_array_pos_b()
    txt = 'my_txt/pnlA.txt'
    if pos_ab == pos_b:
        txt = 'my_txt/pnlB.txt'
    n_double = number_double + 1
    btc_amt = None
    eth_amt = None
    if calculator.pnlAB(pos_ab, txt) < distance:
        for item in pos_ab:
            if item['symbol'] == 'BTCUSDT':
                btc_amt = float(item['positionAmt'])
            elif item['symbol'] == 'ETHUSDT':
                eth_amt = float(item['positionAmt'])
        lot_btc = float(lots("BTCUSDT")) * n_double / 1.3
        lot_eth = float(lots("ETHUSDT")) * n_double / 1.3
        # Проверяем усреднен ли лот в обеих монетах
        if abs(btc_amt) < lot_btc and abs(eth_amt) < lot_eth:
            for item in pos_ab:
                if item['symbol'] == 'BTCUSDT' or item['symbol'] == 'ETHUSDT':
                    # Задаём плечи-----------------------------------------------------------------------------
                    leverg(index)
                    # Усредняем позиции BTC и ETH
                    trade(item['symbol'], item['positionSide'])
                    # Записываем инфо для увеомления
                    with open('double_pos.txt', 'w') as fw:
                        double_info = f"Усреднение: {item['symbol']}, {item['positionSide']}"
                        json.dump(double_info, fw)
                    print('Усреднение обеих поз')
        # Проверяем усреднен ли лот в одной из монет
        elif abs(btc_amt) < lot_btc and abs(eth_amt) > lot_eth:
            for item in pos_ab:
                if item['symbol'] == 'BTCUSDT':
                    # Задаём плечи-----------------------------------------------------------------------------
                    leverg(index)
                    # Усредняем позиции BTC
                    trade(item['symbol'], item['positionSide'])
                    # Записываем инфо для увеомления
                    with open('double_pos.txt', 'w') as fw:
                        double_info = f"Усреднение: {item['symbol']}, {item['positionSide']}"
                        json.dump(double_info, fw)

        elif abs(btc_amt) > lot_btc and abs(eth_amt) < lot_eth:
            for item in pos_ab:
                if item['symbol'] == 'ETHUSDT':
                    # Задаём плечи-----------------------------------------------------------------------------
                    leverg(index)
                    # Усредняем позиции ETH
                    trade(item['symbol'], item['positionSide'])
                    # Записываем инфо для увеомления
                    with open('double_pos.txt', 'w') as fw:
                        double_info = f"Усреднение: {item['symbol']}, {item['positionSide']}"
                        json.dump(double_info, fw)
                    print('Усреднение ETH')