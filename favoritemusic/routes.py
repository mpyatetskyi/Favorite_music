import bcrypt
import datetime
import psycopg2
import jwt
import sqlalchemy

from flask import request, jsonify
from favoritemusic import app, db
from favoritemusic.database_models import Users, Songs
from favoritemusic.models import User, UserSchema, Song, SongSchema
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError


@app.route('/')
def index():
    return 'Hello To Favorite Music App'


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    try:
        user = UserSchema().load(data)
    except ValidationError as err:
        return {"message": err.messages}
    except TypeError:
        return {"message": "Invalid input"}

    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'),
                                    bcrypt.gensalt(10)).decode('utf-8')

    user = Users(name=user.name, email=user.email, password=hashed_password)
    db.session.add(user)

    try:
        db.session.commit()
    except (sqlalchemy.exc.IntegrityError, psycopg2.errors.UniqueViolation):
        return {"message": "User already exists"}

    return {"message": f"User {user.name} successfully created"}


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    user = Users.query.filter_by(email=data['email']).first()

    if not user:
        return {"message": "No user with such email"}

    if not bcrypt.checkpw(data["password"].encode('utf-8'),
                          user.password.encode('UTF-8')):
        return {"message": "Invalid password"}

    else:
        schema = UserSchema()
        user = User(name=user.name, email=user.email, password=user.password)
        load_user = schema.dump(user)
        token = jwt.encode({"user": load_user,
                            'exp': datetime.datetime.utcnow() +
                            datetime.timedelta(minutes=30)},
                           app.config['SECRET_KEY'])
        return jsonify({"token": token})

