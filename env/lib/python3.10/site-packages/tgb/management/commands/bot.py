from email.policy import default
from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater
from telegram.utils.request import Request
import datetime
import time
import threading

from tgb.models import Profile, Message


def log_errors(f):

    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'error: {e}'
            print(error_message)
            raise e

    return inner


@log_errors
def do_echo(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text

    p, _ = Profile.objects.get_or_create(
        user_id=chat_id,
        defaults={
            'name': update.message.from_user.first_name,
            'user_name': update.message.from_user.username
        }
    )

    reply_text = 'Мы сохранили вот эти ваши данные:\n'\
        'ваш ID = {}\n\nваш first_name = {}\n\nваш username = {}'.format(chat_id, 
                                                                        update.message.from_user.first_name, 
                                                                        update.message.from_user.username)
    update.message.reply_text(
        text=reply_text,
    )


@log_errors
def smm(bot):
    while True:
        messages = Message.objects.all()
        profiles = Profile.objects.all()

        for i in messages:
            # print(i.when_message.strftime('%Y-%m-%d %H:%M' + ':00'))
            if i.when_message.strftime('%Y-%m-%d %H:%M' + ':00') == datetime.datetime.now().strftime('%Y-%m-%d %H:%M' + ':00'):
                if i.for_all:
                    for j in profiles:
                        reply_text = i.message_text
                        bot.send_message(j.user_id, reply_text)

        # print(datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M' + ':00'))
        # bot.send_message(621782148, datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M' + ':00'))
        time.sleep(60)


class Command(BaseCommand):
    help = 'telegram-bot'

    def handle(self, *args, **options):
        request = Request(
            connect_timeout=0.5,
            read_timeout=1.0,
        )
        bot = Bot(
            request=request,
            token=settings.TOKEN,
            # base_url=settings.PROXY_URL,
        )
        print(bot.get_me())

        updater = Updater(
            bot=bot,
            use_context=True,
        )
        
        message_handler = MessageHandler(Filters.text, do_echo)
        updater.dispatcher.add_handler(message_handler)

        threading.Thread(target=smm, args=(bot,)).start()
        
        updater.start_polling()
        updater.idle()