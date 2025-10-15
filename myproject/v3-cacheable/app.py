from flask import Flask, jsonify, request, make_response
import time

app = Flask(__name__)

@app.route("/api/time", methods=["GET"])
def get_time():
    # Nếu client gửi header 'If-Modified-Since' (Postman có thể set)
    client_time = request.headers.get("If-Modified-Since")

    # Server giữ mốc thời gian lần cuối cập nhật (giả lập)
    last_update = time.time() - 5  # cách đây 5 giây

    # Nếu client có header và chưa quá 10 giây, trả 304 (Not Modified)
    if client_time and (time.time() - last_update < 10):
        return make_response("", 304)

    # Ngược lại, trả dữ liệu mới và thêm header cache
    resp = make_response(jsonify({
        "message": "Dữ liệu mới được cập nhật!",
        "server_time": time.strftime("%Y-%m-%d %H:%M:%S")
    }), 200)

    resp.headers["Cache-Control"] = "public, max-age=10"
    resp.headers["Last-Modified"] = time.strftime("%a, %d %b %Y %H:%M:%S GMT")

    return resp

if __name__ == "__main__":
    app.run(debug=True)
