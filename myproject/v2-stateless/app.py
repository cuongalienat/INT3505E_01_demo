from flask import Flask, jsonify, request

app = Flask(__name__)

# data

users = [
    {"username" : "cuong123", "password" : "123456"}
]

@app.route("/api/login", methods=["POST"])

def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Dữ liệu đầu vào được kiểm tra trực tiếp, không lưu session
    user = next((u for u in users if u["username"] == username), None)

    if user is None:
        return jsonify({"status": "fail", "message": "Tên tài khoản không tồn tại!"}), 404

    if user["password"] != password:
        return jsonify({"status": "fail", "message": "Mật khẩu không đúng!"}), 401
    
    return jsonify({"status": "success", "message": "Đăng nhập thành công!", "user": {"username": user["username"]}}), 200

if __name__ == "__main__":
    app.run(debug=True)