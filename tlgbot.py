import telebot
from Constatnt import TOKEN
import requests
import json
from ourclass import ConvertException, ValConv

bot = telebot.TeleBot(TOKEN)

def get_valute():
    sp_valute = []
    r = requests.get('https://v6.exchangerate-api.com/v6/820a7e6fb564ea48ea280740/latest/USD')
    text = json.loads(r.content)['conversion_rates']
    for val in text:
        sp_valute.append(val)
    with open('basevalute.json', 'w') as data:
        json.dump(sp_valute, data)
    return sp_valute

@bot.message_handler(commands=['start', 'help', 'valute'])
def startcommand(message: telebot.types.Message):
    if message.text == '/start' or message.text == '/help':
        text = 'Данный бот предназначен для конвертирования валют.\n' \
               'Для конвертирования валют введите: \n ' \
               '<Базовая валюта, цену которой нужно узнать> ' \
               '<Валюта в которой надо узнать цену базовой> <количество базовой валюты>.\n' \
               '!!! Перед обработкой обязательно узнайте информацию о доступных валютах /valute.'
        bot.reply_to(message, text)
    elif message.text == '/valute':
        text = 'Доступные валюты: '
        valute = get_valute()
        for val in valute:
            text += f'\n {val}'
        bot.reply_to(message, text)

@bot.message_handler(content_types= ['text', ])
def convertetion(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertException('Неверное количество переменных.')

        val1, val2, freq = values
        res = ValConv.covert_valute(val1, val2, freq)
    except ConvertException as e:
        bot.reply_to(message, f'Ошибка: {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду {e}')
    else:
        text = f'{freq} валюты {val1}, в валюте {val2} будет стоить: {res}'
        bot.reply_to(message, text)

bot.polling()





