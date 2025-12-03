FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY libraryManagement ./libraryManagement

CMD ["python3", "-m", "flask", "--app", "libraryManagement/app.py", "run", "--host=0.0.0.0", "--port=${PORT}"]
