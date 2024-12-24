#!/bin/sh

# 1. (オプション) DB接続待機スクリプトを実行
#    すでに `wait_for_db.py` などで OperationalError を捕まえて retry する実装がある場合はここで呼びます。
#    python wait_for_db.py

echo "=== 1. Checking/Waiting for DB to be ready ==="
# 例えば先ほどの wait_for_db 関数のように、PythonワンライナーでもOKです。
# python -c "from run import wait_for_db; wait_for_db()"

echo "=== 2. Creating tables (db.create_all) once ==="
# Gunicorn起動前に一回だけテーブルを作成
python -c "from run import app; from app.main import db; app.app_context().push(); db.create_all()"

echo "=== 3. Seeding data (optional) ==="
# シードのみ別のワンライナーやスクリプトで行いたい場合
# python -c "from run import app; from app.main import seed_data; app.app_context().push(); seed_data()"

echo "=== 4. Starting Gunicorn ==="
exec gunicorn -w 2 -b 0.0.0.0:8080 run:app
