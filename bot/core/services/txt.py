import json
import os
import time

from .balances import balance
from .base import *

def create_txt():
    def createTxtFile(txt_file):
        try:
            f = open(txt_file, 'r')
        except FileNotFoundError as err:
            with open(txt_file, 'w') as fw:
                pass

    # Создаем папку "my_txt"
    if not os.path.exists("my_txt"):
        os.mkdir("my_txt")
    # Создаем файлы под запрос пользователя о позах-----------------------------------------------------------------------------
    createTxtFile('my_txt/request_pos_a.txt')
    createTxtFile('my_txt/request_pos_b.txt')
    createTxtFile('my_txt/posA.txt')
    createTxtFile('my_txt/posB.txt')
    createTxtFile('my_txt/pnlpair_A.txt')
    createTxtFile('my_txt/pnlpair_B.txt')
    createTxtFile('my_txt/equity.txt')

    # Создаем файлы для оповещения усреднения сделок-----------------------------------------------------------------------------
    createTxtFile('my_txt/double_pos.txt')

    # Создаем файлы для оповещения закрытия сделок-----------------------------------------------------------------------------
    createTxtFile('my_txt/close_pos.txt')

    # Создаем файлы для оповещения закрытия сделок
    createTxtFile('my_txt/close_pos_pair_A.txt')
    createTxtFile('my_txt/close_pos_pair_B.txt')

    # Создаем файлы для оповещения закрытия сделок
    createTxtFile('my_txt/close_pos_dist.txt')

    # Создаем файлы для оповещения закрытия сделок
    createTxtFile('my_txt/close_pos_hedje.txt')

    # Создаем текстовые файлы для статистики размера прибылей и убытков
    for txt in pair_txt_list:
        createTxtFile(f'my_txt/{txt}')


# возврат текстового файла от символа в паре________________________________________________________________________
def checkSym(symb):
    if symb == 'BTCUSDT':
        return 'BTCETH.txt'

    if symb == 'UNIUSDT':
        return 'UNIAAVE.txt'

    if symb == 'BCHUSDT':
        return 'BCHETC.txt'

    if symb == 'XRPUSDT':
        return 'XRPBNB.txt'

    if symb == 'ADAUSDT':
        return 'ADADOT.txt'

    if symb == 'LINKUSDT':
        return 'LINKXLM.txt'

    if symb == 'LTCUSDT':
        return 'LTCVET.txt'

    if symb == 'DOGEUSDT':
        return 'DOGEATOM.txt'


# Добавялем запись о новой позе по паре и записываем прибыль по новой позе в файл
def writeNewPosPnl(txt):
    try:
        with open(txt, 'r') as fr:
            max_loss_list = json.load(fr)
    except json.decoder.JSONDecodeError as err:
        max_loss_list = [{'number_pos': 0, 'max_loss': "0"}]
    with open(txt, 'w') as fw:
        max_loss_list.append({'number_pos': max_loss_list[-1]['number_pos'] + 1, 'max_loss': "0"})
        json.dump(max_loss_list, fw)


def write_equity(txt_file):
    # проверяем время последнего изменения файла
    if os.path.exists(txt_file):
        mod_time = os.path.getmtime(txt_file)
        current_time = time.time()
        if current_time - mod_time < 3600:
            return  # если прошло менее часа, выходим из функции

    # обновляем массив в файле
    with open(txt_file, 'r') as r:
        equity_list = json.load(r)
    equity_list.append(balance)
    with open(txt_file, 'w') as f:
        json.dump(equity_list, f)
