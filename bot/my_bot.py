"""Создаем бота и передаем ему ключ для авторизации на серверах Telegram"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import ephem
from datetime import date
import settings
from bot_validate_planet import valid_planet_name, PlanetNameError
from random import choice

# Конфигурация логирования, настройка указания времени
logging.basicConfig(filename='bot.log', level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

PROXY = {
    'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {
        'username': settings.PROXY_USERNAME,
        'password': settings.PROXY_PASSWORD
    }}

answer_var = ['Не знаю такой команды. Попробуй еще раз.', 'Смотри, все просто: вводишь команду /planet потом пробел и название планеты.',
              'Повторите ввод в формате: /planet <имя планеты>.', 'Может день такой. Просто.. /planet планета']

def greet_user(update, context):  # update - аргумент - с информацией, пришедшей с платформы Telegram, context - ?
    logging.info('Вызван /start')
    logging.info(update)
    update.message.reply_text(
        'Привет! Я умею говорить в какой констелляции сейчас находится та или иная планета нашей солнечной системы. '
        'Можешь спросить меня командой /planet название планеты. P.S.: про Землю не спрашивай.')


def talk_to_me(update, context):
    text = update.message.text
    logging.info(text)
    update.message.reply_text(choice(answer_var))


def planet_func(update, context):
    text = update.message.text
    try:
        planet = valid_planet_name(text)
    except PlanetNameError as err:
        logging.info(err)
        update.message.reply_text(str(err))
    pre_answer = getattr(ephem, planet)(date.today())
    answer = ephem.constellation(pre_answer)
    logging.info(answer)
    if planet != 'Pluto':
        txt_ans = f"На данный момент {planet.capitalize()} в констелляции: {', '.join(answer)}"
        update.message.reply_text(txt_ans)
    else:
        txt_ans = f"Плутон нынче не планета, но на данный момент он в констелляции: {', '.join(answer)}"
        update.message.reply_text(txt_ans)


def main():
    ''' Основная функция бота, описывающая его команды '''
    mybot = Updater(settings.API_KEY)  # , use_context=True, request_kwargs=PROXY) не работает
    dp = mybot.dispatcher  # сокращаем запись
    # Добавим в перечень существующих команд команду start, вызывающую функция greet_user
    dp.add_handler(CommandHandler('start', greet_user))
    # Добавим обработчика планет
    dp.add_handler(CommandHandler('planet', planet_func))
    logging.info('Бот стартовал')
    # Добавим в перечень поддерживаемых действий работу с текстом. Вызывает функцию text, talk_to_me
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()  # Запрашивает обновления с telegram
    mybot.idle()  # Запускаем бота, он будет работать, пока мы его не остановим принудительно


if __name__ == '__main__':
    main()
