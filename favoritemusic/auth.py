import jwt
from flask import request, jsonify
from functools import wraps
from run import app
from favoritemusic.database_models import Users, Songs


def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Bearer' in request.headers:
            token = request.headers['bearer']

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'],
                              algorithms='HS256')

            current_user = Users.query.filter_by(email=data["user"]["email"]).first()

        except TypeError:
            return jsonify({'message': 'Token is invalid'}), 401
        except jwt.exceptions.DecodeError:
            return jsonify({'message': 'Token is invalid'}), 401
        except jwt.exceptions.ExpiredSignatureError:
            return jsonify({'message': 'Signature has expired. Please Log In '}), 401

        return f(current_user, *args, **kwargs)

    return decorated
