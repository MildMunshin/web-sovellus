import db

def get_user(user_id):
    sql = """SELECT id, username, image IS NOT NULL has_image
             FROM users
             WHERE id = ?"""
    result = db.query(sql, [user_id])
    return result[0] if result else None

#pitäisikö tämä olla songs_repositoriossa? tai toisinpäin?
def get_song(id):
    sql = """SELECT id, user_id, title, artist, audio_file_path, image_file_path, genre
             FROM songs
             WHERE id = ?"""
    result = db.query(sql, [id])
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
