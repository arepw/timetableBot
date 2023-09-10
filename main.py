import os
import datetime
import telebot
from scrapper.schedule_scrapper import get_schedule_current
from redis import Redis

bot = telebot.TeleBot(os.getenv('TG_TOKEN'))

redis = Redis(host='redis')

# Vladivostok time delta
time_delta = datetime.timedelta(hours=10, minutes=0)


def set_last_update_time() -> str:
    # Current time
    time = datetime.datetime.now(datetime.timezone.utc) + time_delta
    time = time.strftime("%m-%d %H:%M:%S")

    redis.set('schedule_last_update', str(time))
    return 'OK'


@bot.message_handler(commands=["start"])
def bot_start(m, res=False):
    bot.send_message(m.chat.id, f'<b>Привет!</b>\nНапиши /this_week чтобы получить расписание на эту неделю!'
                                f'\nИли /next_week - расписание на следущую неделю)'
                                f'\nРасписание <i>обновляется каждые {int(int(os.getenv("UPDATE_RATE")) / 60)} минут,</i>'
                                f' следовательно актуально даже при внезапных изменениях 🤩',
                     parse_mode='HTML'
                     )


@bot.message_handler(commands=["this_week"])
def get_schedule_this(m):
    try:
        bot.send_photo(m.chat.id, photo=open('schedule.png', 'rb'),
                       caption=f'Расписание на эту неделю.\n\n<b>Последнее обновление:\n'
                               f'{redis.get("schedule_last_update").decode("utf8")}</b>',
                       parse_mode='HTML'
                       )
    except OSError:
        bot.send_message(m.chat.id, text='Ошибка получения расписания.')


@bot.message_handler(commands=["next_week"])
def get_schedule_next(m):
    try:
        bot.send_photo(m.chat.id, photo=open('schedule-next.png', 'rb'),
                       caption=f'Расписание на следующую неделю.\n\n<b>Последнее обновление:\n'
                               f'{redis.get("schedule_last_update").decode("utf8")}</b>',
                       parse_mode='HTML'
                       )
    except OSError:
        bot.send_message(m.chat.id,
                         text='Ошибка получения расписания. '
                              'Возможно, в личном кабинете нет расписания на следующую неделю.'
                         )


def get_schedule_on_startup():
    """ If there is no schedule.png on bot startup it will run the scrapper. """
    if not os.path.exists(fr'{os.getcwd()}/schedule.png'):
        print('No schedule.png detected in cwd.\nStarting scrapper, usually it takes ~20 seconds.')
        get_schedule_current()
        print('Success!')


if __name__ == '__main__':
    get_schedule_on_startup()
    set_last_update_time()
    bot.polling(none_stop=True, interval=0)
