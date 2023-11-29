"""Создаем бота и передаем ему ключ для авторизации на серверах Telegram"""

import ephem
from emoji import emojize
from glob import glob
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from datetime import date
import settings
from bot_validate_planet import valid_planet_name, PlanetNameError
from random import choice, randint

# Конфигурация логирования, настройка указания времени
logging.basicConfig(filename='bot.log', level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

USER_EMOJI = [':smiley_cat:', ':smiling_imp:', ':panda_face:', ':dog:']

answer_var = ['Не знаю такой команды. Попробуй еще раз.', 'Смотри, все просто: вводишь команду /команда.']


# 'Повторите ввод в формате: /planet <имя планеты>.', 'Может день такой. Просто.. /planet планета']



def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(USER_EMOJI)
        return emojize(smile, use_aliases=True)
    return user_data['emoji']


def greet_user(update, context):  # update - аргумент - с информацией, пришедшей с платформы Telegram, context - ?
    logging.info('Вызван /start')
    logging.info(update)
    context.user_data['emoji'] = smile = get_smile(context.user_data)

    update.message.reply_text(
        f"Привет, {context.user_data['emoji']}!\n"
        f"Я умею говорить в какой констелляции сейчас находится та или иная планета нашей солнечной системы (команда /planet название планеты).\n"
        f"Могу показать схему созвездий звездного неба (команда /star_map), или основных констелляций (/const).\n"
        f"P.S.: про Землю не спрашивай, мы с нее смотрим.\nА... забыл.. еще умею играть в угадай число. Команда /guess число.")


def play_random_number(user_number):
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
        message = f'Ваше число {user_number}, мое {bot_number}, вы выиграли.'
        picture = glob('images/num_game/win.jpg')
    elif user_number < bot_number:
        message = f'Ваше число {user_number}, мое {bot_number}, я выиграл.'
        picture = glob('images/num_game/loos.jpeg')
    else:
        message = f'Числа равны. Ничья.'
        picture = glob('images/num_game/eval.jpeg')
    logging.info(picture)
    return message, picture


def guess_number(update, context):
    logging.info(f'Контекст содержит {context.args}')
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_number(user_number)[0]
            logging.info(message)
            picture = play_random_number(user_number)[1]
            chat_id = update.effective_chat.id
        except (TypeError, ValueError):
            message = 'Это не число. Давай все сначала.'
    else:
        message = 'Повтори команду с введенным числом.'
    update.message.reply_text(message)
    context.bot.send_photo(chat_id=chat_id, photo=open(picture, 'rb'), caption=message)


def planet_func(update, context):
    text = update.message.text
    logging.info(update)
    logging.info(f'Тут про контекст - {context.args}')
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


def star_map_picture(update, context):
    star_map_list = glob('images/im_star_map/star*.*')
    chat_id = update.effective_chat.id
    logging.info(star_map_list)
    logging.info(chat_id)
    for photo in star_map_list:
        context.bot.send_photo(chat_id=chat_id, photo=open(photo, 'rb'))


def const_picture(update, context):
    const_pictures = glob('images/im_const/im_const_*.jpg')
    chat_id = update.effective_chat.id
    logging.info(const_pictures)
    logging.info(chat_id)
    picture = choice(const_pictures)
    context.bot.send_photo(chat_id=chat_id, photo=open(picture, 'rb'))


def talk_to_me(update, context):
    text = update.message.text
    logging.info(text)
    update.message.reply_text(choice(answer_var))


def main():
    ''' Основная функция бота, описывающая его команды '''
    mybot = Updater(settings.API_KEY)  # , use_context=True, request_kwargs=PROXY) не работает
    dp = mybot.dispatcher  # сокращаем запись
    # Добавим в перечень существующих команд команду start, вызывающую функция greet_user
    dp.add_handler(CommandHandler('start', greet_user))
    # Добавим в перечень существующих команд guess, вызывающую функцию guess_number
    dp.add_handler(CommandHandler('guess', guess_number))

    # Добавим команду star_map, вызывающую функцию star_map_picture
    dp.add_handler(CommandHandler('star_map', star_map_picture))

    # Добавим команду, вызывающую функцию const_picture
    dp.add_handler(CommandHandler('const', const_picture))

    # Добавим обработчика планет
    dp.add_handler(CommandHandler('planet', planet_func))
    logging.info('Бот стартовал')
    # Добавим в перечень поддерживаемых действий работу с текстом. Вызывает функцию text, talk_to_me
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()  # Запрашивает обновления с telegram
    mybot.idle()  # Запускаем бота, он будет работать, пока мы его не остановим принудительно


if __name__ == '__main__':
    main()
