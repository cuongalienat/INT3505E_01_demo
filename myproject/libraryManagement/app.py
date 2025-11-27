from flask import Flask, send_from_directory
from db import close_db
import os, yaml, json
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from datetime import timedelta
from routes_v1 import v1, limiter
from routes_v2 import v2
import logging
from logging.config import dictConfig
def create_app():
    app = Flask(__name__)
    load_dotenv()
    dictConfig({
        'version': 1,
        # Định dạng log: thời gian, mức độ, module (file), nội dung
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        # Handler: Nơi log sẽ được ghi (ở đây là console/stream lỗi chuẩn của WSGI)
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        # Root: Cấu hình chung
        'root': {
            'level': 'INFO', # Mức log tối thiểu được ghi ra (INFO, WARNING, ERROR,...)
            'handlers': ['wsgi']
        }
    })
    # --- CẤU HÌNH JWT ---
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

    # --- CẤU HÌNH SWAGGER ---
    # --- CẤU HÌNH SWAGGER UI (OpenAPI 3.0.0) ---
    limiter.init_app(app)

    @app.route("/OpenAPI.yaml")
    def serve_openapi_yaml():
        return send_from_directory(
            os.path.dirname(__file__),
            "OpenAPI.yaml",
            mimetype="text/yaml"
        )


    SWAGGER_URL = '/apidocs'
    API_URL = '/OpenAPI.yaml'  # file YAML của bạn

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': "Library Management API"}
    )

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)



    # --- KHỞI TẠO JWT ---
    jwt = JWTManager(app)

    # --- ĐĂNG KÝ BLUEPRINT ---
    app.teardown_appcontext(close_db)
    app.register_blueprint(v1)
    app.register_blueprint(v2)

    @app.route('/')
    def hello():
        return 'Hello, World!'
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
