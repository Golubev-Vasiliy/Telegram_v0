import const
import logging
import random
import glob
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(funcName)s', level=logging.INFO)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a fucking bot, please talk to me!\n"
                                                          "I know only one command because I am very stupid!\n"
                                                          "    /music")


def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sorry man, you must use special commands for conversation "
                                                          "with me!\n Write /help for receive a help.")


def help(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="You can use next commands:\n"
                                                          "    /music")


def caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.send_message(chat_id=update.message.chat_id, text=text_caps)


def music(bot, update):
    filename = str(random.randint(1, 3))
    filename_music = filename + ".mp3"
    filename_photo = filename + ".jpg"
    bot.send_message(chat_id=update.message.chat_id, text="Music for Russian\n Wait please!")
    bot.send_audio(chat_id=update.message.chat_id, audio=open(filename_music, 'rb'), duration=20, timeout=60)
    bot.send_photo(chat_id=update.message.chat_id, photo=open(filename_photo, 'rb'))


def music_list(bot, update):
    glob_list = glob.glob('music\\*.mp3')
    mus = ""
    for songs in glob_list:
        print(songs)
        mus += songs.split("\\", 1)[1] + "\n"
    bot.send_message(chat_id=update.message.chat_id, text=mus)


def photo(bot, update):
    filename = "2.jpg"
    bot.send_message(chat_id=update.message.chat_id, text=filename)
    bot.send_photo(chat_id=update.message.chat_id, photo=open(filename, 'rb'))


def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command")


def main():
    updater = Updater(const.token)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    echo_handler = MessageHandler(Filters.text, echo)
    caps_handler = CommandHandler('caps', caps, pass_args=True)
    music_handler = CommandHandler('music', music)
    music_list_handler = CommandHandler('musicList', music_list)
    photo_handler = CommandHandler('photo', photo)
    unknown_handler = MessageHandler(Filters.command, unknown)

    # добавление обработчиков
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(caps_handler)
    dispatcher.add_handler(music_handler)
    dispatcher.add_handler(music_list_handler)
    dispatcher.add_handler(photo_handler)
    dispatcher.add_handler(unknown_handler)

    # запуск работы обработчиков
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()








