from flask import Flask
from db import close_db
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from datetime import timedelta
from routes_v1 import v1 # Blueprint đã có JWT
from routes_v2 import v2 # Blueprint v2 

app = Flask(__name__)
load_dotenv()

# --- CẤU HÌNH JWT ---
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1) 

# --- KHỞI TẠO JWT ---
# Khởi tạo JWTManager, liên kết nó với ứng dụng Flask
jwt = JWTManager(app)

# --- CẤU HÌNH SWAGGER ---
swagger = Swagger(app, template_file='OpenAPI.yaml')

# --- CẤU HÌNH DATABASE VÀ BLUEPRINT ---
app.teardown_appcontext(close_db)
app.register_blueprint(v1)
app.register_blueprint(v2)

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == "__main__":
    app.run(debug=True)
