FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --break-system-packages --no-cache-dir -r requirements.txt

COPY . .

# 暴露端口（Cloud Run 使用 8080）
EXPOSE 8080

CMD ["python", "main.py"]