import jwt
from flask import request, jsonify
from functools import wraps
from run import app


def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'],
                              algorithms='HS256')
            c.execute('SELECT * FROM user WHERE user_id=? LIMIT 1',
                      [data['user_id']])
            user = c.fetchone()
            current_user = user[0]

        except TypeError:
            return jsonify({'message': 'Token is invalid'}), 401
        except jwt.exceptions.DecodeError:
            return jsonify({'message': 'Token is invalid'}), 401
        except jwt.exceptions.ExpiredSignatureError:
            return jsonify({'message': 'Signature has expired. Please Log In '}), 401

        return f(current_user, *args, **kwargs)

    return decorated
