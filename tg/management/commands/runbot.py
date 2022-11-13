from django.core.management.base import BaseCommand, CommandError
from telegram.ext import (messagequeue as mq, Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler)
from telegram.utils.request import Request
from ...mqbot import MQBot
from django.conf import settings

from ...views import start, message_handler, video_handler, photo_handler, audio_handler


class Command(BaseCommand):
    help = 'Bot'

    def handle(self, *args, **options):
        q = mq.MessageQueue(all_burst_limit=3, all_time_limit_ms=3000)
        request = Request(con_pool_size=36)

        bot = MQBot(settings.TOKEN_KEY, request=request, mqueue=q)
        updater = Updater(bot=bot, use_context=True, workers=32)

        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
        dispatcher.add_handler(MessageHandler(Filters.video, video_handler))
        dispatcher.add_handler(MessageHandler(Filters.photo, photo_handler))
        dispatcher.add_handler(MessageHandler(Filters.audio, audio_handler))

        updater.start_polling()
        updater.idle()
