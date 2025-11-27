from flask import Blueprint, jsonify, request, url_for, current_app
from db import get_db, init_db
from datetime import datetime
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from pybreaker import CircuitBreaker, CircuitBreakerError
import logging
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

v1 = Blueprint("v1", __name__, url_prefix="/api/v1")


limiter = Limiter(
    key_func=get_remote_address, # Dùng IP của client để giới hạn
    default_limits=["200 per day", "50 per hour"], # Giới hạn mặc định cho tất cả route
)
db_breaker = CircuitBreaker(fail_max=5, reset_timeout=30)
# -------------------- SYSTEM --------------------
@v1.route("/init-db", methods=["GET"])
def init_database():
    init_db(current_app)
    return jsonify({"message": "Database initialized!"})

# -------------------- AUTH --------------------
@v1.route("/auths", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    def attempt_login(u, p):
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (u,)).fetchone()
        if not user or user["password"] != p:
            return None
        return user
    try:
        user = db_breaker.call(attempt_login, username, password)
        if not user:
            current_app.logger.warning(f"Failed login attempt for username: {username}")
            return jsonify({"msg": "Tên đăng nhập hoặc mật khẩu không đúng."}), 400

        access_token = create_access_token(identity=str(user["id"]))
        current_app.logger.info(f"User {user['id']} logged in successfully.")
        return jsonify({"msg": "Đăng nhập thành công", "access_token": access_token}), 200
    except CircuitBreakerError:
        current_app.logger.error("Database connection error - Circuit Breaker Open")
        return jsonify({"msg": "Hệ thống đăng nhập đang bảo trì. Vui lòng thử lại sau ít phút."}), 503
    except Exception as e:
        # Xử lý các lỗi khác không liên quan đến breaker
        current_app.logger.error(f"An unexpected error occurred: {e}")
        return jsonify({"msg": "Đã xảy ra lỗi không mong muốn."}), 500
    

# -------------------- USERS --------------------
@v1.route("/users", methods=["POST"])
def create_user():
    data = request.json
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE username = ?", (data["username"],)).fetchone()
    if user:
        return jsonify({"msg": "user already exist"}), 400

    db.execute(
        "INSERT INTO users (username, password, name) VALUES (?, ?, ?)",
        (data["username"], data["password"], data["name"]),
    )
    db.commit()
    return jsonify({"message": "User created!"}), 201


@v1.route("/users", methods=["GET"])
@jwt_required()
def get_all_users():
    """
    GET /users: Lấy danh sách người dùng có tìm kiếm và phân trang.
    Query: ?search=cuong&page=1&limit=10
    """
    db = get_db()

    # --- Lấy tham số query ---
    search = request.args.get("search", "").strip()
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    offset = (page - 1) * limit

    # --- Tạo truy vấn ---
    base_query = "SELECT id, username, name FROM users"
    count_query = "SELECT COUNT(*) AS total FROM users"
    params = ()

    if search:
        base_query += " WHERE username LIKE ? OR name LIKE ?"
        count_query += " WHERE username LIKE ? OR name LIKE ?"
        params = (f"%{search}%", f"%{search}%")

    base_query += " LIMIT ? OFFSET ?"
    users = db.execute(base_query, (*params, limit, offset)).fetchall()
    total = db.execute(count_query, params).fetchone()["total"]

    users_list = [
        {"userId": u["id"], "username": u["username"], "full_name": u["name"]}
        for u in users
    ]

    return jsonify({
        "total": total,
        "page": page,
        "limit": limit,
        "data": users_list
    }), 200


# -------------------- BOOKS --------------------
@v1.route("/books", methods=["GET"])
@limiter.limit("100 per hour")
def get_books():
    """
    GET /books: Lấy danh sách sách có tìm kiếm và phân trang.
    Query: ?search=harry&page=1&limit=10
    """
    db = get_db()

    search = request.args.get("search", "").strip()
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    offset = (page - 1) * limit

    base_query = "SELECT * FROM books"
    count_query = "SELECT COUNT(*) AS total FROM books"
    params = ()

    if search:
        base_query += " WHERE title LIKE ? OR author LIKE ?"
        count_query += " WHERE title LIKE ? OR author LIKE ?"
        params = (f"%{search}%", f"%{search}%")

    base_query += " LIMIT ? OFFSET ?"
    books = db.execute(base_query, (*params, limit, offset)).fetchall()
    total = db.execute(count_query, params).fetchone()["total"]

    return jsonify({
        "total": total,
        "page": page,
        "limit": limit,
        "data": [dict(b) for b in books]
    }), 200


@v1.route("/books/<int:id>", methods=["GET"])
def get_book(id):
    db = get_db()
    book = db.execute("SELECT * FROM books WHERE id = ?", (id,)).fetchone()
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(dict(book))


@v1.route("/books", methods=["POST"])
@jwt_required()
def add_book():
    data = request.json
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO books (title, author) VALUES (?, ?)",
        (data["title"], data["author"])
    )
    db.commit()

    new_id = cursor.lastrowid  # Lấy ID của quyển sách vừa thêm

    # 🔹 Tạo các link HATEOAS
    links = [
        {"rel": "self", "href": url_for("v1.get_book", id=new_id, _external=True)},
        {"rel": "all-books", "href": url_for("v1.get_books", _external=True)},
        {"rel": "update", "href": url_for("v1.update_book", id=new_id, _external=True)},
        {"rel": "delete", "href": url_for("v1.delete_book", id=new_id, _external=True)}
    ]

    response = {
        "message": "Book added successfully (v1)!",
        "data": {
            "id": new_id,
            "title": data["title"],
            "author": data["author"]
        },
        "links": links
    }
    return jsonify(response), 201

# editBook
@v1.route("/books/<int:id>", methods=["PUT"])
@jwt_required()
def update_book(id):
    data = request.json
    db = get_db()
    db.execute(
        "UPDATE books SET title=?, author=? WHERE id=?",
        (data["title"], data["author"], id),
    )
    db.commit()
    return jsonify({
        "message": "Book updated!",
        "data": {"id": id, "new_title": data["title"], "new_author": data["author"]},
    }), 200


@v1.route("/books/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_book(id):
    db = get_db()
    db.execute("DELETE FROM books WHERE id=?", (id,))
    db.commit()
    return jsonify({"message": "Book deleted!"}), 200

# -------------------- LOANS --------------------
@v1.route("/loans", methods=["POST"])
@jwt_required()
def borrow_book():
    data = request.json
    db = get_db()
    user_id = get_jwt_identity()
    # Kiểm tra sách còn không
    book = db.execute("SELECT available FROM books WHERE id=?", (data["book_id"],)).fetchone()
    if not book or book["available"] == 0:
        return jsonify({"error": "Book not available"}), 400
    time = datetime.now().isoformat()
    db.execute("INSERT INTO loans (user_id, book_id, borrow_date, borrow_status) VALUES (?, ?, ?, ?)",
               (user_id, data["book_id"], time, "Borrowed"))
    db.execute("UPDATE books SET available=0 WHERE id=?", (data["book_id"],))
    db.commit()
    return jsonify({"message": "Book borrowed!", "createdAt": time}), 201


@v1.route("/loans", methods=["GET"])
@jwt_required()
def get_loans():
    """
    GET /loans: Lấy danh sách lượt mượn có tìm kiếm và phân trang.
    Query: ?search=harry&page=1&limit=10
    """
    db = get_db()

    search = request.args.get("search", "").strip()
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    offset = (page - 1) * limit

    base_query = """
        SELECT loans.id, users.name AS user_name, books.title AS book_title,
               loans.borrow_date, loans.return_date, loans.borrow_status
        FROM loans
        JOIN users ON loans.user_id = users.id
        JOIN books ON loans.book_id = books.id
    """
    count_query = "SELECT COUNT(*) AS total FROM loans JOIN users ON loans.user_id = users.id JOIN books ON loans.book_id = books.id"
    params = ()

    if search:
        base_query += " WHERE users.name LIKE ? OR books.title LIKE ?"
        count_query += " WHERE users.name LIKE ? OR books.title LIKE ?"
        params = (f"%{search}%", f"%{search}%")

    base_query += " ORDER BY loans.borrow_date DESC LIMIT ? OFFSET ?"
    loans = db.execute(base_query, (*params, limit, offset)).fetchall()
    total = db.execute(count_query, params).fetchone()["total"]

    return jsonify({
        "total": total,
        "page": page,
        "limit": limit,
        "data": [dict(l) for l in loans],
    }), 200


@v1.route("/loans", methods=["PATCH"])
@jwt_required()
def return_book():
    data = request.json
    db = get_db()
    user_id = get_jwt_identity()
    time = datetime.now().isoformat()
    db.execute("UPDATE loans SET return_date=?, borrow_status = ? WHERE user_id=? AND book_id=? AND return_date IS NULL",
               (time,"Returned" ,user_id, data["book_id"]))
    db.execute("UPDATE books SET available=1 WHERE id=?", (data["book_id"],))
    db.commit()
    return jsonify({"message": "Book returned!",  "createdAt" : time})