from flask import Flask, request, jsonify, url_for
from db import get_db, close_db, init_db
from flasgger import Swagger
from datetime import datetime
from routes_v1 import v1

app = Flask(__name__)
swagger = Swagger(app, template_file='OpenAPI.yaml')

app.teardown_appcontext(close_db)
app.register_blueprint(v1)

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == "__main__":
    app.run(debug=True)