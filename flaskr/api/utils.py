from jwt import decode
from jwt.exceptions import InvalidTokenError
from flask import request, jsonify
from flaskr import app


def get_user():
    jwt_token = request.headers.get("Authorization")
    if not jwt_token:
        return jsonify({
            "error": "JTW token is missing."
        }), 403
    try:
        data = decode(jwt_token, app.config.get(
            "JWT_SECRET_KEY"), algorithms=['HS256'])
        return data.get("id")
    except InvalidTokenError:
        return jsonify({
            "error": "Invalid token.",
        }), 403
    except Exception as e:
        return jsonify({
            "error": e.__str__(),
        }), 500
