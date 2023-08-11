import json

import emoji

from core.services import pos_info
from core.services.balances import balance
from core.services.base import um_futures_client
from core.services.pnl_info import ProfitCalculator

from core.services.pos_info import positions

calculator = ProfitCalculator()

def close(sym, pos_side, amt):
    side = 'BUY'
    if pos_side == 'LONG':
        side = 'SELL'
    qt = abs(float(amt))
    params = {
        'symbol': sym,
        'side': side,
        'positionSide': pos_side,
        'type': 'MARKET',
        'quantity': str(qt),
    }
    um_futures_client.new_order(**params)
    print('Close')
    print("")

# Проверка наличия обеих поз в паре и закрытие при отсутствии одной из них
def checkPos(pair):
    check_one = 0
    check_two = 0
    positions = pos_info.positions()
    for pos_one in positions:
        if pos_one["symbol"] == pair[0]['sym'] and pos_one["positionSide"] == pair[0]['side']:
            check_one = 1
            one = pos_one
            break

    for pos_two in positions:
        if pos_two["symbol"] == pair[1]['sym'] and pos_two["positionSide"] == pair[1]['side']:
            check_two = 1
            two = pos_two
            break

    if check_one == 1 and check_two == 0:
        close(one['symbol'], one['positionSide'], one['positionAmt'])
        with open('my_txt/close_pos_hedje.txt', 'w') as fw:
            close_info = [emoji.emojize(':balance_scale:Закрытие хедж-позы'), '\n', one['symbol'], f' pnl: {float(one["unrealizedProfit"]) / balance * 100:.{2}f}%']
            close_info = ' '.join(close_info)
            json.dump(close_info, fw)

    if check_one == 0 and check_two == 1:
        close(two['symbol'], two['positionSide'], two['positionAmt'])
        with open('my_txt/close_pos_hedje.txt', 'w') as fw:
            close_info = [emoji.emojize(':balance_scale:Закрытие хедж-позы'), '\n', two['symbol'], f' pnl: {float(two["unrealizedProfit"]) / balance * 100:.{2}f}%']
            close_info = ' '.join(close_info)
            json.dump(close_info, fw)

        print("Закрытие одной из поз при отсутствии второй позы в паре")
        print(pair)
    return check_one + check_two

# Закрытие пары поз с прибылью______________________________________________________________
def closePair(pair, txt_file):
    positions = pos_info.positions()
    one_pos = "pos_two"
    two_pos = "postwo"
    for position in positions:
        if pair[0]['sym'] == position['symbol'] and pair[0]['side'] == position['positionSide']:
            close(position['symbol'], position['positionSide'], position['positionAmt'])
            one_pos = f"{position['symbol'][:-4]}[{position['positionSide']}]"
        if pair[1]['sym'] == position['symbol'] and pair[1]['side'] == position['positionSide']:
            close(position['symbol'], position['positionSide'], position['positionAmt'])
            two_pos = f"{position['symbol'][:-4]}[{position['positionSide']}]"
    with open(txt_file, 'w') as fw:
        close_info = [emoji.emojize(':money_bag:Частичное закрытие с профитом'), '\n', '\n', one_pos, '-', two_pos, '\n', f'pnl: {calculator.pnlPair(pair):.{2}f}%']
        close_info = ' '.join(close_info)
        json.dump(close_info, fw)
        print("Частичное закрытие с профитом")

def checkDistance(posa_x):
    global pos_distance_avrg
    pos_distance_list = []
    positions = pos_info.positions()
    for p in positions:
        pos_distance_list.append(p)
    print('')
    print('pos_distance_list')
    print(pos_distance_list)
    print('posa_x')
    print(posa_x)
    print('')
    pos_distance_list.remove(posa_x)
    pos_distance_avrg_list = []
    for posts in positions:
        if posts['initialMargin'] != '0':
            # print('Монета и дистанция')
            # print(token['symbol'])
            distance = abs(calculator.pnlPos(posts))
            # print('Дистанция')
            # print(distance)
            # print('')
            pos_distance_avrg_list.append(distance)
    if len(pos_distance_avrg_list) > 2:
        pos_distance_avrg = sum(pos_distance_avrg_list) / len(pos_distance_avrg_list)
    if len(pos_distance_avrg_list) == 1:
        pos_distance_avrg = distance
    if len(pos_distance_avrg_list) == 0:
        pos_distance_avrg = abs(calculator.pnlPos(posa_x))
    # print('СРЕДНЯЯ ДИСТАНЦИЯ СПИСОК')
    # print(pos_distance_avrg_list)
    # print('СРЕДНЯЯ ДИСТАНЦИЯ')
    # print(pos_distance_avrg)
    # print('')
    return pos_distance_avrg

