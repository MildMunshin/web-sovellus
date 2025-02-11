import db

def get_threads(id):
    sql = """SELECT t.id
             FROM threads t
             WHERE t.id = ?"""
    return db.query(sql, [id])


# def get_threads(id):
#     sql = """SELECT t.id, t.title, COUNT(m.id) total, MAX(m.sent_at) last
#              FROM threads t, messages m, songs s
#              WHERE t.id = s.song_id
#              GROUP BY t.id
#              ORDER BY t.id DESC"""
#     return db.query(sql)
