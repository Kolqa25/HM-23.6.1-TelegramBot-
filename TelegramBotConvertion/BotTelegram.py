import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CurrencyConverter


bot = telebot.TeleBot(TOKEN)




@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите боту команду в следующем формате: \n<Название валюты> \
<Название валюты в которую перевести> \
<Количество переводимой валюты>\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)



@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Недопустимое количество параметров.')

        quote, base, amount = values
        total_base = CurrencyConverter.get_pice(quote.casefold(), base.casefold(), amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} : {float(total_base) * float(amount)}'
        bot.send_message(message.chat.id, text)

bot.polling()
