import const
import additional
import logging
import random
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import eyed3
import os
import shutil
from telegram import ReplyKeyboardMarkup
from re import search
import mutagen


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(funcName)s', level=logging.INFO)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a fucking bot, please talk to me!\n"
                                                          "I very like Russian rap.\n"
                                                          "    /find - Send me this command and look on the result\n"
                                                          "    /music - Beautiful track's for my friends\n"
                                                          "    /help - I can help you")


def echo(bot, update):
    button = []
    error = "You sent me a shit"
    output = "you don't write new output"
    print(update.message.text)
    search_author = search('[\w\s&\(\)\.]*', update.message.text)
    if search_author:
        author = search_author.group(0)
        print(author)
        search_album = search('(?<=\\\)[\w\s]*(?=\\\?)', update.message.text)
        if search_album:
            album = search_album.group(0)
            print(album)
            search_song = search('(?<=\\\)[\w\s\.\(\)-]*\.mp3$', update.message.text)
            if search_song:
                song = search_song.group(0)
                print(song)
                path = "music\\" + author + "\\" + album + "\\" + song
                bot.send_message(chat_id=update.message.chat_id, text="Wait please")
                bot.send_audio(chat_id=update.message.chat_id, audio=open(path, 'rb'), duration=5, timeout=60)
            else:
                path = "music\\" + author + "\\" + album
                try:
                    songs_list = os.listdir(path)
                    output = "Choose Song:"
                    for song in songs_list:
                        list = author + "\\" + album + "\\" + song
                        button.append([list])
                    keyboard = ReplyKeyboardMarkup(button, one_time_keyboard=True)
                except FileNotFoundError:
                    bot.send_message(chat_id=update.message.chat_id, text=error)
        else:
            path = "music\\" + author
            try:
                album_list = os.listdir(path)
                output = "Choose album:"
                for album in album_list:
                    list = author + "\\" + album
                    button.append([list])
                keyboard = ReplyKeyboardMarkup(button, one_time_keyboard=True)
            except FileNotFoundError:
                bot.send_message(chat_id=update.message.chat_id, text=error)
    else:
        output = "What you send me?"
    try:
        bot.send_message(chat_id=update.message.chat_id, text=output, reply_markup=keyboard)
    except:
        pass

def help(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="You can use next commands:\n"
                                                          "I like listen new music and if you send me music, that "
                                                          "I don't know, I add this song in my music library\n"
                                                          "    /find - I show you a new keyboard and you can choose "
                                                          "something in the interactive mode\n"
                                                          "    /music - If you sent me only command, then I send you one"
                                                          " of most popular Russian track. If you sent me command and "
                                                          "path, then I send you track on the this path\n"
                                                          "path has format: author\\album\song.mp3\n"
                                                          "    /help - I can help you")


def music(bot, update, args):
    if args:
        path = ""
        for part in args:
            path += part + " "
        try:
            filename_music = "music\\" + path
            print(filename_music)
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


def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command")


def analyze_mp3(bot, update, args):
    music_info = mutagen.File(str(args))
    info = music_info.tags.pprint()
    print(info)
    rec_author = search('(?<=(ART=|PE1=)).*', info).group(0)
    rec_album = search('(?<=(alb=|ALB=)).*', info).group(0)
    rec_song = search('(?<=(nam=|IT2=)).*', info).group(0)
    path = rec_author + "\\" + rec_album + "\\" + rec_song
    author_dir = os.listdir("music\\")
    found_author = False
    print(author_dir)
    for author in author_dir:
        if author == rec_author:
            found_author = True
    if found_author:
        path = "music\\" + rec_author + "\\"
        album_dir = os.listdir(path)
        found_album = False
        print(album_dir)
        for album in album_dir:
            if album == rec_album:
                found_album = True
        if found_album:
            path = "music\\" + rec_author + "\\" + rec_album
            songs_list = os.listdir(path)
            found_song = False
            print(songs_list)
            for song in songs_list:
                try:
                    path = "music\\" + rec_author + "\\" + rec_album + "\\" + song
                    new_song = mutagen.File(path)
                    new_song = search('(?<=(nam=|IT2=)).*', info).group(0)
                    if rec_song == new_song:
                        found_song = True
                except OSError:
                    print(OSError)
            if found_song:
                way = "I have this song"
            else:
                dst_path = "music\\" + rec_author + "\\" + rec_album + "\\" + rec_song + ".mp3"
                shutil.copyfile("".join(args), dst_path)
                way = "I know this author and album, but i don't have this song"
        else:
            print("i'm here")
            path_album = "music\\" + rec_author + "\\" + rec_album
            os.mkdir(path_album)
            dst_path = "music\\" + rec_author + "\\" + rec_album + "\\" + rec_song + ".mp3"
            shutil.copyfile("".join(args), dst_path)
            way = "I know this author, but i don't have this album and song"
    else:
        path_author = "music\\" + rec_author
        os.mkdir(path_author)
        path_album = "music\\" + rec_author + "\\" + rec_album
        print(path_album)
        os.mkdir(path_album)
        dst_path = "music\\" + rec_author + "\\" + rec_album + "\\" + rec_song + ".mp3"
        shutil.copyfile("".join(args), dst_path)
        way = "i don't know this author"
    bot.send_message(chat_id=update.message.chat_id, text=way)


def save_music(bot, update):
    save_file = bot.getFile(file_id=update.message.audio.file_id)
    title = update.message.audio.title
    print(title)
    save_file.download()
    print(save_file.file_path)
    title_base = search('(?<=music/).*\.(mp3|m4a)$', save_file.file_path)
    title_on_the_server = title_base.group(0)
    print(title_on_the_server)
    music_info = mutagen.File(title_on_the_server)
    info = music_info.tags.pprint()
    print(info)
    author = search('(?<=(ART=|PE1=)).*', info).group(0)
    album = search('(?<=(alb=|ALB=)).*', info).group(0)
    song = search('(?<=(nam=|IT2=)).*', info).group(0)
    path = author + "\\" + album + "\\" + song
    print(path)
    print(type(info))
    analyze_mp3(bot, update, title_on_the_server)
    os.remove(title_on_the_server)
    bot.send_message(chat_id=update.message.chat_id, text=path)


def find(bot, update):
    button = []
    path = "music\\"
    list_author = os.listdir(path)
    for author in list_author:
        button.append([author])
    keyboard = ReplyKeyboardMarkup(button, one_time_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, text="Custom keyboard", reply_markup=keyboard)


def main():
    updater = Updater(const.token)
    dispatcher = updater.dispatcher

    # main handler
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    echo_handler = MessageHandler(Filters.text, echo)
    music_handler = CommandHandler('music', music, pass_args=True)
    analyze_mp3_handler = CommandHandler('analyze', analyze_mp3, pass_args=True)
    save_music_handler = MessageHandler(Filters.audio, save_music)
    find_handler = CommandHandler('find', find)
    unknown_handler = MessageHandler(Filters.command, unknown)

    # additional handler
    photo_handler = CommandHandler('photo', additional.photo)
    music_list_handler = CommandHandler('musiclisttest', additional.music_list_test, pass_args=True)
    caps_handler = CommandHandler('caps', additional.caps, pass_args=True)
    bd_music_handler = CommandHandler('bdmusic', additional.bd_music, pass_args=True)

    # main dispatcher
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(music_handler)
    dispatcher.add_handler(analyze_mp3_handler)
    dispatcher.add_handler(save_music_handler)
    dispatcher.add_handler(find_handler)
    dispatcher.add_handler(unknown_handler)

    # additional dispatcher
    dispatcher.add_handler(bd_music_handler)
    dispatcher.add_handler(music_list_handler)
    dispatcher.add_handler(photo_handler)
    dispatcher.add_handler(caps_handler)

    # Start work dispatcher
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()