import asyncio
import threading

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

# Функция, которая будет выполняться в отдельном потоке
def telegram_thread():
    # Создайте новый событийный цикл
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Запустите цикл обновлений бота
    loop.run_until_complete(dp.start_polling())

# запуск потока телеграм-бота

telegram_thread = threading.Thread(target=telegram_thread)
telegram_thread.start()

