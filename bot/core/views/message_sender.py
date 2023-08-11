import threading
import telebot
import time
import json
import os

from core.views.telegram import token
from core.views.tg_token import user_id


def message_monitor():
    token_tg = token
    bot = telebot.TeleBot(token, parse_mode=None)
    id_user_ = user_id

    def mess(txt_file):
        if os.stat(txt_file).st_size > 0:
            with open(txt_file, 'r') as fr:
                mess = json.load(fr)
            bot.send_message(user_id, mess)
            with open(txt_file, 'w') as fw:
                pass

    while True:
        time.sleep(1)
        try:
            mess('my_txt/close_pos.txt')
            mess('my_txt/close_pos_pair_A.txt')
            mess('my_txt/close_pos_pair_B.txt')
            mess('my_txt/close_pos_dist.txt')
            mess('my_txt/close_pos_hedje.txt')
            mess('my_txt/posA.txt')
            mess('my_txt/posB.txt')

        except json.decoder.JSONDecodeError as err:
            mess = 'ошибка'

# Создаем новый поток и запускаем в нем функцию мониторинга
message_sender_thread = threading.Thread(target=message_monitor)
message_sender_thread.start()