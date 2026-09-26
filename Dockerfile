FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 暴露 Render 預設或動態指定的連接埠
EXPOSE 8080

CMD ["python", "main.py"]