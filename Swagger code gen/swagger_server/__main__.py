#!/usr/bin/env python3
import connexion
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

from swagger_server.encoder import CustomJSONProvider

load_dotenv()

def main():
    # Tạo app Connexion (bên trong có Flask)
    connex_app = connexion.App(__name__, specification_dir="./swagger/")
    connex_app.add_api(
        "swagger.yaml",
        arguments={'title': 'Library Management API (v1)'},
        pythonic_params=True
    )

    # Lấy Flask app bên trong Connexion
    app = connex_app.app
    app.json = CustomJSONProvider(app)

    # Cấu hình Mongo
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")

    # Khởi tạo PyMongo đúng cách (vào Flask instance của Connexion)
    mongo = PyMongo(app)
    # Gắn mongo vào Flask để dùng trong controller
    app.mongo = mongo

    app.extensions['pymongo'] = mongo

    # Chạy server
    connex_app.run(port=5000)


if __name__ == "__main__":
    main()
