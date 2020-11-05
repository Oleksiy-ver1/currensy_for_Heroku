import json
import telebot
from parser_bot import Parser
import os

with open(f'{os.path.dirname(os.path.abspath(__file__))}/config.json','r') as f:  # Считываем данные из конфиг.
    # os.path.dirname - получение папки из полного пути os.path.abspath(__file__) - получение полного пути для запущеного файла
     config = json.load(f)

help_msg = 'телебот показывает курс валют в обменнике Обмен 24. Сам обменник работает кругласуточно и находится на ул. Сачко 5'
button1 = 'USD/UAH - EUR/UAH'
button2 = 'other currency'
button3 = 'Addres'
button4 = 'Phone'
parser = Parser(config["url"])  # Создаем экземпляр класса Parser и передаем ему url из конфига
bot = telebot.TeleBot(config["token"])

keyboard1 = telebot.types.ReplyKeyboardMarkup()  # создаем клавиатуру
keyboard1.row(button1, button2)
keyboard1.row(button3, button4)


# Обработчик команд '/start' и
@bot.message_handler(commands=['start'])
def handle_start_help(message):
    bot.send_message(message.chat.id, "Курс валют в Каменском. Используй клавиатуру под окошком сообщений.",
                     reply_markup=keyboard1)  # выведет ответет


# '/help'.
@bot.message_handler(commands=['help'])
def handle_start_help(message):
    bot.reply_to(message, help_msg)  # повторит принятое сообщение и выведет ответет


@bot.message_handler(content_types=["sticker"])  # при втправке стикера
def sticker_got(message):
    # bot.send_message(message.chat.id, message)
    print(message)


@bot.message_handler(content_types=["text"])
def seng_text(message):
    if message.text.lower() == "привет":  # весь текст с маленькой буквы
        bot.send_message(message.chat.id, 'Привет-медвед!')
    if message.text.lower() == "i love you":
        file_id = 'CAACAgIAAxkBAANNX4l8JPW7U4mE4cJZYb24i9FLRkUAArAFAAJjK-IJvDIz3H7MRNQbBA'
        bot.send_sticker(message.chat.id, file_id)
    if message.text.lower() == "курс":
        bot.send_message(message.chat.id, "доллар/гривна " + parser.course.get('USD/UAH'))
    if message.text == button1:
        bot.send_message(message.chat.id,
                         "доллар/гривна " + parser.course.get('USD/UAH') + '   ' + "евро/гривна " + parser.course.get(
                             'EUR/UAH'))
    if message.text == button2:
        text_all_course=json.dumps(parser.course, indent=1, ensure_ascii=False).replace('{','').replace('}','')
        bot.send_message(message.chat.id, text_all_course)
    if message.text == button3:
        bot.send_message(message.chat.id, parser.address)
    if message.text == button4:
        bot.send_message(message.chat.id,
                         str(parser.phones).replace('[', '').replace(']', '').replace("'", "").replace('tel:', ''))

    # else:
    #     bot.send_message(message.chat.id, "используй клавиатуру")


# Теперь запустим бесконечный цикл получения новых записей со стороны Telegram:
if __name__ == '__main__':
    bot.polling(none_stop=True)
