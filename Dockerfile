# Python ベースイメージ
FROM python:3.10-slim

# 作業ディレクトリを作成
WORKDIR /app

# 必要なパッケージをインストール（Nginxを追加）
RUN apt-get update && apt-get install -y nginx \
    build-essential \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# アプリケーションファイルをコピー
COPY . .

# `nginx.conf` を適用
COPY nginx.conf /etc/nginx/nginx.conf

# 依存関係をインストール
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Flask を 5000 で起動（Nginx が 8080 でリバースプロキシ）
ENV FLASK_APP=run.py
ENV FLASK_ENV=production
ENV PORT=5000

# ポートを指定
EXPOSE 8080

# Flask と Nginx を並列起動
CMD service nginx start && flask run --host=0.0.0.0 --port=$PORT
