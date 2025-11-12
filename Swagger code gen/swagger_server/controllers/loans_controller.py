import connexion
import six

from swagger_server.models.inline_response2005 import InlineResponse2005  # noqa: E501
from swagger_server.models.loan import Loan  # noqa: E501
from swagger_server.models.loans_body import LoansBody  # noqa: E501
from swagger_server import util
from flask import request, jsonify, current_app
from datetime import datetime
from bson import ObjectId

# ===============================
# Lấy danh sách lượt mượn
# ===============================
def loans_get(search=None, page=1, limit=10):  # noqa: E501
    """Lấy danh sách lượt mượn (có tìm kiếm & phân trang)"""
    mongo = current_app.extensions['pymongo']
    loans_col = mongo.db.loans
    books_col = mongo.db.books
    users_col = mongo.db.users

    query = {}
    if search:
        # Tìm theo tên user hoặc tên sách
        user_matches = list(users_col.find({"username": {"$regex": search, "$options": "i"}}))
        book_matches = list(books_col.find({"title": {"$regex": search, "$options": "i"}}))
        user_ids = [u["id"] for u in user_matches]
        book_ids = [b["id"] for b in book_matches]
        query = {"$or": [{"user_id": {"$in": user_ids}}, {"book_id": {"$in": book_ids}}]}

    # Phân trang
    skips = (page - 1) * limit
    cursor = loans_col.find(query).skip(skips).limit(limit)
    results = []

    for loan in cursor:
        user = users_col.find_one({"id": loan["user_id"]})
        book = books_col.find_one({"id": loan["book_id"]})
        results.append({
            "loan_id": str(loan.get("_id")),
            "user": user["username"] if user else None,
            "book": book["title"] if book else None,
            "borrow_date": loan["borrow_date"],
            "return_date": loan["return_date"]
        })

    total = loans_col.count_documents(query)
    return jsonify({
        "total": total,
        "page": page,
        "limit": limit,
        "data": results
    }), 200


# ===============================
# Mượn sách mới
# ===============================
def loans_post(body):  # noqa: E501
    """Mượn sách mới"""
    data = request.json
    mongo = current_app.extensions['pymongo']
    loans_col = mongo.db.loans
    books_col = mongo.db.books

    # Kiểm tra sách tồn tại
    book = books_col.find_one({"id": data["book_id"]})
    if not book:
        return jsonify({"message": "Book not found"}), 404
    if not book.get("available", True):
        return jsonify({"message": "Book already borrowed"}), 400

    # Thêm lượt mượn
    loans_col.insert_one({
        "user_id": data["user_id"],
        "book_id": data["book_id"],
        "borrow_date": datetime.utcnow(),
        "return_date": None
    })
    # Cập nhật trạng thái sách
    books_col.update_one({"id": data["book_id"]}, {"$set": {"available": False}})

    return jsonify({"message": "Book borrowed successfully"}), 201


# ===============================
# Trả sách
# ===============================
def loans_id_return_patch(id):  # noqa: E501
    """Trả sách"""
    mongo = current_app.extensions['pymongo']
    loans_col = mongo.db.loans
    books_col = mongo.db.books

    loan = loans_col.find_one({"_id": ObjectId(id)})
    if not loan:
        return jsonify({"message": "Loan record not found"}), 404
    if loan.get("return_date"):
        return jsonify({"message": "Book already returned"}), 400

    # Cập nhật ngày trả và trạng thái sách
    loans_col.update_one({"_id": ObjectId(id)}, {"$set": {"return_date": datetime.utcnow()}})
    books_col.update_one({"id": loan["book_id"]}, {"$set": {"available": True}})

    return jsonify({"message": "Book returned successfully"}), 200