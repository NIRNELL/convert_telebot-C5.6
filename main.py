import telebot
from config import TOKEN, currency_list
from extensions import CryptoConvertor, ValuesException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands = ['start', 'help'])
def start(message: telebot.types.Message):
    text = ('Приветствую!'
            '\nЧтобы начать работу, введите команду боту в следующем формате: '
            '\n<в какую валюту перевести> <имя валюты> <количество переводимой валюты>'
            '\n'
            '\nПосмотреть список доступных валют: /values')
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in currency_list.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)

@bot.message_handler(content_types = ['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise ValuesException('Неверное количество параметров!\nПовторите ввод.')
        text_fin = CryptoConvertor.convert(*values)
    except ValuesException as e:
        bot.reply_to(message, f'Ошибка ввода:\n{e}\nПовторите ввод.')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду:\n{e}')
    else:
        bot.reply_to(message, text_fin)

bot.polling()