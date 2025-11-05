#!/usr/bin/env python3

import connexion
from swagger_server.encoder import CustomJSONProvider
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

# Tải biến môi trường từ file .env
load_dotenv()

def main():
    # Tạo connexion app
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json = CustomJSONProvider(app.app)

    # Lấy Flask app thật bên trong connexion
    flask_app = app.app

    # Cấu hình MongoDB cho Flask app
    flask_app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/library_db")

    # Khởi tạo PyMongo trên Flask app này
    mongo = PyMongo(flask_app)

    # (Quan trọng) Gắn mongo vào extensions để các controller có thể truy cập
    flask_app.extensions['pymongo'] = mongo

    # Thêm API từ swagger.yaml
    app.add_api('swagger.yaml', arguments={'title': 'Library Management API (v1)'}, pythonic_params=True)

    # Chạy server
    app.run(port=5000)


if __name__ == '__main__':
    main()
