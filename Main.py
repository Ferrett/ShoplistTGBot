import telebot
import sqlite3
from telebot import types
from datetime import datetime
import json

with open('config.json', 'r') as file:
    data = json.load(file)

bot = telebot.TeleBot(data['bot_token'])
users = [123456789, 987654321]


@bot.message_handler(commands=['start'])
def start(message):
    liststr = 'Список:\n'

    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute(f"SELECT 1 FROM Item LIMIT 1")
    if cursor.fetchone() is None:
        liststr = 'Список пуст!'
    else:
        cursor.execute(f"SELECT Name FROM Item")
        names = cursor.fetchall()
        liststr += '\n'.join(f"— {name[0]}" for name in names)
    cursor.close()
    conn.close()

    markup = types.ReplyKeyboardMarkup()
    btn = types.KeyboardButton('Обновить')
    markup.row(btn)
    btn2 = types.KeyboardButton('Удалить')
    btn3 = types.KeyboardButton('Добавить')
    markup.row(btn2, btn3)
    bot.send_message(message.chat.id, liststr, reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


def on_click(message):
    if message.text == 'Обновить':
        return start(message)
    elif message.text == 'Удалить':
        return on_delete_from_list(message)
    elif message.text == 'Добавить':
        return on_add_to_list(message)
    else:
        bot.register_next_step_handler(message, on_click)


def on_add_to_list(message):
    markup = types.ReplyKeyboardMarkup()
    btn = types.KeyboardButton('Отмена')
    markup.row(btn)
    bot.send_message(message.chat.id, 'Введите новый товар:', reply_markup=markup)
    bot.register_next_step_handler(message, add_item)


def add_item(message):
    if message.text == 'Отмена':
        return start(message)

    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    # Iterate over each line
    for line in message.text.splitlines():
        cursor.execute("INSERT INTO Item (Name, CreationDate) VALUES (?, ?)", (f'{line}', f'{datetime.now()}'))
    conn.commit()
    cursor.close()
    conn.close()
    return start(message)


def on_delete_from_list(message):
    markup = types.ReplyKeyboardMarkup()
    if delete_item_markup(message, markup):
        bot.send_message(message.chat.id, 'Нажмите на товар, который хотите удалить', reply_markup=markup)
        bot.register_next_step_handler(message, delete_item)


def item_deleted_from_list(message):
    markup = types.ReplyKeyboardMarkup()
    if delete_item_markup(message, markup):
        bot.send_message(message.chat.id, f'\'{message.text}\' - Удалён', reply_markup=markup)
        bot.register_next_step_handler(message, delete_item)


def delete_item_markup(message, markup):
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()

    # Check if the 'Item' table is empty
    cursor.execute("SELECT 1 FROM Item LIMIT 1")
    val = cursor.fetchone()
    if val is None:
        start(message)
    else:
        cursor.execute("SELECT Name FROM Item")
        names = cursor.fetchall()
        markup.row(types.KeyboardButton('Назад'))
        for name in names:
            markup.row(types.KeyboardButton(name[0]))
        markup.row(types.KeyboardButton('Удалить всё'))

    cursor.close()
    conn.close()
    return val

def delete_item(message):
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()

    if message.text == 'Назад':
        start(message)
    elif message.text == 'Удалить всё':
        cursor.execute(f"DELETE FROM Item")
        conn.commit()

        start(message)
    elif any(item[0] == message.text for item in cursor.execute("SELECT Name FROM Item").fetchall()):
        cursor.execute(f"DELETE FROM Item where Name = '{message.text}'")
        conn.commit()

        item_deleted_from_list(message)
    else:
        bot.register_next_step_handler(message, delete_item)
    cursor.close()
    conn.close()


@bot.message_handler()
def info(message):
    return start(message)


bot.polling(none_stop=True)
