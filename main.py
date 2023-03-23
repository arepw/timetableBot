import os
import telebot
from alchemy import session, Entry
from scrapper.schedule_scrapper import get_schedule_current


bot = telebot.TeleBot(os.getenv('TG_TOKEN'))


@bot.message_handler(commands=["start"])
def bot_start(m, res=False):
    bot.send_message(m.chat.id, '<b>Привет!</b>\nНапиши /timetable чтобы получить расписание на сегодня!'
                                '\nРасписание <i>обновляется каждые 30 минут,</i> следовательно актуально'
                                ' даже при внезапных изменениях 🤩',
                     parse_mode='HTML'
                     )


@bot.message_handler(commands=["timetable"])
def get_schedule(m):
    bot.send_photo(m.chat.id, photo=open('schedule.png', 'rb'),
                   caption=f'Лови расписание!\nИ не вздумай прогуливать 😏\n\n<b>Последнее обновление:\n'
                           f'{session.query(Entry).first().time}</b>',
                   parse_mode='HTML'
                   )


# If there is no schedule.png on bot startup
def get_schedule_on_startup():
    if not os.path.exists(fr'{os.getcwd()}/schedule.png'):
        print('No schedule.png detected in cwd.\nStarting scrapper, usually it takes ~20 seconds.')
        get_schedule_current()
        print('Success!')


if __name__ == '__main__':
    get_schedule_on_startup()
    bot.polling(none_stop=True, interval=0)
