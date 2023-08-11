from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_pnlA = KeyboardButton("PNL A")
button_pnlB = KeyboardButton("PNL B")
button_posA = KeyboardButton("Pos A")
button_posB = KeyboardButton("Pos B")
button_max_profit_loss_A = KeyboardButton("Max profit/loss A")
button_max_profit_loss_B = KeyboardButton("Max profit/loss B")
button_balance = KeyboardButton("Balance")

greet_kb1 = ReplyKeyboardMarkup(resize_keyboard=True).add(button_pnlA, button_pnlB).row(button_posA, button_posB).row(button_max_profit_loss_A, button_max_profit_loss_B).row(button_balance)





