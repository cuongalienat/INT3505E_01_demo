import connexion
import six

from swagger_server.models.book import Book  # noqa: E501
from swagger_server.models.book_create import BookCreate  # noqa: E501
from swagger_server.models.inline_response2004 import InlineResponse2004  # noqa: E501
from swagger_server import util
from flask import request, jsonify, current_app


def books_get(search=None, page=None, limit=None):  # noqa: E501
    """Lấy danh sách tất cả sách (có tìm kiếm &amp; phân trang)

     # noqa: E501

    :param search: Từ khóa tìm kiếm theo tiêu đề hoặc tác giả
    :type search: str
    :param page: Số trang (bắt đầu từ 1)
    :type page: int
    :param limit: Số bản ghi mỗi trang
    :type limit: int

    :rtype: InlineResponse2004
    """
    return 'do some magic!'


def books_id_delete(id):  # noqa: E501
    """Xóa sách

     # noqa: E501

    :param id: 
    :type id: int

    :rtype: None
    """
    return 'do some magic!'


def books_id_get(id):  # noqa: E501
    """Lấy thông tin sách theo ID

     # noqa: E501

    :param id: 
    :type id: int

    :rtype: Book
    """
    return 'do some magic!'


def books_id_put(body, id):  # noqa: E501
    """Cập nhật thông tin sách

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param id: 
    :type id: int

    :rtype: None
    """
    if connexion.request.is_json:
        body = BookCreate.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def books_post(body):  # noqa: E501
    """Thêm sách mới

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: Book
    """
    data = request.json
    mongo = current_app.extensions['pymongo']
    books_col = mongo.db.books

    books_col.insert_one({
        "title": data["title"],
        "author": data["author"],
        "available": True
    })
    return jsonify({"message": "Book added"}), 201
