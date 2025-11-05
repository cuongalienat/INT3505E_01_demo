import connexion
import six

from swagger_server.models.inline_response2005 import InlineResponse2005  # noqa: E501
from swagger_server.models.loan import Loan  # noqa: E501
from swagger_server.models.loans_body import LoansBody  # noqa: E501
from swagger_server import util
from flask import request, jsonify, current_app
from datetime import datetime

def loans_get(search=None, page=None, limit=None):  # noqa: E501
    """Lấy danh sách lượt mượn (có tìm kiếm &amp; phân trang)

     # noqa: E501

    :param search: Tìm kiếm theo tên người dùng hoặc tiêu đề sách
    :type search: str
    :param page: Số trang (bắt đầu từ 1)
    :type page: int
    :param limit: Số bản ghi mỗi trang
    :type limit: int

    :rtype: InlineResponse2005
    """
    return 'do some magic!'


def loans_id_return_patch(id):  # noqa: E501
    """Trả sách

     # noqa: E501

    :param id: 
    :type id: int

    :rtype: None
    """
    return 'do some magic!'


def loans_post(body):  # noqa: E501
    """Mượn sách mới

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: Loan
    """
    data = request.json
    mongo = current_app.extensions['pymongo']
    loans_col = mongo.db.loans
    books_col = mongo.db.books

    book = books_col.find_one({"id": data["book_id"]})
    if not book:
        return jsonify({"message": "Book not found"}), 404
    if not book["available"]:
        return jsonify({"message": "Book already borrowed"}), 400

    loans_col.insert_one({
        "user_id": data["user_id"],
        "book_id": data["book_id"],
        "borrow_date": datetime.utcnow(),
        "return_date": None
    })
    books_col.update_one({"id": data["book_id"]}, {"$set": {"available": False}})

    return jsonify({"message": "Book borrowed successfully"}), 201
