from flask import Blueprint, jsonify, request
from db import get_db
from datetime import datetime

v2 = Blueprint("v2", __name__, url_prefix="/api/v2")

def migrate_v2():
    db = get_db()
    # Thêm published_year và genres vào table books
    db.execute("ALTER TABLE books ADD COLUMN published_year INTEGER;")
    db.execute("ALTER TABLE books ADD COLUMN genre TEXT;")
    db.commit()

@v2.route("/migrations", methods=["GET"])
def migrate_db_v2():
    migrate_v2()
    return jsonify({"message": "Database upgraded to v2!"})

@v2.route("/books", methods=["POST"])
def add_book_v2():
    data = request.json
    db = get_db()
    db.execute(
        "INSERT INTO books (title, author, published_year, genre) VALUES (?, ?, ?, ?)",
        (data["title"], data["author"], data.get("published_year"), data.get("genre"))
    )
    db.commit()
    return jsonify({
        "message": "Book added (v2)!",
        "data": data
    }), 201