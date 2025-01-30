CREATE TABLE visits (
    id INTEGER PRIMARY KEY,
    visited_at TEXT
);
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
, image BLOB);
CREATE TABLE songs (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    artist TEXT NOT NULL CHECK (LENGTH(artist) > 0),
    file_path TEXT NOT NULL,
    upload_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    genre TEXT CHECK (LENGTH(genre) > 0),
    duration INTEGER CHECK (duration > 0),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
