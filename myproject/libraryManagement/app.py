from flask import Flask, send_from_directory
from db import close_db
import os, yaml, json
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from datetime import timedelta
from routes_v1 import v1
from routes_v2 import v2

app = Flask(__name__)
load_dotenv()

# --- CẤU HÌNH JWT ---
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

# --- CẤU HÌNH SWAGGER ---
# --- CẤU HÌNH SWAGGER UI (OpenAPI 3.0.0) ---

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

if __name__ == "__main__":
    app.run(debug=True)
