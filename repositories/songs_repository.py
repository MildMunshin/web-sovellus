import sqlite3
from random import choice
import db

# def get_songs(sort_by="random"):
#     sql = ("SELECT * FROM songs")
#     songs = db.session.execute(sql).fetchall()
    
#     # if sort_by == "random":
#     #     return sorted(songs, key=lambda x: choice([0, 1]))
#     # elif sort_by == "title":
#     #     return sorted(songs, key=lambda x: x.title.lower())
#     # elif sort_by == "artist":
#     #     return sorted(songs, key=lambda x: x.artist.lower())

#     return songs


def get_songs():
    connection = sqlite3.connect("database.db")  # Oletetaan, että tietokanta on nimeltään database.db
    connection.row_factory = sqlite3.Row  # Tämä palauttaa tulokset sanakirjoina
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM songs")  # Haetaan kaikki kappaleet
    songs = cursor.fetchall()

    connection.close()
    return songs  # Nyt jokainen song on sanakirja, ei tuple!
