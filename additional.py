import mysql.connector
import const

def caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.send_message(chat_id=update.message.chat_id, text=text_caps)


def music_list_test(bot, update, args):
    if args:
        path = "music\\" + "".join(args)
        mus = "List from " + "".join(args) + ":\n"
    else:
        path = "music\\"
        mus = "List of author:\n"
    author_dir = os.listdir(path)
    for songs in author_dir:
        mus += songs + "\n"
    bot.send_message(chat_id=update.message.chat_id, text=mus)


def photo(bot, update):
    filename = "2.jpg"
    bot.send_message(chat_id=update.message.chat_id, text=filename)
    bot.send_photo(chat_id=update.message.chat_id, photo=open(filename, 'rb'))


def bd_music(bot, update, args):
    db = mysql.connector.connect(**const.config)
    cursor = db.cursor()
    query = "SHOW TABLES"
    cursor.execute(query)
    for tables in cursor.fetchall():
        print(tables[0])
    db.close()


