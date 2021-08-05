import telebot
from extensions import APIException, CryptoConverter
from config import keys, TOKEN


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def assistance(message: telebot.types.Message):
    text = 'Чтобы начать работу необходимо отправить сообщение в следующем формате:\n' \
           '<целевая валюта> <исходная валюта> <сумма перевода>\n' \
           'Увидеть список доступных валют: /values'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты:\n"
    for key in keys.keys():
        text += key + '\n'
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        params = message.text.split(' ')

        if len(params) != 3:
            raise APIException("Кол-во параметров должно быть равно 3!")

        base, quote, amount = params

        total_result = CryptoConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.send_message(message.chat.id, f"Ошибка пользователя\n{e}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Не удалось обработать команду\n{e}")
    else:
        text = f"{amount} {base} = {total_result} {quote}"
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
