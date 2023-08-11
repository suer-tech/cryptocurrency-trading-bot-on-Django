import asyncio
import json
import threading
import asyncio
import threading
import time

import telebot
from django.http import HttpResponse
from django.shortcuts import render

import importlib
import json
from datetime import datetime

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor

from core.services.keyboard import greet_kb1
import os
from threading import Thread

token = '6026428031:AAFcoXdslKvztNPf0bbMhvA-qRvU_DM7m9Q'

bot = Bot(token)
dp = Dispatcher(bot)

current_datetime = datetime.now()

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIDZ2JEZuGR8N1D5s__y0O8cIUGMk9OAAIiEwACXWxwS64th70744A-IwQ')
    mess = f'Привет, <b>{message.from_user.first_name}</b>'
    await bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=greet_kb1)

@dp.message_handler(Text(equals="PNL A"))
async def with_puree(message: types.Message):
    # открываем файл в режиме чтения
    with open('my_txt/pnlpair_A.txt', 'r') as fr:
        # читаем из файла
        pnlposA = json.load(fr)
    await bot.send_message(message.chat.id,pnlposA)


@dp.message_handler(Text(equals="PNL B"))
async def with_puree(message: types.Message):
    # открываем файл в режиме чтения
    with open('my_txt/pnlpair_B.txt', 'r') as fr:
        # читаем из файла
        pnlposB = json.load(fr)
    await bot.send_message(message.chat.id,pnlposB)

@dp.message_handler(Text(equals="Pos A"))
async def with_puree(message: types.Message):
    with open('my_txt/request_pos_a.txt', 'w') as fw:
        status = 'request'
        json.dump(status, fw)
    mess = 'Обработка запроса...'
    await bot.send_message(message.chat.id, mess)

@dp.message_handler(Text(equals="Pos B"))
async def with_puree(message: types.Message):
    with open('my_txt/request_pos_b.txt', 'w') as fw:
        status = 'request'
        json.dump(status, fw)
    mess = 'Обработка запроса...'
    await bot.send_message(message.chat.id, mess)

@dp.message_handler(Text(equals="Max profit/loss A"))
async def with_puree(message: types.Message):
    # открываем файл в режиме чтения
    with open('my_txt/profit_lossA.txt', 'r') as fr:
        # читаем из файла
        profitA = json.load(fr)
        await bot.send_message(message.chat.id,profitA)

@dp.message_handler(Text(equals="Max profit/loss B"))
async def with_puree(message: types.Message):
    # открываем файл в режиме чтения
    with open('my_txt/profit_lossB.txt', 'r') as fr:
        # читаем из файла
        profitB = json.load(fr)
        await bot.send_message(message.chat.id,profitB)

@dp.message_handler(Text(equals="Balance"))
async def with_puree(message: types.Message):
    # открываем файл в режиме чтения
    with open('my_txt/balance.txt', 'r') as fr:
        # читаем из файла
        bal = json.load(fr)
        await bot.send_message(message.chat.id,bal)

# Создаем глобальный объект мьютекса
api_lock = threading.Lock()

# Первый поток
def telegram_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def start_polling_with_lock():
        # Захватываем мьютекс перед началом работы с API
        with api_lock:
            await dp.start_polling()

    loop.run_until_complete(start_polling_with_lock())

# Второй поток
def message_monitor():
    # ...
    user_id = 412850740
    bot = telebot.TeleBot(token, parse_mode=None)

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
            # Захватываем мьютекс перед отправкой сообщений через API
            with api_lock:
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
