from favoritemusic import db


class Users(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    songs = db.relationship('Songs', backref='song', lazy=True)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return f"User('{self.name}', '{self.email}' )"


class Songs(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    spotify_id = db.Column(db.String)
    song_name = db.Column(db.String(100))
    album = db.Column(db.String(100))
    author = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, spotify_id, song_name, album, author, user_id):
        self.spotify_id = spotify_id
        self.song_name = song_name
        self.album = album
        self.author = author
        self.user_id = user_id

    def __repr__(self):
        return f"Song('{self.author}', '{self.song_name}')"




