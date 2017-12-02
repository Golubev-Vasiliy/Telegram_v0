import const
import logging
import random
import glob
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import eyed3
import mysql.connector
import os
import shutil
from re import search


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


def music(bot, update, args):
    if args:
        try:
            filename_music = "music\\" + "".join(args)
            bot.send_audio(chat_id=update.message.chat_id, audio=open(filename_music, 'rb'), duration=20, timeout=60)
            bot.send_message(chat_id=update.message.chat_id, text="".join(args))
        except FileNotFoundError:
            bot.send_message(chat_id=update.message.chat_id, text="Song not found")
    else:
        filename = str(random.randint(1, 3))
        filename_music = filename + ".mp3"
        filename_photo = filename + ".jpg"
        bot.send_message(chat_id=update.message.chat_id, text="Music for Russian guys\n Wait please!")
        bot.sendAudio(chat_id=update.message.chat_id, audio=open(filename_music, 'rb'), duration=20, timeout=60)
        bot.send_photo(chat_id=update.message.chat_id, photo=open(filename_photo, 'rb'))


def music_list(bot, update):
    glob_list = glob.glob('music\\*.mp3')
    mus = ""
    for songs in glob_list:
        mus += songs.split("\\", 1)[1] + "\n"
    bot.send_message(chat_id=update.message.chat_id, text=mus)


def photo(bot, update):
    filename = "2.jpg"
    bot.send_message(chat_id=update.message.chat_id, text=filename)
    bot.send_photo(chat_id=update.message.chat_id, photo=open(filename, 'rb'))


def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command")


def analyze_mp3(bot, update, args):
    music_info = eyed3.load("".join(args))
    info = music_info.tag.album + "\n" + \
           str(music_info.tag.track_num[0]) + "." + \
           music_info.tag.title + "\n" + \
           music_info.tag.artist
    author_dir = os.listdir("music\\")
    found_author = False
    way = ""
    print(author_dir)
    for author in author_dir:
        if author == music_info.tag.artist:
            found_author = True
    if found_author:
        path = "music\\" + music_info.tag.artist + "\\"
        album_dir = os.listdir(path)
        found_album = False
        print(album_dir)
        for album in album_dir:
            if album == music_info.tag.album:
                found_album = True
        if found_album:
            path = "music\\" + music_info.tag.artist + "\\" + music_info.tag.album
            songs_list = os.listdir(path)
            found_song = False
            print(songs_list)
            for song in songs_list:
                path = "music\\" + music_info.tag.artist + "\\" + music_info.tag.album + "\\" + song
                new_song = eyed3.load(path)
                if music_info.tag.title == new_song.tag.title:
                    found_song = True
            if found_song:
                way = "I have this song"
            else:
                dst_path = "music\\" + music_info.tag.artist + "\\" + music_info.tag.album + "\\" + \
                           str(music_info.tag.track_num[0]) + ". " + music_info.tag.title + ".mp3"
                shutil.copyfile("".join(args), dst_path)
                way = "I know this author and album, but i don't have this song"
        else:
            print("i'm here")
            path_album = "music\\" + music_info.tag.artist + "\\" + music_info.tag.album
            os.mkdir(path_album)
            dst_path = "music\\" + music_info.tag.artist + "\\" + music_info.tag.album + "\\" + \
                       str(music_info.tag.track_num[0]) + ". " + music_info.tag.title + ".mp3"
            shutil.copyfile("".join(args), dst_path)
            way = "I know this author, but i don't have this album and song"
    else:
        path_author = "music\\" + music_info.tag.artist
        os.mkdir(path_author)
        path_album = "music\\" + music_info.tag.artist + "\\" + music_info.tag.album
        os.mkdir(path_album)
        dst_path = "music\\" + music_info.tag.artist + "\\" + music_info.tag.album + "\\" + \
                   str(music_info.tag.track_num[0]) + ". " + music_info.tag.title + ".mp3"
        shutil.copyfile("".join(args), dst_path)
        way = "i don't know this author"
    bot.send_message(chat_id=update.message.chat_id, text=way)


def bd_music(bot, update, args):
    db = mysql.connector.connect(**const.config)
    cursor = db.cursor()
    query = "SHOW TABLES"
    cursor.execute(query)
    for tables in cursor.fetchall():
        print(tables[0])
    db.close


def save_music(bot, update):
    save_file = bot.getFile(file_id=update.message.audio.file_id)
    save_file.download()
    print(save_file.file_path)
    title_base = search('(?<=music/).*\.mp3$', save_file.file_path)
    title_on_the_server = title_base.group(0)
    print(title_on_the_server)
    music_info = eyed3.load(title_on_the_server)
    info = music_info.tag.album + "\n" + \
           music_info.tag.title + "\n" + \
           music_info.tag.artist
    analyze_mp3(bot, update, title_on_the_server)
    os.remove(title_on_the_server)
    bot.send_message(chat_id=update.message.chat_id, text=info)


def main():
    updater = Updater(const.token)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    echo_handler = MessageHandler(Filters.text, echo)
    caps_handler = CommandHandler('caps', caps, pass_args=True)
    music_handler = CommandHandler('music', music, pass_args=True)
    music_list_handler = CommandHandler('musiclist', music_list)
    photo_handler = CommandHandler('photo', photo)
    analyze_mp3_handler = CommandHandler('analyze', analyze_mp3, pass_args=True)
    bd_music_handler = CommandHandler('bdmusic', bd_music, pass_args=True)
    unknown_handler = MessageHandler(Filters.command, unknown)
    save_music_handler = MessageHandler(Filters.audio, save_music)

    # добавление обработчиков
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(caps_handler)
    dispatcher.add_handler(music_handler)
    dispatcher.add_handler(music_list_handler)
    dispatcher.add_handler(photo_handler)
    dispatcher.add_handler(analyze_mp3_handler)
    dispatcher.add_handler(bd_music_handler)
    dispatcher.add_handler(unknown_handler)
    dispatcher.add_handler(save_music_handler)

    # запуск работы обработчиков
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()








