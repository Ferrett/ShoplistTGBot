import telebot

bot = telebot.TeleBot('6558187379:AAFQeAw0td96ht761lPdIw4x0ZVbUgNMS4I')


@bot.message_handler(commands=['start','main','hello'])
def main(message):
    bot.send_message(message.chat.id, 'Hello')

bot.polling(none_stop=True)
