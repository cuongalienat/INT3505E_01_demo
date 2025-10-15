from flask import Flask, jsonify, request, url_for

app = Flask(__name__)

books = [
    {"id": 1, "title": "Lập trình Python"},
    {"id": 2, "title": "Flask cơ bản"}
]

# Hàm tiện ích để thêm link HATEOAS vào mỗi tài nguyên
def add_hateoas_links(book):
    return {
        "id": book["id"],
        "title": book["title"],
        "_links": {
            "self": {"href": url_for("get_book", book_id=book["id"], _external=True)},
            "delete": {"href": url_for("delete_book", book_id=book["id"], _external=True)},
            "all_books": {"href": url_for("get_books", _external=True)}
        }
    }

@app.route("/api/books", methods=["GET"])
def get_books():
    result = [add_hateoas_links(book) for book in books]
    return jsonify(result)

@app.route("/api/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    for book in books:
        if book["id"] == book_id:
            return jsonify(add_hateoas_links(book))
    return jsonify({"message": "Không tìm thấy sách"}), 404

@app.route("/api/books", methods=["POST"])
def add_book():
    new_book = request.get_json()
    new_book["id"] = len(books) + 1
    books.append(new_book)
    response = add_hateoas_links(new_book)
    return jsonify(response), 201

@app.route("/api/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    global books
    books = [b for b in books if b["id"] != book_id]
    return jsonify({"message": "Đã xóa thành công!"})

if __name__ == "__main__":
    app.run(debug=True)
