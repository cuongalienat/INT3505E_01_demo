import connexion
from flask import request, jsonify, current_app
from bson.objectid import ObjectId

def books_get(search=None, page=1, limit=10):
    """Lấy danh sách tất cả sách (có tìm kiếm & phân trang)"""
    mongo = getattr(current_app, "mongo", None)
    if not mongo:
        return jsonify({"error": "MongoDB chưa được khởi tạo"}), 500

    books_col = mongo.db.books

    query = {}
    if search:
        query = {
            "$or": [
                {"title": {"$regex": search, "$options": "i"}},
                {"author": {"$regex": search, "$options": "i"}},
            ]
        }

    page = int(page)
    limit = int(limit)
    skip = (page - 1) * limit

    books_cursor = books_col.find(query).skip(skip).limit(limit)
    books = []
    for b in books_cursor:
        b["_id"] = str(b["_id"])
        books.append(b)

    total = books_col.count_documents(query)
    return jsonify({
        "total": total,
        "page": page,
        "limit": limit,
        "books": books
    }), 200


def books_id_get(id):
    """Lấy thông tin sách theo ID Mongo"""
    mongo = getattr(current_app, "mongo", None)
    if not mongo:
        return jsonify({"error": "MongoDB chưa được khởi tạo"}), 500

    books_col = mongo.db.books

    try:
        book = books_col.find_one({"_id": ObjectId(id)})
    except Exception:
        return jsonify({"error": "ID sách không hợp lệ"}), 400

    if not book:
        return jsonify({"error": "Không tìm thấy sách"}), 404

    book["_id"] = str(book["_id"])
    return jsonify(book), 200


def books_post(body):
    """Thêm sách mới vào Mongo"""
    mongo = getattr(current_app, "mongo", None)
    if not mongo:
        return jsonify({"error": "MongoDB chưa được khởi tạo"}), 500

    data = request.json or {}
    books_col = mongo.db.books

    if not data.get("title") or not data.get("author"):
        return jsonify({"error": "Thiếu tiêu đề hoặc tác giả"}), 400

    result = books_col.insert_one({
        "title": data["title"],
        "author": data["author"],
        "available": True
    })

    return jsonify({
        "message": "Thêm sách thành công",
        "id": str(result.inserted_id)
    }), 201


def books_id_put(body, id):
    """Cập nhật thông tin sách theo ID Mongo"""
    mongo = getattr(current_app, "mongo", None)
    if not mongo:
        return jsonify({"error": "MongoDB chưa được khởi tạo"}), 500

    data = request.json or {}
    books_col = mongo.db.books

    update_data = {k: v for k, v in data.items() if k in ["title", "author", "available"]}
    if not update_data:
        return jsonify({"error": "Không có dữ liệu cập nhật"}), 400

    try:
        result = books_col.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    except Exception:
        return jsonify({"error": "ID sách không hợp lệ"}), 400

    if result.matched_count == 0:
        return jsonify({"error": "Không tìm thấy sách"}), 404

    return jsonify({"message": "Cập nhật sách thành công"}), 200


def books_id_delete(id):
    """Xóa sách theo ID Mongo"""
    mongo = getattr(current_app, "mongo", None)
    if not mongo:
        return jsonify({"error": "MongoDB chưa được khởi tạo"}), 500

    books_col = mongo.db.books

    try:
        result = books_col.delete_one({"_id": ObjectId(id)})
    except Exception:
        return jsonify({"error": "ID sách không hợp lệ"}), 400

    if result.deleted_count == 0:
        return jsonify({"error": "Không tìm thấy sách"}), 404

    return jsonify({"message": "Xóa sách thành công"}), 200
