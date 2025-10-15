from flask import Flask, jsonify, request

app = Flask(__name__)

# Server chỉ xử lý dữ liệu và trả JSON cho client, name là tham số trên query
@app.route("/api/hello", methods=["GET"])
def hello():
    name = request.args.get("name")
    return jsonify({"message": f"hello {name}, this is reponse from Server!"})

if __name__ == "__main__":
    app.run(debug=True)
