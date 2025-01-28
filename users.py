def get_user(user_id):
    sql = "SELECT username FROM users WHERE id = ?"
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
