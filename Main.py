import telebot
from telebot import types

bot = telebot.TeleBot('6558187379:AAFQeAw0td96ht761lPdIw4x0ZVbUgNMS4I')
shoplist = ['1', '2', '3']
users = [123456789, 987654321]

@bot.message_handler(commands=['start'])
def start(message):
    liststr = 'Список:\n'
    if len(shoplist) == 0:
        liststr = 'Список пуст!'
    else:
        for index, element in enumerate(shoplist, start=1):
            liststr += f"— {element}\n"
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
    shoplist.extend(message.text.splitlines())
    return start(message)


def on_delete_from_list(message):
    markup = types.ReplyKeyboardMarkup()
    delete_item_markup(message, markup)
    bot.send_message(message.chat.id, 'Нажмите на товар, который хотите удалить', reply_markup=markup)
    bot.register_next_step_handler(message, delete_item)


def item_deleted_from_list(message):
    markup = types.ReplyKeyboardMarkup()
    delete_item_markup(message, markup)
    bot.send_message(message.chat.id, f'\'{message.text}\' - Удалён', reply_markup=markup)
    bot.register_next_step_handler(message, delete_item)


def delete_item_markup(message, markup):
    if len(shoplist) == 0:
        return start(message)
    markup.row(types.KeyboardButton('Назад'))
    for element in shoplist:
        markup.row(types.KeyboardButton(element))
    markup.row(types.KeyboardButton('Удалить всё'))


def delete_item(message):
    if message.text == 'Назад':
        return start(message)
    elif message.text == 'Удалить всё':
        shoplist.clear()
        return start(message)
    elif any(item == message.text for item in shoplist):
        shoplist.remove(message.text)
        return item_deleted_from_list(message)
    else:
        bot.register_next_step_handler(message, delete_item)


@bot.message_handler()
def info(message):
    return start(message)


bot.polling(none_stop=True)
