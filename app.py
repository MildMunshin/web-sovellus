import sqlite3
import os
from flask import Flask
from flask import redirect, render_template, request, session, make_response, redirect, url_for, abort, flash
from werkzeug.security import generate_password_hash, check_password_hash
import config, db, users, forum
from users import add_bio_text
from repositories.songs_repository import get_songs, get_user_songs, delete_song_from_db, get_likes, get_dislikes, search_songs


app = Flask(__name__)
app.secret_key = config.secret_key

AUDIO_FOLDER = 'static/audio_uploads/'
COVER_FOLDER = 'static/cover_uploads/'

app.config['AUDIO_FOLDER'] = AUDIO_FOLDER
app.config['COVER_FOLDER'] = COVER_FOLDER


@app.route("/")
def index():
    search_query = request.args.get("search", "").strip()

    if search_query:
        songs = search_songs(search_query)
    else:
        songs = get_songs()
    return render_template("index.html", songs=songs, search_query=search_query)

@app.route("/login_page")
def login_page():
    return render_template("login_page.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    
    sql = "SELECT password_hash FROM users WHERE username = ?"
    password_hash = db.query(sql, [username])[0][0]

    sql = "SELECT id FROM users WHERE username = ?"
    user_id = db.query(sql, [username])[0][0]
    print(user_id)

    if check_password_hash(password_hash, password):
        session["username"] = username
        session["user_id"] = user_id
        return redirect("/")
    else:
        return "VIRHE: väärä tunnus tai salasana"


@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")


@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    songs = get_user_songs(user)
    if not user:
        abort(404)
    return render_template("show_user.html", user=user, songs=songs)

@app.route("/song/<int:id>")
def show_song(id):
    song = users.get_song(id)
    thread = forum.get_thread(id)
    messages = forum.get_messages(id)
    like_counter = get_likes(id)
    dislike_counter = get_dislikes(id)
#    if not user:
#        abort(404)
    return render_template("show_song.html", song=song, thread=thread, messages=messages, like_counter=like_counter, dislike_counter=dislike_counter)

@app.route("/new_message", methods=["POST"])
def new_message():
    content = request.form["content"]
    user_id = session["user_id"]
    thread_id = request.form["thread_id"]

    forum.add_message(content, user_id, thread_id)
    return redirect("/song/" + str(thread_id))

@app.route("/edit/<int:message_id>", methods=["GET", "POST"])
def edit_message(message_id):
    require_login()  # Ensure user is logged in
    
    message = forum.get_message(message_id)
    if not message:
        abort(404)  # Message not found

    user_id = session.get("user_id")
    if message["user_id"] != user_id:
        abort(403)  # Prevent editing someone else's message

    if request.method == "GET":
        return render_template("edit.html", message=message)

    if request.method == "POST":
        new_content = request.form["content"].strip()
        if new_content:
            forum.update_message(message_id, new_content)
        return redirect("/song/" + str(message["thread_id"]))
    
@app.route("/remove/<int:message_id>", methods=["POST", "GET"])
def delete_message(message_id):
    require_login()

    message = forum.get_message(message_id)
    if not message:
        abort(404)  # Message not found

    if session.get("user_id") != message["user_id"]:
        abort(403)  # Prevent deleting someone else's message

    forum.delete_message(message_id)
    flash("Message deleted successfully!", "success")
    
    return redirect(f"/song/{message['thread_id']}")


def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/add_image", methods=["GET", "POST"])
def add_image():
    require_login()

    if request.method == "GET":
        return render_template("add_image.html")

    if request.method == "POST":
        file = request.files["image"]
        if not file.filename.endswith(".jpg"):
            return "VIRHE: väärä tiedostomuoto"

        image = file.read()
        if len(image) > 100 * 1024:
            return "VIRHE: liian suuri kuva"

        user_id = session["user_id"]
        users.update_image(user_id, image)
        return redirect("/user/" + str(user_id))
    
@app.route("/add_bio", methods=["POST"])
def add_bio():
    require_login()
    
    content = request.form.get("content", "").strip()  # Get content and remove extra spaces
    user_id = session["user_id"]

    # if session["user_id"] != user_id:
    #     abort(403)

    if content:  # Ensure bio is not empty
        add_bio_text(content, user_id)

    return redirect(f"/user/{user_id}")
    
    
@app.route("/image/<int:user_id>")
def show_image(user_id):
    image = users.get_image(user_id)
    # if not image:
    #     abort(404)

    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/jpeg")
    return response


@app.route("/upload_song")
def upload_song():
    return render_template("upload_song.html")

@app.route("/delete_song/<int:id>", methods=["POST"])
def delete_song(id):
    delete_song_from_db(id)
    user_id = session["user_id"]
    return redirect("/user/" + str(user_id))



@app.route('/upload', methods=['POST'])
def upload():
    title = request.form['title']
    artist = request.form['artist']
    genre = request.form['genre']
    
    file = request.files['file']
    cover = request.files['cover']
    
    if file and cover:
        filename = file.filename
        covername = cover.filename
        user_id = session["user_id"]

        # Tiedostojen tallennus
        audio_file_path = os.path.join(app.config['AUDIO_FOLDER'], filename)
        image_file_path = os.path.join(app.config['COVER_FOLDER'], covername)

        file.save(audio_file_path)
        cover.save(image_file_path)

        # Tallenna tietokantaan
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO songs (user_id, title, artist, audio_file_path, genre, image_file_path) 
            VALUES (?, ?, ?, ?, ?, ?)''', (user_id, title, artist, audio_file_path, genre, image_file_path))
        conn.commit()
        conn.close()

        # Tallenna uusi thread tietokantaan
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO threads DEFAULT VALUES;')
        conn.commit()
        conn.close()

        return redirect(url_for('index'))


@app.route("/like/<int:song_id>", methods=["POST"])
def like_song(song_id):
    if "user_id" not in session:
        return redirect(url_for("login_page"))

    user_id = session["user_id"]
    
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO likes (user_id, song_id, is_like) VALUES (?, ?, 1) "
        "ON CONFLICT(user_id, song_id) DO UPDATE SET is_like = 1",
        (user_id, song_id)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("show_song", id=song_id))

@app.route("/dislike/<int:song_id>", methods=["POST"])
def dislike_song(song_id):
    if "user_id" not in session:
        return redirect(url_for("login_page"))

    user_id = session["user_id"]
    
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO likes (user_id, song_id, is_like) VALUES (?, ?, 0) "
        "ON CONFLICT(user_id, song_id) DO UPDATE SET is_like = 0",
        (user_id, song_id)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("show_song", id=song_id))