import telegram
from telegram.ext import Updater, MessageHandler, Filters
import minecraft.server
import logging
import os

def main():
    # إنشاء بوت Telegram
    bot = telegram.Bot(token=os.environ['6394505280:AAHVKo6X0R-BvDp6VkOSwHyEUZjJmuO1uhE'])

    # إنشاء خادم Minecraft
    server = minecraft.server.MinecraftServer()

    # إعداد تسجيل الدخول
    logging.basicConfig(level=logging.DEBUG)

    # إنشاء قاموس الأوامر
    commands = {
        '/createserver': create_server,
        '/servercontrol': control_server,
        '/players': players,
        '/allowlist': allowlist,
        '/moderators': moderators,
        '/settings': settings,
        '/restart': restart,
        '/log': log,
        '/editor': editor,
        '/world': world,
        '/change_world': change_world,
        '/install_mod': install_mod,
        '/uninstall_mod': uninstall_mod,
        '/broadcast': broadcast,
    }

    # إنشاء كائن Updater
    updater = Updater(token=os.environ['6394505280:AAHVKo6X0R-BvDp6VkOSwHyEUZjJmuO1uhE'])    

    # تعريف التابع لمعالجة الرسائل
    updater.dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

    # بدء Updater
    updater.start_polling()
    updater.idle()

def handle_message(update, context):
    chat_id = update.message.chat_id
    text = update.message.text

    # تحقق مما إذا كانت الرسالة أمرًا
    if text in commands:
        # تنفيذ الأمر
        commands[text](update, context)
    else:
        # الرسالة ليست أمرًا ، لذا أرسل رسالة إلى المستخدم
        bot = telegram.Bot(token=os.environ['6394505280:AAHVKo6X0R-BvDp6VkOSwHyEUZjJmuO1uhE'])
        bot.send_message(chat_id, 'عذرًا ، لم أفهم هذا الأمر.')

def create_server(update, context):
    chat_id = update.message.chat_id

    # اسأل المستخدم عن اسم الخادم
    bot = telegram.Bot(token=os.environ['6394505280:AAHVKo6X0R-BvDp6VkOSwHyEUZjJmuO1uhE'])
    bot.send_message(chat_id, 'ما هو اسم الخادم الذي تريده؟')

    def ask_server_name(response):
        server_name = response.message.text

        # تحقق مما إذا كان المستخدم هو المالك
        if chat_id in server.owners:
            # إنشاء خادم
            server.create_server(server_name)

            # إرسال رسالة إلى المستخدم بتأكيد إنشاء الخادم
            bot.send_message(chat_id, 'تم إنشاء الخادم {} بنجاح.'.format(server_name))
        else:
            # إرسال رسالة إلى المستخدم بأنه غير مالك
            bot.send_message(chat_id, 'لست مالكًا لهذا الخادم.')

    # تحديد التابع للاستجابة عندما يُرسل المستخدم اسم الخادم
    bot.dispatcher.add_handler(MessageHandler(Filters.text, ask_server_name))

def control_server(update, context):
    chat_id = update.message.chat_id

    # عرض قائمة أزرار للتحكم في الخادم
    buttons = [
        telegram.KeyboardButton('العالم'),
        telegram.KeyboardButton('الإعدادات'),
        telegram.KeyboardButton('اللاعبين'),
        telegram.KeyboardButton('قائمة السماح'),
        telegram.KeyboardButton('المشرفين'),
        telegram.KeyboardButton('إعادة التشغيل'),
        telegram.KeyboardButton('السجل'),
        telegram.KeyboardButton('المحرر'),
        telegram.KeyboardButton('تغيير العالم'),
        telegram.KeyboardButton('تثبيت تعديل'),
        telegram.KeyboardButton('إلغاء تثبيت تعديل'),
    ]
    reply_markup = telegram.ReplyKeyboardMarkup([buttons], one_time_keyboard=True)
    bot = telegram.Bot(token=os.environ['6394505280:AAHVKo6X0R-BvDp6VkOSwHyEUZjJmuO1uhE'])
    bot.send_message(chat_id, 'ماذا تريد أن تفعل بالخادم؟', reply_markup=reply_markup)

def players(update, context):
    chat_id = update.message.chat_id

    # عرض قائمة أزرار للتحكم في اللاعبين
    buttons = [
        telegram.KeyboardButton('قائمة السماح'),
        telegram.KeyboardButton('المشرفين'),
    ]
    reply_markup = telegram.ReplyKeyboardMarkup([buttons], one_time_keyboard=True)
    bot = telegram.Bot(token=os.environ['6394505280:AAHVKo6X0R-BvDp6VkOSwHyEUZjJmuO1uhE'])
    bot.send_message(chat_id, 'ماذا تريد أن تفعل باللاعبين؟', reply_markup=reply_markup)

def allowlist(update, context):
    chat_id = update.message.chat_id

    # اسأل المستخدم عن اسم اللاعب الذي يريد إضافته إلى قائمة السماح
    bot = telegram.Bot(token=os.environ['6394505280:AAHVKo6X0R-BvDp6VkOSwHyEUZjJmuO1uhE'])
    bot.send_message(chat_id, 'ما هو اسم اللاعب الذي تريد إضافته إلى قائمة السماح؟')

    def ask_player_name(response):
        player_name = response.message.text

        # أضف اللاعب إلى قائمة السماح
        server.add_player_to_allowlist(player_name)

        # إرسال رسالة إلى المستخدم بتأكيد إضافة اللاعب إلى قائمة السماح
        bot.send_message(chat_id, 'تم إضافة اللاعب {} إلى قائمة السماح بنجاح.'.format(player_name))

    # تحديد التابع للاستجابة عندما يُرسل المستخدم اسم اللاعب
    bot.dispatcher.add_handler(MessageHandler(Filters.text, ask_player_name))

def moderators(update, context):
    chat_id = update.message.chat_id

    # اسأل المستخدم عن اسم اللاعب الذي يريد جعله مشرفًا
    bot = telegram.Bot(token=os.environ['6394505280:AAHVKo6X0R-BvDp6VkOSwHyEUZjJmuO1uhE'])
    bot.send_message(chat_id, 'ما هو اسم اللاعب الذي تريد جعله مشرفًا؟')

    def ask_player_name(response):
        player_name = response.message.text

        # اجعل اللاعب مشرفًا
        server.make_player_moderator(player_name)

        # إرسال رسالة إلى المستخدم بتأكيد جعل اللاعب مشرفًا
        bot.send_message(chat_id, 'تم جعل اللاعب {} مشرفًا بنجاح.'.format(player_name))

    # تحديد التابع للاستجابة عندما يُرسل المستخدم اسم اللاعب
    bot.dispatcher.add_handler(MessageHandler(Filters.text, ask_player_name))

def settings(update, context):
    chat_id = update.message.chat_id

    # عرض قائمة أزرار للتحكم في الإعدادات
    buttons = [
        telegram.KeyboardButton('اسم العالم'),
        telegram.KeyboardButton('صعوبة اللعبة'),
        telegram.KeyboardButton('عدد اللاعبين الأقصى'),
        telegram.KeyboardButton('الذاكرة العشوائية (RAM)'),
        telegram.KeyboardButton('المساحة'),
    ]
    reply_markup = telegram.ReplyKeyboardMarkup([buttons], one_time_keyboard=True)
    bot = telegram.Bot(token=os.environ['6394505280:AAHVKo6X0R-BvDp6VkOSwHyEUZjJmuO1uhE'])
    bot.send_message(chat_id, 'ماذا تريد أن تفعل بالإعدادات؟', reply_markup=reply_markup)

def restart(update, context):
    chat_id = update.message.chat_id

    # أعد تشغيل الخادم
    server.restart()

    # إرسال رسالة إلى المستخدم بتأكيد إعادة تشغيل الخادم
    bot = telegram.Bot(token=os.environ['6394505280:AAHVKo6X0R-BvDp6VkOSwHyEUZjJmuO1uhE'])
    bot.send_message(chat_id, 'تم إعادة تشغيل الخادم بنجاح.')

def log(update, context):
    chat_id = update.message.chat_id

    # استعراض سجل الأحداث الخاص بالخادم
    server_log = server.get_log()

    # إرسال رسالة إلى المستخدم بسجل الأحداث
    bot = telegram.Bot(token=os.environ['6394505280:AAHVKo6X0R-BvDp6VkOSwHyEUZjJmuO1uhE'])
    bot.send_message(chat_id, 'سجل الخادم:\n{}'.format(server_log))

def editor(update, context):
    chat_id = update.message.chat_id

    # اسأل المستخدم عن الأمر الذي يرغب في تنفيذه
    bot = telegram.Bot(token=os.environ['6394505280:AAHVKo6X0R-BvDp6VkOSwHyEUZjJmuO1uhE'])
    bot.send_message(chat_id, 'أدخل الأمر الذي تريد تنفيذه:')

    def execute_command(response):
        command = response.message.text

        # تنفيذ الأمر
        server.execute_command(command)

        # إرسال رسالة إلى المستخدم بتأكيد تنفيذ الأمر
        bot.send_message(chat_id, 'تم تنفيذ الأمر {} بنجاح.'.format(command))

    # تحديد التابع للاستجابة عندما يُرسل المستخدم الأمر
    bot.dispatcher.add_handler(MessageHandler(Filters.text, execute_command))

def world(update, context):
    chat_id = update.message.chat_id

    # عرض قائمة أزرار للتحكم في العالم
    buttons = [
        telegram.KeyboardButton('تغيير العالم'),
        telegram.KeyboardButton('تثبيت تعديل'),
        telegram.KeyboardButton('إلغاء تثبيت تعديل'),
    ]
    reply_markup = telegram.ReplyKeyboardMarkup([buttons], one_time_keyboard=True)
    bot = telegram.Bot(token=os.environ['6394505280:AAHVKo6X0R-BvDp6VkOSwHyEUZjJmuO1uhE'])
    bot.send_message(chat_id, 'ماذا تريد أن تفعل بالعالم؟', reply_markup=reply_markup)

def change_world(update, context):
    chat_id = update.message.chat_id

    # اسأل المستخدم عن ملف العالم الجديد
    bot = telegram.Bot(token=os.environ['6394505280:AAHVKo6X0R-BvDp6VkOSwHyEUZjJmuO1uhE'])
    bot.send_message(chat_id, 'ما هو ملف العالم الجديد؟')

    def ask_new_world_file(response):
        new_world_file = response.message.text

        # غير العالم
        server.change_world(new_world_file)

        # إرسال رسالة إلى المستخدم بتأكيد تغيير العالم
        bot.send_message(chat_id, 'تم تغيير العالم بنجاح.')

    # تحديد التابع للاستجابة عندما يُرسل المستخدم ملف العالم الجديد
    bot.dispatcher.add_handler(MessageHandler(Filters.text, ask_new_world_file))

def install_mod(update, context):
    chat_id = update.message.chat_id

    # اسأل المستخدم عن ملف التعديل
    bot = telegram.Bot(token=os.environ['6394505280:AAHVKo6X0R-BvDp6VkOSwHyEUZjJmuO1uhE'])
    bot.send_message(chat_id, 'ما هو ملف التعديل؟')

    def ask_mod_file(response):
        mod_file = response.message.text

        # تثبيت التعديل
        server.install_mod(mod_file)

        # إرسال رسالة إلى المستخدم بتأكيد تثبيت التعديل
        bot.send_message(chat_id, 'تم تثبيت التعديل بنجاح.')

    # تحديد التابع للاستجابة عندما يُرسل المستخدم ملف التعديل
    bot.dispatcher.add_handler(MessageHandler(Filters.text, ask_mod_file))

def uninstall_mod(update, context):
    chat_id = update.message.chat_id

    # اسأل المستخدم عن اسم التعديل الذي يريد إلغاء تثبيته؟
    bot = telegram.Bot(token=os.environ['6394505280:AAHVKo6X0R-BvDp6VkOSwHyEUZjJmuO1uhE'])
    bot.send_message(chat_id, 'ما هو اسم التعديل الذي تريد إلغاء تثبيته؟')

    def ask_mod_name(response):
        mod_name = response.message.text

        # إلغاء تثبيت التعديل
        server.uninstall_mod(mod_name)

        # إرسال رسالة إلى المستخدم بتأكيد إلغاء تثبيت التعديل
        bot.send_message(chat_id, 'تم إلغاء تثبيت التعديل بنجاح.')

    # تحديد التابع للاستجابة عندما يُرسل المستخدم اسم التعديل
    bot.dispatcher.add_handler(MessageHandler(Filters.text, ask_mod_name))

def broadcast(update, context):
    chat_id = update.message.chat_id

    # اسأل المستخدم عن اسم الخادم
    bot = telegram.Bot(token=os.environ['6394505280:AAHVKo6X0R-BvDp6VkOSwHyEUZjJmuO1uhE'])
    bot.send_message(chat_id, 'ما هو اسم الخادم الذي تريد البث منه؟')

    def ask_server_name(response):
        server_name = response.message.text

        # تحقق مما إذا كان المستخدم هو المالك
        if chat_id in server.owners:
            # اسأل المستخدم عن اسم المجموعة
            bot.send_message(chat_id, 'ما هو اسم المجموعة التي تريد البث إليها؟')

            def ask_group_name(response):
                group_name = response.message.text

                # اسأل المستخدم عن رسالة البث
                bot.send_message(chat_id, 'ما هي رسالة البث؟')

                def broadcast_message(response):
                    message = response.message.text

                    # قم بإجراء البث
                    server.broadcast(server_name, group_name, message)

                    # إرسال رسالة إلى المستخدم بتأكيد البث
                    bot.send_message(chat_id, 'تم البث بنجاح.')

                # تحديد التابع للاستجابة عندما يُرسل المستخدم رسالة البث
                bot.dispatcher.add_handler(MessageHandler(Filters.text, broadcast_message))

            # تحديد التابع للاستجابة عندما يُرسل المستخدم اسم المجموعة
            bot.dispatcher.add_handler(MessageHandler(Filters.text, ask_group_name))
        else:
            # إرسال رسالة إلى المستخدم بأنه غير مالك
            bot.send_message(chat_id, 'لست مالكًا لهذا الخادم.')

    # تحديد التابع للاستجابة عندما يُرسل المستخدم اسم الخادم
    bot.dispatcher.add_handler(MessageHandler(Filters.text, ask_server_name))


if __name__ == '__main__':
    main()
