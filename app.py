import sqlite3
import os
from flask import Flask
from flask import redirect, render_template, request, session, make_response, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import config, db, users
from repositories.songs_repository import get_songs, get_user_songs


app = Flask(__name__)
app.secret_key = config.secret_key

AUDIO_FOLDER = 'static/audio_uploads/'
COVER_FOLDER = 'static/cover_uploads/'

app.config['AUDIO_FOLDER'] = AUDIO_FOLDER
app.config['COVER_FOLDER'] = COVER_FOLDER

# @app.route("/")
# def index():
#     return render_template("index.html")

@app.route("/")
def index():
    songs = get_songs()
    return render_template("index.html", songs=songs)

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

    return "Tunnus luotu"

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

# @app.route("/login", methods=["POST"])
# def login():
#     username = request.form["username"]
#     password = request.form["password"]
    
#     # Hae käyttäjän ID ja salasana yhdellä kyselyllä
#     sql = "SELECT id, password_hash FROM users WHERE username = ?"
#     result = db.query(sql, [username])
    
#     # Tarkista, löytyikö käyttäjä
#     if not result:
#         return "VIRHE: väärä tunnus tai salasana"

#     user_id, password_hash = result[0]

#     # Vertaile salasanaa
#     if check_password_hash(password_hash, password):
#         # Tallenna käyttäjän tiedot sessioon
#         session["username"] = username
#         session["user_id"] = user_id
#         return redirect("/")
#     else:
#         return "VIRHE: väärä tunnus tai salasana"

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


# @app.route("/user/<int:user_id>")
# def show_user(user_id):
#     if "user_id" not in session or session["user_id"] != user_id:
#         return redirect("/login_page")
#     user = users.get_user(user_id)
#     if not user:
#         return "Käyttäjää ei löytynyt", 404
#     return render_template("show_user.html", user=user)

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
    
@app.route("/image/<int:user_id>")
def show_image(user_id):
    image = users.get_image(user_id)
    if not image:
        abort(404)

    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/jpeg")
    return response

@app.route("/upload_song")
def upload_song():
    return render_template("upload_song.html")



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

        return redirect(url_for('index'))

