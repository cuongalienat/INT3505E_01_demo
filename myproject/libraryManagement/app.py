from flask import Flask, request, jsonify, url_for
from db import get_db, close_db, init_db
from datetime import datetime

app = Flask(__name__)
app.teardown_appcontext(close_db)

@app.route('/')
def hello():
    return 'Hello, World!'

# Khởi tạo database
@app.route("/init-db", methods=["GET"])
def init_database():
    init_db(app)
    return jsonify({"message": "Database initialized!"})

#  USERS
@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    db = get_db()
    db.execute("INSERT INTO users (name) VALUES (?)", (data["name"],))
    db.commit()
    return jsonify({"message": "User created!"})

# BOOKS

# getAllBook
@app.route("/books", methods=["GET"])
def get_books():
    db = get_db()
    books = db.execute("SELECT * FROM books").fetchall()
    return jsonify([dict(b) for b in books])

# getBookbyID
@app.route("/books/<int:id>", methods=["GET"])
def get_book(id):
    db = get_db()
    book = db.execute("SELECT * FROM books WHERE id = ?", (id,)).fetchone()
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(dict(book))

# addBook
@app.route("/books", methods=["POST"])
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
        {"rel": "self", "href": url_for("get_book", id=new_id, _external=True)},
        {"rel": "all-books", "href": url_for("get_books", _external=True)},
        {"rel": "update", "href": url_for("update_book", id=new_id, _external=True)},
        {"rel": "delete", "href": url_for("delete_book", id=new_id, _external=True)}
    ]

    response = {
        "message": "Book added successfully!",
        "data": {
            "id": new_id,
            "title": data["title"],
            "author": data["author"]
        },
        "links": links
    }
    return jsonify(response), 201

# editBook
@app.route("/books/<int:id>", methods=["PUT"])
def update_book(id):
    data = request.json
    db = get_db()
    db.execute("UPDATE books SET title=?, author=? WHERE id=?",
               (data["title"], data["author"], id))
    db.commit()
    return jsonify({"message": "Book updated!","data": { "id" : id, "new_title": data["title"], "new_author": data["author"]}})
# deleteBook
@app.route("/books/<int:id>", methods=["DELETE"])
def delete_book(id):
    db = get_db()
    db.execute("DELETE FROM books WHERE id=?", (id,))
    db.commit()
    return jsonify({"message": "Book deleted!"})
# borrowBook
@app.route("/borrows", methods=["POST"])
def borrow_book():
    data = request.json
    db = get_db()
    # Kiểm tra sách còn không
    book = db.execute("SELECT available FROM books WHERE id=?", (data["book_id"],)).fetchone()
    if not book or book["available"] == 0:
        return jsonify({"error": "Book not available"}), 400
    time = datetime.now().isoformat()
    db.execute("INSERT INTO borrows (user_id, book_id, borrow_date, borrow_status) VALUES (?, ?, ?, ?)",
               (data["user_id"], data["book_id"], time, "Borrowed"))
    db.execute("UPDATE books SET available=0 WHERE id=?", (data["book_id"],))
    db.commit()
    return jsonify({"message": "Book borrowed!", "createdAt" : time})
# returnBook
@app.route("/borrows", methods=["PATCH"])
def return_book():
    data = request.json
    db = get_db()
    time = datetime.now().isoformat()
    db.execute("UPDATE borrows SET return_date=?, borrow_status = ? WHERE user_id=? AND book_id=? AND return_date IS NULL",
               (time,"Returned" ,data["user_id"], data["book_id"]))
    db.execute("UPDATE books SET available=1 WHERE id=?", (data["book_id"],))
    db.commit()
    return jsonify({"message": "Book returned!",  "createdAt" : time})

if __name__ == "__main__":
    app.run(debug=True)