FROM python:3.10-slim

# 必要なパッケージのインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .  

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# entrypoint.sh をコピーして実行権限を付与
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Gunicorn 実行用のデフォルトコマンドは削除 or 後述
# CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8080", "run:app"]

# 代わりにエントリーポイントを設定
ENTRYPOINT ["/entrypoint.sh"]
