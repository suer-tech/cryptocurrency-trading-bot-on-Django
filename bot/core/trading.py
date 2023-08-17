import threading

import binance
from binance.client import Client
from binance.um_futures import UMFutures
import requests
import emoji
from colorama import Fore, Style
import datetime
import statistics

from urllib3.exceptions import ReadTimeoutError

from .services.base import *
from .services.balances import *
from .services.pnl_info import ProfitCalculator
from .services.txt import *
from .services.open import *
from .services.close import *
from .services.pnl_info import *
from .services.pos_info import *
from .services.token_info import *
from .services.double import *
from .services.pos_info import positions


class MyTrading(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        my_trading()

start_trade = MyTrading()

def my_trading():
    # Деление позиций на А и В-----------------------------------------------------------------------------

    divisionsAB('LONG', 'SHORT', index_a)
    divisionsAB('SHORT', 'LONG', index_b)

    pair_a = np.array_split(index_a, len(index) / 2)
    pair_b = np.array_split(index_b, len(index) / 2)

    # Запускаем бесконечный цикл бота-----------------------------------------------------------------------------
    while True:
        # выполняем определенную задачу
        try:
            response = um_futures_client.account(recvWindow=50000)
            for item in response['assets']:
                if item['asset'] == 'USDT':
                    pos_margin = float(item['positionInitialMargin'])
            # Запросим баланс-----------------------------------------------------------------------------
            url_pos = 'https://fapi.binance.com/fapi/v2/positionRisk'
            rpos = requests.get(url_pos)
            datapos = rpos.json()

            positions = response['positions']
            write_equity('my_txt/equity.txt')

            # Трейдинг-----------------------------------------------------------------------------
            if float(pos_margin) == 0:

                # Задаём плечи-----------------------------------------------------------------------------
                leverg(index)

                # Открываем позиции А-----------------------------------------------------------------------------
                for token_a in index_a:
                    trade(token_a['sym'], token_a['side'])
                # Открываем позиции В-----------------------------------------------------------------------------
                for token_b in index_b:
                    trade(token_b['sym'], token_b['side'])

                # Добавялем запись о новой позе и записываем убыток по новой позе в файл
                with open('my_txt/lossA.txt', 'r') as fr:
                    lossA_list = json.load(fr)
                with open('my_txt/lossA.txt', 'w') as fw:
                    lossA_list.append({'number_pos': lossA_list[-1]['number_pos'] + 1, 'max_loss': "0"})
                    json.dump(lossA_list, fw)

                with open('my_txt/lossB.txt', 'r') as fr:
                    lossB_list = json.load(fr)
                with open('my_txt/lossB.txt', 'w') as fw:
                    lossB_list.append({'number_pos': lossB_list[-1]['number_pos'] + 1, 'max_loss': "0"})
                    json.dump(lossB_list, fw)

                # Добавялем запись о новой позе и записываем прибыль по новой позе в файл
                with open('my_txt/profitA.txt', 'r') as fr:
                    profitA_list = json.load(fr)
                with open('my_txt/profitA.txt', 'w') as fw:
                    profitA_list.append({'number_pos': profitA_list[-1]['number_pos'] + 1, 'max_profit': "0"})
                    json.dump(profitA_list, fw)

                with open('my_txt/profitB.txt', 'r') as fr:
                    profitB_list = json.load(fr)
                with open('my_txt/profitB.txt', 'w') as fw:
                    profitB_list.append({'number_pos': profitB_list[-1]['number_pos'] + 1, 'max_profit': "0"})
                    json.dump(profitB_list, fw)

                # Добавялем запись о новой позе по паре и записываем прибыль по новой позе в файл
                for txt in pair_txt_list:
                    writeNewPosPnl(txt)

            # Деление поз на А и В -----------------------------------------------------------------------------
            pos = pos_info.positions()
            pos_a = create_array_pos_a()
            pos_b = create_array_pos_b()
            # Закрытие одной из поз при отсутствии второй позы в паре-----------------------------------------------------------------------------
            while len(pos) % 2 != 0:
                for pair in pair_a:
                    checkPos(pair)

                for pair in pair_b:
                    checkPos(pair)

            # Подсчёт максимальных значений по парам и запись их в файл -----------------------------------------------------------------------------
            calculator = ProfitCalculator()
            if len(pos_a) > 0:
                for pair in pair_a:
                    thread_write_a = threading.Thread(target=calculator.writPnlPair(pair))
                    thread_write_a.start()
            if len(pos_b) > 0:
                for pair in pair_b:
                    thread_write_b = threading.Thread(target=calculator.writPnlPair(pair))
                    thread_write_b.start()


            # # Усреднение поз A-----------------------------------------------------------------------------
            if len(pos_a) > 0:
                double(pos_a, -15, 1)

            if len(pos_b) > 0:
                double(pos_b, -15, 1)

            if len(pos_a) > 0:
                double(pos_a, -30, 2)

            if len(pos_b) > 0:
                double(pos_b, -30, 2)

            # Закрытие поз A-----------------------------------------------------------------------------
            close_check_a = 0
            if len(pos_a) > 0 and len(pos_b) > 0:
                if calculator.pnlPair(pair_a[0]) > calculator.profitPair(pair_a[0]) and calculator.pnlAB(pos_a, 'my_txt/pnlA.txt') > 2:
                    for pos_a_token in pos_a:
                        close(pos_a_token['symbol'], pos_a_token['positionSide'], pos_a_token['positionAmt'])
                        close_check_a = 1
                        print("Закрытие поз А")

            if len(pos_a) > 0 and len(pos_b) == 0:
                if calculator.pnlAB(pos_a, 'my_txt/pnlA.txt') > calculator.profitPair(pair_a[0]) / 3 and calculator.pnlAB(pos_a, 'my_txt/pnlA.txt') > 2:
                    for pos_a_token in pos_a:
                        close(pos_a_token['symbol'], pos_a_token['positionSide'], pos_a_token['positionAmt'])
                        close_check_a = 1
                        print("Закрытие поз А")

            if close_check_a == 1:
                with open('my_txt/pnlpair_A.txt', 'r') as fr:
                    close_info = [emoji.emojize(':money_bag:Закрытие'), '\n', json.load(fr)]
                    close_info = ' '.join(close_info)
                with open('close_pos.txt', 'w') as fw:
                    json.dump(close_info, fw)

            # Закрытие поз B-----------------------------------------------------------------------------
            close_check_b = 0
            if len(pos_b) > 0 and len(pos_a) > 0:
                if calculator.pnlPair(pair_b[0]) > calculator.profitPair(pair_b[0]) and calculator.pnlAB(pos_b, 'my_txt/pnlB.txt') > 2:
                    for pos_b_token in pos_b:
                        close(pos_b_token['symbol'], pos_b_token['positionSide'], pos_b_token['positionAmt'])
                        close_check_b = 1
                        print("Закрытие поз B")
            if len(pos_b) > 0 and len(pos_a) == 0:
                if calculator.pnlAB(pos_b, 'my_txt/pnlB.txt') > calculator.profitPair(pair_b[0]) / 3 and calculator.pnlAB(pos_b, 'my_txt/pnlB.txt') > 2:
                    for pos_b_token in pos_b:
                        close(pos_b_token['symbol'], pos_b_token['positionSide'], pos_b_token['positionAmt'])
                        close_check_b = 1
                        print("Закрытие поз B")

            if close_check_b == 1:
                with open('my_txt/pnlpair_B.txt', 'r') as fr:
                    close_info = [emoji.emojize(':money_bag:Закрытие'), '\n', json.load(fr)]
                    close_info = ' '.join(close_info)
                with open('my_txt/close_pos.txt', 'w') as fw:
                    json.dump(close_info, fw)
            #
            # # Частичное закрытие позы с большим расстоянием от точки входа-----------------------------------------------------------------------------
            if calculator.pnlAB(pos_a, 'pnlA.txt') < calculator.profitPair(pair_a[0]) * -1 or calculator.pnlAB(pos_b, 'pnlB.txt') < calculator.profitPair(pair_b[0]) * -1:
                for posa_x in pos:
                    if posa_x["symbol"] != 'BTCUSDT' and posa_x["symbol"] != 'ETHUSDT':
                        price = float(Info(posa_x["symbol"]).lastprice)
                        entry_price = float(posa_x["entryPrice"])
                        proc_distance = float(posa_x["entryPrice"]) / 100 * checkDistance(posa_x)
                        critical_distance = float(posa_x["entryPrice"]) / 100 * 10
                        if posa_x["positionSide"] == "LONG":
                            if price < (entry_price - proc_distance - critical_distance):
                                with open('close_pos_dist.txt', 'w') as fw:
                                    close_info = [emoji.emojize(
                                        ':chart_increasing:Частичное закрытие позы с большим расстоянием от точки входа'),
                                                  '\n', posa_x['symbol'], '\n', f'Дистанция позы: {calculator.pnlPos(posa_x)}',
                                                  '\n', f'Средняя дистанция по позам: {checkDistance(posa_x)}',
                                                  '\n',
                                                  f'pnl: {float(posa_x["unrealizedProfit"]) / balance * 100:.{2}f}%']
                                    close_info = ' '.join(close_info)
                                    json.dump(close_info, fw)
                                    close(posa_x['symbol'], posa_x['positionSide'], posa_x['positionAmt'])
                                print("Частичное закрытие позы с большим расстоянием от точки входа")
                        if posa_x["positionSide"] == "SHORT":
                            if price > (entry_price + proc_distance + critical_distance):
                                with open('close_pos_dist.txt', 'w') as fw:
                                    close_info = [emoji.emojize(
                                        ':chart_increasing:Частичное закрытие позы с большим расстоянием от точки входа'),
                                                  '\n', posa_x['symbol'], '\n', f'Дистанция позы: {calculator.pnlPos(posa_x)}',
                                                  '\n', f'Средняя дистанция по позам: {checkDistance(posa_x)}',
                                                  '\n',
                                                  f'pnl: {float(posa_x["unrealizedProfit"]) / balance * 100:.{2}f}%']
                                    close_info = ' '.join(close_info)
                                    json.dump(close_info, fw)
                                    close(posa_x['symbol'], posa_x['positionSide'], posa_x['positionAmt'])
                                print("Частичное закрытие позы с большим расстоянием от точки входа")

            # Частичное закрытие с профитом-----------------------------------------------------------------------------
            if len(pos_a) > 0:
                # Создаем новый поток и передаем туда метод calculate_profit()
                thread_pnl_pair_a = threading.Thread(target=calculator.create_pnl_pair_ab_array('my_txt/pnlpair_A.txt', 'Позы А', pair_a, pos_a, 'my_txt/pnlA.txt'))
                thread_pnl_pair_a.start()
                for pair in pair_a:
                    for posas in pos_a:
                        if pair[0]['sym'] == posas['symbol']:
                            if pair[0]['sym'] != 'BTCUSDT':
                                if calculator.pnlPair(pair) > calculator.profitPair(pair):
                                    closePair(pair, 'my_txt/close_pos_pair_A.txt')
            if len(pos_b) > 0:
                # Создаем новый поток и передаем туда метод calculate_profit()
                thread_pnl_pair_b = threading.Thread(target=calculator.create_pnl_pair_ab_array('my_txt/pnlpair_B.txt', 'Позы B', pair_b, pos_b, 'my_txt/pnlB.txt'))
                thread_pnl_pair_b.start()
                for pair in pair_b:
                    for posb in pos_b:
                        if pair[0]['sym'] == posb['symbol']:
                            # Условие по закрытию-----------------------------------------------------------------------------
                            if pair[0]['sym'] != 'BTCUSDT':
                                if calculator.pnlPair(pair) > calculator.profitPair(pair):
                                    closePair(pair, 'my_txt/close_pos_pair_B.txt')


            # Запрос состояния поз от пользователя и запись при необходимости поз в файлы-----------------------------------------------------------------------------

            if os.stat('my_txt/request_pos_a.txt').st_size > 0:
                posAB(pos_a, 'my_txt/posA.txt')
                with open('my_txt/request_pos_a.txt', 'w') as fw:
                    pass

            if os.stat('my_txt/request_pos_b.txt').st_size > 0:
                posAB(pos_b, 'my_txt/posB.txt')
                with open('my_txt/request_pos_b.txt', 'w') as fw:
                    pass

            # Принты-----------------------------------------------------------------------------

            if calculator.pnlAB(pos_a, 'my_txt/pnlA.txt') < 0:
                print("PNL A:" + Fore.RED + f" {calculator.pnlAB(pos_a, 'my_txt/pnlA.txt'):.{2}f} %", Style.RESET_ALL)
            else:
                print("PNL A:" + Fore.GREEN + f" {calculator.pnlAB(pos_a, 'my_txt/pnlA.txt'):.{2}f} %", Style.RESET_ALL)

            if calculator.pnlAB(pos_b, 'my_txt/pnlB.txt') < 0:
                print("PNL B:" + Fore.RED + f" {calculator.pnlAB(pos_b, 'my_txt/pnlB.txt'):.{2}f} %", Style.RESET_ALL)
            else:
                print("PNL B:" + Fore.GREEN + f" {calculator.pnlAB(pos_b, 'my_txt/pnlB.txt'):.{2}f} %", Style.RESET_ALL)


            plA = calculator.pnlAB(pos_a, 'my_txt/pnlA.txt')
            plB = calculator.pnlAB(pos_b, 'my_txt/pnlB.txt')

            calculator.profitA(plA)

            calculator.profitB(plB)
            calculator.lossA(plA)
            calculator.lossB(plB)
            calculator.profit_lossA()
            calculator.profit_lossB()


            time.sleep(3)

        except binance.error.ClientError as err:
            print('ReduceOnly Order is rejected')
            time.sleep(5)
        except ConnectionError as err:
            print('Connection reset by peer')
            time.sleep(5)
        except binance.error.ServerError as err:
            print('except binance.error.ServerError as err:')
            time.sleep(5)
        except ccxt.base.errors.NetworkError as err:
            print('ccxt.base.errors.RequestTimeout as err:')
            time.sleep(5)
        except TypeError as err:
            print('except TypeError as err:')
            time.sleep(5)
        except ReadTimeoutError as err:
            print('except ReadTimeoutError as err:')
            time.sleep(5)

