from datetime import datetime
from django.conf import settings
from telegram import bot

from tg.models import Post, Users

BOT = bot.Bot(settings.TOKEN_KEY)


def send_post_to_channel():
    today = datetime.today().date()
    posts = Post.objects.filter(send_post=False, send_time__date=today, is_active=True).order_by("pk")
    if posts:
        for post in posts:
            caption = ""
            if post.caption:
                caption = post.caption

            if post.post_type == 1:
                try:
                    BOT.send_photo(chat_id=post.channel, photo=post.file_id, caption=caption, parse_mode='HTML')
                except Exception as e:
                    print("error send image post e=", e)
            elif post.post_type == 2:
                try:
                    BOT.send_video(chat_id=post.channel, video=post.file_id, caption=caption, parse_mode='HTML')
                except Exception as e:
                    print("error send video post e=", e)
            elif post.post_type == 3:
                try:
                    BOT.send_audio(chat_id=post.channel, audio=post.file_id, caption=caption, parse_mode='HTML')
                except Exception as e:
                    print("error send audio post e=", e)
            elif post.post_type == 4:
                try:
                    BOT.send_message(chat_id=post.channel, text=caption, parse_mode='HTML')
                except Exception as e:
                    print("error send message post e=", e)
