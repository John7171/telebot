import telebot
import requests
import json
from confiq import keys,TOKEN
from extensions import ConvertExeption,Cryptoconverter,ApiExeption

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start','help'])
def repeat(message: telebot.types.Message):
    text = ' Чтобы начать работу введите команду в следующем формате: \n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты> \n увидеть список доступных валют: /values'
    bot.reply_to(message,text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text='\n'.join((text,key,))
    bot.reply_to(message,text)

@bot.message_handler(commands=['text',])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertExeption('Лишние параметры')

        quote, base, amount = values
        total_base = Cryptoconverter.convert(quote,base,amount)
    except ConvertExeption as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception:
        bot.reply_to(message, f' Не удалось обработать команду\т{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

    quote_ticker, base_ticker = keys[quote], keys[base]
    r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
    total_base = json.loads(r.content)[keys[base]]
    if total_base < 0:
        raise ApiExeption('Несуществуюшая валюта')

bot.polling()