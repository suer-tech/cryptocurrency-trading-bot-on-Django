import json

from core.services.balances import balance
from core.services.base import um_futures_client, index_a, index_b


def posAB(pos_a, pos_txt_file):
    from core.services.pnl_info import ProfitCalculator
    calculator = ProfitCalculator()
    bal = balance()
    a_item = []
    # создаем позы А файл
    with open(pos_txt_file, 'w') as fw:
        pass
    for a in pos_a:
        one = f'{a["symbol"][:-4]}: {a["positionSide"]}'
        a_item.append(one)
        a_item.append('\n')
        two = f'TVH_distance: {calculator.pnlPos(a):.{2}f}%'
        a_item.append(two)
        a_item.append('\n')
        three = f'pnl: {float(a["unrealizedProfit"]) / bal * 100:.{2}f}%'
        a_item.append(three)
        a_item.append('\n')
        a_item.append('\n')
    if len(a_item) == 0:
        a_item = "Нет открытых позиций"
    a_item = ''.join(a_item)
     # записываем позы А в файл
    with open(pos_txt_file, 'w') as fw:
        json.dump(a_item, fw)
    return a_item

def positions():
    response = um_futures_client.account(recvWindow=50000)
    positions = response['positions']
    pos = []
    for cr in positions:
        if cr['initialMargin'] != '0':
            pos.append(cr)
    return pos

def create_array_pos_a():
    pos = positions()
    pos_a = []
    for open_pos in pos:
        for a_pos in index_a:
            if open_pos['symbol'] == a_pos['sym'] and open_pos['positionSide'] == a_pos['side']:
                pos_a.append(open_pos)
    return pos_a

def create_array_pos_b():
    pos = positions()
    pos_b = []
    for open_pos in pos:
        for b_pos in index_b:
            if open_pos['symbol'] == b_pos['sym'] and open_pos['positionSide'] == b_pos['side']:
                pos_b.append(open_pos)
    return pos_b