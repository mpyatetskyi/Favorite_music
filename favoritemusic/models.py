from marshmallow import Schema, fields, post_load, validate, INCLUDE


class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return f"<User(name={self.name!r})>"


class UserSchema(Schema):
    class Meta:
        unknown = INCLUDE

    name = fields.Str(validate=validate.Length(min=1), required=True)
    email = fields.Email()
    password = fields.Str()

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


class Song:
    def __init__(self, **kwargs):
        self.spotify_id = kwargs['spotify_id']
        self.song_name = kwargs['song_name']
        self.album = kwargs['album']
        self.author = kwargs['author']


class SpotifySongSchema(Schema):
    spotify_id = fields.Str()
    song_name = fields.Str()
    album = fields.Str()
    author = fields.Str()

    @post_load()
    def make_song(self, data, **kwargs):
        return SpotifySong(**data)


class SpotifySong:
    def __init__(self, spotify_id: str,
                 song_name: str,
                 album: str,
                 author: str):
        self.spotify_id = spotify_id
        self.song_name = song_name
        self.album = album
        self.author = author


class SpotifySongSchema(Schema):
    spotify_id = fields.Str()
    song_name = fields.Str()
    album = fields.Str()
    author = fields.Str()

    @post_load()
    def make_song(self, data, **kwargs):
        return SpotifySong(**data)


