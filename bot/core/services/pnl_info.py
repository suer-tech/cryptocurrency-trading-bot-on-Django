import json
import math
import statistics
import threading

from core.services.balances import total_balance
from core.services.base import create_lossA_list, create_profitB_list, create_profitA_list, create_lossB_list
from core.services.pos_info import positions, create_array_pos_a, create_array_pos_b
from core.services.token_info import Info
from core.services.txt import checkSym
from ..trading import *


class ProfitCalculator:
    def pnlPos(self, pos_token):
        price = Info(pos_token["symbol"]).lastprice
        distance = (float(pos_token["entryPrice"]) - float(price)) / float(pos_token["entryPrice"]) * 100
        return distance

    def lossA(self, plA):
        # проверяем  убыток по позе и сравниваем из файла
        lossA_list = create_lossA_list()
        if float(plA) < 0:
            if float(lossA_list[-1]['max_loss']) > float(plA):
                with open('my_txt/lossA.txt', 'w') as fw:
                    pass
                with open('my_txt/lossA.txt', 'w') as fw:
                    lossA_list[-1]['max_loss'] = plA
                    json.dump(lossA_list, fw)

    def lossB(self, plB):
        # проверяем  убыток по позе и сравниваем из файла
        lossB_list = create_lossB_list()
        if float(plB) < 0:
            if float(lossB_list[-1]['max_loss']) > float(plB):
                with open('my_txt/lossB.txt', 'w') as fw:
                    pass
                with open('my_txt/lossB.txt', 'w') as fw:
                    lossB_list[-1]['max_loss'] = plB
                    json.dump(lossB_list, fw)


    def profitA(self, plA):
        # проверяем  прибыль по позе и сравниваем из файла
        profitA_list = create_profitA_list()
        if float(profitA_list[-1]['max_profit']) < float(plA):
            with open('my_txt/profitA.txt', 'w') as fw:
                pass
            with open('my_txt/profitA.txt', 'w') as fw:
                profitA_list[-1]['max_profit'] = plA
                json.dump(profitA_list, fw)

    def profitB(self, plB):
        # проверяем  прибыль по позе и сравниваем из файла
        profitB_list = create_profitB_list()
        if float(profitB_list[-1]['max_profit']) < float(plB):
            with open('my_txt/profitB.txt', 'w') as fw:
                pass
            with open('my_txt/profitB.txt', 'w') as fw:
                profitB_list[-1]['max_profit'] = plB
                json.dump(profitB_list, fw)

    def profit_lossA(self):
        with open('my_txt/profit_lossA.txt', 'w') as fw:
            pass
        profit_loss = []
        profit_list = []
        with open('my_txt/profitA.txt', 'r') as fr:
            # читаем из файла
            try:
                profit_list = json.load(fr)
                one = f"Max profit: {float(profit_list[-1]['max_profit']):.{2}f}%"
                profit_loss.append(one)
                profit_loss.append('\n')

            except json.decoder.JSONDecodeError as err:
                one = "Max profit: 0%"
                profit_loss.append(one)
                profit_loss.append('\n')

        with open('my_txt/lossA.txt', 'r') as fr:
            # читаем из файла
            try:
                loss_list = json.load(fr)
                two = f"Max loss: {float(loss_list[-1]['max_loss']):.{2}f}%"
                profit_loss.append(two)
                profit_loss.append('\n')

            except json.decoder.JSONDecodeError as err:
                two = "Max profit: 0%"
                profit_loss.append(two)
                profit_loss.append('\n')

        if len(profit_loss) > 0:
            profit_loss = ' '.join(profit_loss)
            # записываем прибыль и убыток А в файл
            with open('my_txt/profit_lossA.txt', 'w') as fw:
                json.dump(profit_loss, fw)

    def profit_lossB(self):
        with open('my_txt/profit_lossB.txt', 'w') as fw:
            pass
        profit_loss = []
        with open('my_txt/profitB.txt', 'r') as fr:
            # читаем из файла
            try:
                profit_list = json.load(fr)
                one = f"Max profit: {float(profit_list[-1]['max_profit']):.{2}f}%"
                profit_loss.append(one)
                profit_loss.append('\n')

            except json.decoder.JSONDecodeError as err:
                one = "Max profit: 0%"
                profit_loss.append(one)
                profit_loss.append('\n')

        with open('my_txt/lossB.txt', 'r') as fr:
            try:
                # читаем из файла
                loss_list = json.load(fr)
                two = f"Max loss: {float(loss_list[-1]['max_loss']):.{2}f}%"
                profit_loss.append(two)
                profit_loss.append('\n')

            except json.decoder.JSONDecodeError as err:
                two = "Max profit: 0%"
                profit_loss.append(two)
                profit_loss.append('\n')

        if len(profit_loss) > 0:
            profit_loss = ' '.join(profit_loss)
            # записываем прибыль и убыток B в файл
            with open('my_txt/profit_lossB.txt', 'w') as fw:
                json.dump(profit_loss, fw)

    def pnlAB(self, pos_a, pnl_txt_file):
        # очищаем все данные из файла с позами
        with open(pnl_txt_file, 'w') as fw:
            pass
        pnl = 0
        pos = positions()
        total_bal = total_balance()
        for crypto in pos_a:
            for token in pos:
                if crypto['symbol'] == token['symbol']:
                    if crypto['positionSide'] == 'LONG' and token['positionSide'] == 'LONG':
                        pnl = pnl + float(token['unrealizedProfit'])
                    if crypto['positionSide'] == 'SHORT' and token['positionSide'] == 'SHORT':
                        pnl = pnl + float(token['unrealizedProfit'])
        with open(pnl_txt_file, 'w') as fw:
            json.dump(f"{pnl/total_bal*100:.{2}f}", fw)
        return pnl/total_bal*100

    # Подсчет прибыли по паре________________________________________________________________________
    def pnlPair(self, pair):
        pos = positions()
        total_bal = total_balance()
        pnl_pair = 0
        for one in pos:
            if one["symbol"] == pair[0]['sym'] and one['positionSide'] == pair[0]['side']:
                pnl_pair = pnl_pair + float(one['unrealizedProfit'])

        for two in pos:
            if two["symbol"] == pair[1]['sym'] and two['positionSide'] == pair[1]['side']:
                pnl_pair = pnl_pair + float(two['unrealizedProfit'])
        return pnl_pair / total_bal * 100

    # Проверка размера и прибыли по паре и Запись прибыли по паре________________________________________________________________________
    def writPnlPair(self, pair):
        symb = pair[0]['sym']
        pair_txt_file = checkSym(symb)
        try:
            with open(f'my_txt/{pair_txt_file}', 'r') as fr:
                pair_loss_list = json.load(fr)
        except json.decoder.JSONDecodeError as err:
            pair_loss_list = [{'number_pos': 0, 'max_loss': "0"}]

        if abs(self.pnlPair(pair)) > abs(float(pair_loss_list[-1]['max_loss'])):
            pair_loss_list[-1]['max_loss'] = f"{self.pnlPair(pair):.{2}f}"
            with open(f'my_txt/{pair_txt_file}', 'w') as fw:
                json.dump(pair_loss_list, fw)

    # Рассчитываем процент тейк-профита по паре
    def profitPair(self, pair):
        symb = pair[0]['sym']
        pair_txt_file = checkSym(symb)
        try:
            with open(f'my_txt/{pair_txt_file}', 'r') as fr:
                pair_loss_list = json.load(fr)

        except json.decoder.JSONDecodeError as err:
            print("profitPair(self, pair)    json.decoder.JSONDecodeError")
            with open(f'my_txt/{pair_txt_file}', 'w') as fw:
                pair_loss_list = [{'number_pos': 0, 'max_loss': "0"}]
                json.dump(pair_loss_list, fw)
            return 0.3
        except FileNotFoundError as err:
            with open(pair_txt_file, 'w') as fw:
                pair_loss_list = [{'number_pos': 0, 'max_loss': "0"}]
                json.dump(pair_loss_list, fw)

        last_five = pair_loss_list[-5:]  # выбираем последние пять элементов массива
        # print('last_five')
        # print(last_five)
        central_tendency = statistics.median([abs(float(item['max_loss'])) for item in last_five])
        # print('central_tendency')
        # print(central_tendency)
        mean_value = sum([abs(float(item['max_loss'])) for item in last_five]) / len(last_five)
        # print('mean_value')
        # print(mean_value)
        std_deviation = math.sqrt(
            sum([(abs(float(item['max_loss'])) - mean_value) ** 2 for item in last_five]) / len(last_five))
        # print('std_deviation')
        # print(std_deviation)
        filtered_array = [item for item in last_five if
                          abs(float(item['max_loss']) - central_tendency) <= 2 * std_deviation]
        # print('filtered_array')
        # print(filtered_array)
        if len(filtered_array) == 0:
            filtered_array = last_five
        max_losses = [float(d["max_loss"]) for d in filtered_array]  # извлекаем значения "max_loss"
        # print('max_losses')
        # print(max_losses)
        average_max_loss = abs(statistics.median(max_losses))
        # print('average_max_loss')
        # print(average_max_loss)
        # print('average_max_loss - average_max_loss / 100 * 30')
        # print(average_max_loss - average_max_loss / 100 * 30)
        base_take = 0.3
        if average_max_loss > 0.6:
            return average_max_loss - average_max_loss / 100 * 30
        if 0.25 < average_max_loss < 0.6:
            return average_max_loss - average_max_loss / 100 * 20
        if average_max_loss < 0.25:
            return base_take

    def create_pnl_pair_ab_array(self, txt, posab, pair_a, pos_ab, pnltxt):
        with open(txt, 'w') as fw:
            pass
        pos_a = create_array_pos_a
        pos_b = create_array_pos_b
        pnlpair_ab = [posab]
        pnlpos = ''
        pnlpair_ab.append('\n')
        for pair in pair_a:
            for posas in pos_ab:
                if pair[0]['sym'] == posas['symbol']:
                    pnlpair_ab.append('\n')
                    pnlpair_ab.append(pair[0]['sym'][:-4])
                    pnlpair_ab.append('-')
                    pnlpair_ab.append(pair[1]['sym'][:-4])
                    pnlpair_ab.append('= ')
                    pnlpair_ab.append(f'{self.pnlPair(pair):.{2}}% [{self.profitPair(pair):.{2}}%]')
                    self.profitPair(pair)
        pnlpair_ab.append('\n')
        pnlpair_ab.append('\n')
        pnlpos = f"PNL = {self.pnlAB(pos_ab, pnltxt):.{2}f}"

        pnlpair_ab.append(pnlpos)
        pnlpair_ab = ' '.join(pnlpair_ab)
        with open(txt, 'w') as fw:
            json.dump(pnlpair_ab, fw)

