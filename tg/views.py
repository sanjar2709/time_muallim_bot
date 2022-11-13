from datetime import datetime, timedelta
import time
from telegram import ReplyKeyboardMarkup, BotCommand, ReplyKeyboardRemove
from .models import Users, Post
from .userlog import UserLog


def go_message(context, user_id, message, reply_murkup):
    context.bot.send_message(chat_id=user_id, text=message, reply_markup=reply_murkup, parse_mode='HTML',
                             disable_web_page_preview=True)


def delete_message_user(context, user_id, message_id):
    context.bot.delete_message(chat_id=user_id, message_id=message_id)


def start(update, context):
    user_data = update.message.from_user
    user = Users.objects.filter(tg_id=user_data.id).first()
    if not user:
        try:
            first_name = user_data.first_name
        except:
            first_name = "User"
        Users.objects.create(tg_id=user_data.id, first_name=first_name).save()

    message = "<b>🤖 Men Media Filelarni vaqtga moslab kanalga tashlovchi botman.</b>\n\n🕔 Meni afzalligim shundaki menga yuzlab media filelarni tashlasangiz men ularni hammasini bitta vaqtga moslab har kuni kanalizga tashlab beraman!"
    button = [
        ["🧾 Post Joylash"]
    ]
    go_message(context=context, user_id=user_data.id, message=message,
               reply_murkup=ReplyKeyboardMarkup(button, one_time_keyboard=True, resize_keyboard=True))
    return 1


def message_handler(update, context):
    command = [BotCommand("start", "Boshlash")]
    context.bot.set_my_commands(command)

    user_data = update.message.from_user
    text = update.message.text

    user_log = UserLog(user_data.id)
    user_state = user_log.get_log()

    if text == "🧾 Post Joylash":
        user_log.clear_log()
        user_state.update({'menu_state': 1, 'state': 100, 'index': 0})
        user_log.change_log(user_state)

    menu_state = user_state.get("menu_state", 0)
    state = user_state.get("state", 0)

    if menu_state == 1:
        if state == 100:
            user_state.update({'state': 101})
            user_log.change_log(user_state)

            button = [[
                "🧾 Tugadi"
            ]]
            message = "<b>Media filelaringizni tartib bilan tashlang</b> 👇\n\nAgar media filelaringizni tashlab bo'lsangiz\n<b>🧾 Tugadi</b> Tugmasini bosing 👇"
            go_message(context=context, user_id=user_data.id, message=message,
                       reply_murkup=ReplyKeyboardMarkup(button, one_time_keyboard=True, resize_keyboard=True))
            return 1

        elif state == 101 and text == "🧾 Tugadi":
            user_state.update({'state': 102})
            user_log.change_log(user_state)
            message = "<b>Media filelar tashlaydigan kanal silkasini jo'nating 👇\nMisol:</b> @kunuzofficial\n\n<b>Siz tashlagan kanalda men admin bo'lishim shart ❗</b>"
            go_message(context=context, message=message, user_id=user_data.id, reply_murkup=ReplyKeyboardRemove())
            return 1
        elif state == 101:
            user = Users.objects.filter(tg_id=user_data.id).first()
            Post.objects.create(
                file_id="--",
                caption=text,
                post_type=4,
                user=user,
                is_active=False,
                send_post=False
            ).save()
            return 1
        elif state == 102:
            user_state.update({'state': 103, "channel": text})
            user_log.change_log(user_state)
            message = "<b>Xabar yuboradigan vaqtni boshlanishini jo'nating 👇.\nMisol:</b> 15.11.2022 14:00\n\nMisol uchun 15.11.2022 14:00 tashlasangiz 15-noyabrdan boshlab har kuni 14:00 da menga tashlagan xabarlaringizni kanalizga tashlab beraman."
            go_message(context=context, user_id=user_data.id, message=message, reply_murkup=None)
            return 1

        elif state == 103:
            date = date_check(text)
            if date:
                user_state.update({"state": 104, "date": text})
                user_log.change_log(user_state)
                message = f"<b>Malumotlaringiz to'g'rimi? 👇</b>\n\n<b>Kanal:</b> {user_state.get('channel', '')}\n<b>Vaqt:</b> {date}"
                button = [
                    ["✅ Ha", "❌ Yoq"]
                ]
                go_message(context=context, user_id=user_data.id, message=message,
                           reply_murkup=ReplyKeyboardMarkup(button, one_time_keyboard=True, resize_keyboard=True))
            else:
                message = "<b>❌❗️Xatolik. Sana va vaqtni to'g'ri kiriting.\n\nMisol:</b> 15.11.2022 14:00 (15-noyabrdan boshlab har kuni 14:00 da)"
                go_message(context=context, user_id=user_data.id, message=message, reply_murkup=ReplyKeyboardRemove())
                return 1

        elif state == 104:
            if text == "✅ Ha":
                date = date_check(user_state.get("date", ''))
                channel = user_state.get("channel", "")

                posts = Post.objects.filter(user__tg_id=user_data.id, is_active=False, send_post=False).order_by("id")
                if posts:
                    for i, post in enumerate(posts, start=0):
                        date = date + timedelta(days=1 if i != 0 else 0)

                        post.is_active = True
                        post.channel = channel
                        post.send_time = date
                        post.save()

                user_log.clear_log()

                button = [
                    ["🧾 Post Joylash"]
                ]
                message = "<b>✅ Sizning postlaringiz haqidagi malumotlar muvaffaqiyatli saqlandi.\nMen ularni vaqti vaqti bilan kanalingizga joylab boraman.</b>"
                go_message(context=context, user_id=user_data.id, message=message,
                           reply_murkup=ReplyKeyboardMarkup(button, one_time_keyboard=True, resize_keyboard=True))

                return 1
            elif text == "❌ Yoq":
                user_log.clear_log()
                message = "<b>Sizning barcha media filelaringiz o'chirib tashlandi.</b>"

                posts = Post.objects.filter(user__tg_id=user_data.id, is_active=False, send_post=False)
                posts.delete()
                button = [
                    ["🧾 Post Joylash"]
                ]
                go_message(context=context, user_id=user_data.id, message=message,
                           reply_murkup=ReplyKeyboardMarkup(button, one_time_keyboard=True, resize_keyboard=True))
                return 1


def video_handler(update, context):
    user_data = update.message.from_user

    user_log = UserLog(user_data.id)
    user_state = user_log.get_log()

    menu_state = user_state.get("menu_state", 0)
    state = user_state.get("state", 0)

    if menu_state == 1:
        if state == 101:
            user = Users.objects.filter(tg_id=user_data.id).first()

            caption = update.message.caption
            file_id = update.message.video.file_id
            Post.objects.create(
                file_id=file_id,
                caption=caption,
                post_type=2,
                user=user,
                is_active=False,
                send_post=False
            ).save()


def photo_handler(update, context):
    user_data = update.message.from_user

    user_log = UserLog(user_data.id)
    user_state = user_log.get_log()

    menu_state = user_state.get("menu_state", 0)
    state = user_state.get("state", 0)

    if menu_state == 1:
        if state == 101:
            user = Users.objects.filter(tg_id=user_data.id).first()

            caption = update.message.caption
            file_id = update.message.photo[-1].file_id
            Post.objects.create(
                file_id=file_id,
                caption=caption,
                post_type=1,
                user=user,
                is_active=False,
                send_post=False
            ).save()


def audio_handler(update, context):
    user_data = update.message.from_user

    user_log = UserLog(user_data.id)
    user_state = user_log.get_log()

    menu_state = user_state.get("menu_state", 0)
    state = user_state.get("state", 0)

    if menu_state == 1:
        if state == 101:
            user = Users.objects.filter(tg_id=user_data.id).first()

            caption = update.message.caption
            file_id = update.message.audio.file_id

            Post.objects.create(
                file_id=file_id,
                caption=caption,
                post_type=3,
                user=user,
                is_active=False,
                send_post=False
            ).save()


def date_check(date):
    date_format = '%d.%m.%Y %H:%M'
    try:
        datetime_obj = datetime.strptime(date, date_format)
        return datetime_obj
    except ValueError:
        return False
