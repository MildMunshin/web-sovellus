import db

def get_thread(id):
    sql = """SELECT t.id
             FROM threads t
             WHERE t.id = ?"""
    result = db.query(sql, [id])
    return result[0]


def add_message(content, user_id, thread_id):
    sql = """INSERT INTO messages (content, sent_at, user_id, thread_id)
             VALUES (?, datetime('now'), ?, ?)"""
    db.execute(sql, [content, user_id, thread_id])

def get_messages(id):
    sql = """SELECT m.id, m.content, m.sent_at, m.user_id, u.username
             FROM messages m, users u
             WHERE m.user_id = u.id AND m.thread_id = ?
             ORDER BY m.id DESC"""
    return db.query(sql, [id])

def get_message(message_id):
    sql = """SELECT m.id, m.content, m.sent_at, m.user_id, u.username, m.thread_id
             FROM messages m
             JOIN users u ON m.user_id = u.id
             WHERE m.id = ?"""
    result = db.query(sql, [message_id])
    return result[0] if result else None  # Return None if no message is found

def update_message(message_id, content):
    sql = "UPDATE messages SET content = ? WHERE id = ?"
    db.execute(sql, [content, message_id])

def delete_message(message_id):
    sql = "DELETE FROM messages WHERE id = ?"
    db.execute(sql, [message_id])


# def get_threads(id):
#     sql = """SELECT t.id, t.title, COUNT(m.id) total, MAX(m.sent_at) last
#              FROM threads t, messages m, songs s
#              WHERE t.id = s.song_id
#              GROUP BY t.id
#              ORDER BY t.id DESC"""
#     return db.query(sql)
