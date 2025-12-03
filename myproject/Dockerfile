# Sử dụng base image Python chính thức
FROM python:3.11-slim

# Thiết lập biến môi trường
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Thiết lập thư mục làm việc trong container
WORKDIR /usr/src/app

# Sao chép file requirements.txt và cài đặt dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# SAO CHÉP CHỈ THƯ MỤC CHỨA CODE CỦA BẠN (libraryManagement)
# và các file config khác lên thư mục làm việc
COPY libraryManagement ./libraryManagement

# Mở cổng 5000
EXPOSE 5000

# Lệnh chạy ứng dụng của bạn
# GIẢ SỬ file khởi chạy chính của bạn là 'app.py' nằm trong thư mục 'libraryManagement'
# Tức là module của bạn là 'libraryManagement' và đối tượng Flask là 'app'
# Bạn NÊN sử dụng Gunicorn (nếu đã cài đặt trong requirements.txt)
# Hoặc nếu bạn muốn dùng Flask built-in server (chỉ nên dùng cho demo)
CMD ["python3", "./libraryManagement/app.py","-m", "flask", "run", "--host=0.0.0.0", "--port=8080", "./libraryManagement/app.py"]

