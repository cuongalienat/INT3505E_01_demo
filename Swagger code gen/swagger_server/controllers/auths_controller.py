import connexion
import six

from swagger_server.models.auths_body import AuthsBody  # noqa: E501
from swagger_server.models.inline_response2002 import InlineResponse2002  # noqa: E501
from swagger_server import util

from flask import request, jsonify, current_app
import jwt
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

def auths_post(body):  # noqa: E501
    """Đăng nhập

    Đăng nhập bằng username và password để nhận JWT token. # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: InlineResponse2002
    """
    data = request.get_json()

    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"message": "Thiếu tên đăng nhập hoặc mật khẩu"}), 400

    username = data["username"]
    password = data["password"]

    # Lấy Mongo instance từ Flask app
    mongo = current_app.mongo
    users_col = mongo.db.users

    # Tìm user trong MongoDB
    user = users_col.find_one({"username": username})
    if not user:
        return jsonify({"message": "Không tìm thấy người dùng"}), 404

    # Kiểm tra mật khẩu (ở demo này chưa mã hóa)
    if user["password"] != password:
        return jsonify({"message": "Sai mật khẩu"}), 401

    # ✅ Sinh JWT token (hết hạn sau 1 giờ)
    payload = {
        "user_id": str(user["_id"]),
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    secret = os.getenv("JWT_SECRET_KEY", "default_secret_key")  # fallback nếu chưa có
    token = jwt.encode(payload, secret, algorithm="HS256")

    return jsonify({
        "message": "Đăng nhập thành công",
        "token": token
    }), 200
