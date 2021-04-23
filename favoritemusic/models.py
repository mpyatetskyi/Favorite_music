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
    def __init__(self, song_id):
        self.song_id = song_id

    def __repr__(self):
        return f"<Song(song_id={self.song_id!r})>"


class SongSchema(Schema):
    song_id = fields.Str()

    @post_load
    def make_song(self, data, **kwargs):
        return Song(**data)
