token = '452787256:AAEr8gS8I8cGpH9oAfRXIog7ip6q_XQuagk'

config = {'user': 'root',
          'password': 'Iwantusesimplypassword',
          'db': 'music',
          'host': '127.0.0.1'
}

select_author = "SELECT author.id, author.name FROM author;"
select_album = "SELECT album.id, album.name FROM album WHERE author.author = %d;"
select_song = "SELECT songs.path, songs.name FROM songs WHERE songs.album = %d;"


inser_author = "INSERT author ()"
insert_song = "INSERT song ();"
