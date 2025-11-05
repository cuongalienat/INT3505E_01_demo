import connexion
import six

from swagger_server.models.inline_response2003 import InlineResponse2003  # noqa: E501
from swagger_server.models.user import User  # noqa: E501
from swagger_server.models.user_create import UserCreate  # noqa: E501
from swagger_server import util
from flask import request, jsonify, current_app

def users_get(search=None, page=1, limit=10):  # noqa: E501
    """Lấy danh sách người dùng (có tìm kiếm &amp; phân trang)

     # noqa: E501

    :param search: Từ khóa tìm kiếm theo tên hoặc username
    :type search: str
    :param page: Số trang (bắt đầu từ 1)
    :type page: int
    :param limit: Số bản ghi mỗi trang
    :type limit: int

    :rtype: InlineResponse2003
    """
    mongo = current_app.extensions['pymongo']
    users_col = mongo.db.users

    query = {}
    if search:
        query["$or"] = [
            {"username": {"$regex": search, "$options": "i"}},
            {"name": {"$regex": search, "$options": "i"}}
        ]

    cursor = users_col.find(query, {"password": 0})  # ẩn password
    total = cursor.count()
    data = list(cursor.skip((page-1)*limit).limit(limit))

    for user in data:
        user["_id"] = str(user["_id"])

    return jsonify({
        "total": total,
        "page": page,
        "limit": limit,
        "data": data
    })


def users_post(body):  # noqa: E501
    """Tạo người dùng mới

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: User
    """
    data = request.json
    mongo = current_app.extensions['pymongo']
    users_col = mongo.db.users

    # Kiểm tra trùng username
    if users_col.find_one({"username": data["username"]}):
        return jsonify({"message": "Username already exists"}), 400

    users_col.insert_one({
        "username": data["username"],
        "password": data["password"],
        "name": data["name"]
    })
    return jsonify({"message": "User created"}), 201
