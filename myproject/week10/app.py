from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os
from datetime import datetime, UTC
import time
from deprecated import deprecated 
import warnings

warnings.simplefilter("default", DeprecationWarning)
# Tải biến môi trường
load_dotenv()

app = Flask(__name__)

# Cấu hình MongoDB
app.config["MONGO_URI"] = os.getenv("MONGO_URI") 
mongo = PyMongo(app)
payments_collection = mongo.db.payments

# --- HẰNG SỐ VÀ LOGIC MÔ PHỎNG ---
# Tỷ giá hối đoái giả định (Coi VND là base currency)
EXCHANGE_RATES = {
    "VND": 1.0,
    "USD": 25000.0, # 1 USD = 25,000 VND
    "EUR": 27000.0  # 1 EUR = 27,000 VND
}
SUPPORTED_CURRENCIES = list(EXCHANGE_RATES.keys())
BASE_CURRENCY = "VND"
BASE_AMOUNT_FACTOR = 100 # Lưu tiền ở đơn vị cent/xu để tránh lỗi float
def generate_transaction_id():
    """Tạo ID giao dịch giả định."""
    return f"TXN-{int(time.time() * 1000)}"

def convert_to_base(amount, currency):
    """Quy đổi số tiền từ đơn vị tiền tệ giao dịch sang VND (base currency)."""
    if currency not in EXCHANGE_RATES:
        raise ValueError("Unsupported currency")
        
    rate = EXCHANGE_RATES.get(currency)
    base_amount = amount * rate
    # Lưu dưới dạng đơn vị thấp nhất (nhân 100) và làm tròn
    return int(round(base_amount * BASE_AMOUNT_FACTOR))

# --- API Version 1 (V1) - Nghiệp vụ VND Cố định ---
@app.route("/api/migrate/payments", methods=["POST"])
def auto_migrate_payment():
    """
    Tự động chuyển request V1 sang V2.
    Dành cho client không chịu cập nhật currencyCode.
    """
    data = request.get_json()

    # Nếu client không gửi currencyCode → mặc định dùng VND (v1 style)
    if "currencyCode" not in data:
        data["currencyCode"] = "VND"

    # Chuyển hướng sang xử lý logic của V2
    with app.test_request_context(
        "/api/v2/payments",
        method="POST",
        json=data
    ):
        return create_payment_v2()

@app.route('/api/v1/payments', methods=['POST'])
def create_payment_v1():
    warnings.warn(
        "API V1 đã lỗi thời và sẽ bị gỡ bỏ vào ngày 01/01/2026.",
        DeprecationWarning,
        stacklevel=2
    )
    """
    V1: Tạo giao dịch. CHỈ CHẤP NHẬN VND (implicit).
    Input: {"amount": 100000.00}
    """
    data = request.get_json()
    
    amount_float = float(data.get("amount"))
    
    if not amount_float:
        return jsonify({"error_message": "amount là bắt buộc."}), 400

    # *** ĐIỂM KHÁC BIỆT V1: Mặc định và chỉ hỗ trợ VND ***
    amount_cents = int(round(amount_float * BASE_AMOUNT_FACTOR))
    
    new_payment_document = {
        "transactionId": generate_transaction_id(),
        "amount": amount_cents, 
        "currencyCode": "VND", # Hardcode VND
        "status": 'SUCCESS',
        "processedAt": datetime.now(UTC).isoformat(),
        "version": 1
    }
    
    result = payments_collection.insert_one(new_payment_document)
    
    # Response V1 
    response = jsonify({
        "statusCode": 201,
        "transactionId": new_payment_document["transactionId"],
        "paymentAmountVnd": amount_float
    })
    response.headers["X-API-Deprecated"] = "true"
    response.headers["X-API-EOL"] = "2026-01-01"
    response.headers["X-Migration-Guide"] = "/docs/migration/v1-to-v2"

    return response, 201


# --- API Version 2 (V2) - Nghiệp vụ Đa tiền tệ ---
@app.route('/api/v2/payments', methods=['POST'])
def create_payment_v2():
    """
    V2: Tạo giao dịch. YÊU CẦU currencyCode và QUY ĐỔI sang base currency.
    Input: {"amount": 50.00, "currencyCode": "USD"}
    """
    data = request.get_json()
    
    amount_float = float(data.get("amount"))
    currency_code = data.get("currencyCode", "").upper()
    
    if not amount_float or currency_code not in SUPPORTED_CURRENCIES:
        return jsonify({
            "error": {"message": f"amount và currencyCode ({SUPPORTED_CURRENCIES}) là bắt buộc và hợp lệ."}
        }), 400

    try:
        # *** ĐIỂM KHÁC BIỆT V2: Quy đổi và lưu cả 2 giá trị ***
        payment_amount_cents = int(round(amount_float * BASE_AMOUNT_FACTOR))
        base_amount_cents = convert_to_base(amount_float, currency_code)
        
    except ValueError as e:
        return jsonify({"error": {"message": str(e)}}), 400
    
    new_payment_document = {
        "transactionId": generate_transaction_id(),
        "paymentCurrency": currency_code,
        "paymentAmount": payment_amount_cents, 
        "baseCurrency": BASE_CURRENCY, # VND
        "baseAmount": base_amount_cents, 
        "exchangeRate": EXCHANGE_RATES.get(currency_code),
        "status": 'SUCCESS', 
        "processedAt": datetime.utcnow(),
        "version": 2
    }
    
    result = payments_collection.insert_one(new_payment_document)

    # Response V2 
    return jsonify({
        "status": "SUCCESS", 
        "data": {
            "transactionId": new_payment_document['transactionId'],
            "paymentAmount": amount_float,
            "paymentCurrency": currency_code,
            "baseAmountVND": base_amount_cents / BASE_AMOUNT_FACTOR,
            "exchangeRateUsed": new_payment_document['exchangeRate']
        }
    }), 201


# --- Khởi chạy Ứng dụng ---
if __name__ == '__main__':
    print(f"API chạy: http://127.0.0.1:5000/")
    print(f"V1 POST: /api/v1/payments (Chỉ VND)")
    print(f"V2 POST: /api/v2/payments (Hỗ trợ Đa tiền tệ)")
    app.run(debug=True)