import sqlite3
import db

#fixaa samanlaiseksi kuin users.py-tiedostossa sit kun ehdit

def get_songs():
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row #sanakirjamuodossa
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM songs")
    songs = cursor.fetchall()

    connection.close()
    return songs

def get_user_songs(user):
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    user_id = user["id"] if isinstance(user, sqlite3.Row) else user #poimitaan käyttäjä_id sanakirjasta

    cursor.execute("SELECT * FROM songs WHERE user_id = ?", (user_id,))
    songs = cursor.fetchall()

    connection.close()
    return songs

def delete_song_from_db(id):
    sql = "DELETE FROM songs WHERE id = ?"
    db.execute(sql, [id])

# def delete_song_from_db(id):
#     connection = sqlite3.connect("database.db")
#     cursor = connection.cursor()

#     cursor.execute("DELETE FROM songs WHERE id = ?", (id,))  # Huomaa pilkku tuple-muodossa
#     connection.commit()  # Tallennetaan muutokset

#     connection.close()

def get_likes(id):
    sql = "SELECT COUNT(*) FROM likes WHERE song_id = ? AND is_like = 1"
    result = db.query(sql, [id])  # Assuming db.query() returns fetched data
    return result[0][0] if result else 0  # Extract the count from the result

def get_dislikes(id):
    sql = "SELECT COUNT(*) FROM likes WHERE song_id = ? AND is_like = 0"
    result = db.query(sql, [id])  # Assuming db.query() returns fetched data
    return result[0][0] if result else 0  # Extract the count from the result
