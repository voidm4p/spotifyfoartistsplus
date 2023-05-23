from flask import jsonify
#from sqlalchemy.ext.declarative import DeclarativeMeta
import json
from datetime import datetime
from uuid import UUID
from functools import wraps
from flask import request, jsonify
from flask import current_app as app
import jwt
from models import User

def handle_success(data):
    d = {
        'meta': {
            'code': 200
        },
        'data': data
    }
    resp = jsonify(d)
    resp.status_code = 200
    return resp


def handle_error(code, type="", message="", data={}):
    d = {
        'meta': {
            'code': code,
            'error_type': type,
            'error_message': message
        },
        'data': data
    }
    resp = jsonify(d)
    resp.status_code = code
    return resp


def handle_400(message="", data={}):
    return handle_error(400, "Bad Request", message, data)


def handle_401(message="", data={}):
    return handle_error(401, "Unauthorized", message, data)


def handle_403(message="", data={}):
    return handle_error(403, "Forbidden", message, data)


def handle_404(message="", data={}):
    return handle_error(404, "Not Found", message, data)

def handle_409(message="", data={}):
    return handle_error(409, "Conflict", message, data)

def handle_500(type="", message="", data={}):
    return handle_error(500, type, message, data)


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None
        print(request.headers)
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"])
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)

    return decorator
