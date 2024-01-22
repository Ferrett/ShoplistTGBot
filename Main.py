import telebot
from telebot import types

bot = telebot.TeleBot('6558187379:AAFQeAw0td96ht761lPdIw4x0ZVbUgNMS4I')
shoplist = ['1', '2', '3']


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Открыть список')
    markup.row(btn1)
    btn2 = types.KeyboardButton('Удалить из списка')
    btn3 = types.KeyboardButton('Добавить в список')
    markup.row(btn2, btn3)
    bot.send_message(message.chat.id, 'Добро пожаловать', reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


def on_click(message):
    if message.text == 'Открыть список':
        liststr = ''
        if len(shoplist) == 0:
            liststr = 'Список пуст!'
        else:
            for index, element in enumerate(shoplist, start=1):
                liststr += f"{index}. {element}\n"
        bot.send_message(message.chat.id, liststr)
        bot.register_next_step_handler(message, start)
    elif message.text == 'Удалить из списка':
        bot.send_message(message.chat.id, 'Удалить:')
    elif message.text == 'Добавить в список':
        bot.send_message(message.chat.id, 'Добавить:')


@bot.message_handler(commands=['help'])
def main(message):
    bot.send_message(message.chat.id, '<b>help</b> <u>info</u>', parse_mode='html')


@bot.message_handler()
def info(message):
    if message.text == 'Открыть список1':
        bot.send_message(message.chat.id, 'Список:')
    elif message.text == 'Удалить из списка1':
        bot.send_message(message.chat.id, 'Удалить:')
    elif message.text == 'Добавить в список1':
        bot.send_message(message.chat.id, 'Добавить:')
    else:
        bot.send_message(message.chat.id, 'Ничё не понял')


bot.polling(none_stop=True)
