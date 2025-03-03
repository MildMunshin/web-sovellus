import db
import sqlite3

def get_user(user_id):
    sql = """SELECT id, username, image IS NOT NULL has_image, bio, bio IS NOT NULL has_bio
             FROM users
             WHERE id = ?"""
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_messages(user_id):
    sql = """SELECT m.id,
                    m.thread_id,
                    t.title thread_title,
                    m.sent_at
             FROM threads t, messages m
             WHERE t.id = m.thread_id AND
                   m.user_id = ?
             ORDER BY m.sent_at DESC"""
    return db.query(sql, [user_id])

def update_image(user_id, image):
    sql = "UPDATE users SET image = ? WHERE id = ?"
    db.execute(sql, [image, user_id])

def get_image(user_id):
    sql = "SELECT image FROM users WHERE id = ?"
    result = db.query(sql, [user_id])  # Käytä db.query, koska db.execute ei palauta tuloksia

    if result and result[0][0]:  # Tarkistetaan, että tulos ei ole tyhjä ja kuva on olemassa
        return result[0][0]  # Palautetaan binääri-BLOB
    return None  # Jos kuvaa ei ole, palautetaan None

def add_bio_text(content, user_id):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    
    cursor.execute(
        "UPDATE users SET bio = ? WHERE id = ?", (content, user_id)
    )
    
    connection.commit()
    connection.close()