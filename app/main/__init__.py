from flask import Flask
from app.main.config import Config
from app.main.routes import main_bp
from app.main.models import db, Text
from app.auth.models import User
from app.auth.models import Public_User
from app.auth.routes import auth
from werkzeug.security import generate_password_hash
from flask_migrate import Migrate
from sqlalchemy.exc import OperationalError
from sqlalchemy import text
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
import os
import time

migrate = Migrate()

# limiter = Limiter(
#     get_remote_address,
#     default_limits=["300 per day", "60 per hour"],
# )

# csp = {
#     'default-src': ['\'self\''],  # デフォルトは自ドメインのみ許可
#     'style-src': [
#         '\'self\'',  # 自身のCSSを許可
#         'https://fonts.googleapis.com',  # Google Fonts（必要な場合）
#         'https://cdn.jsdelivr.net'  # Bootstrap CDN（必要な場合）
#     ],
#     'script-src': [
#         '\'self\'',  # 自身のJavaScriptを許可
#         'https://cdn.jsdelivr.net'  # Bootstrap JS（必要な場合）
#     ],
#     'font-src': [
#         '\'self\'',
#         'https://fonts.gstatic.com'  # Google Fonts（必要な場合）
#     ],
#     'img-src': [
#         '\'self\'',  # 自身の画像を許可
#         'data:',  # Base64エンコード画像を許可
#         'https://cdn.jsdelivr.net'  # 必要に応じて外部画像を許可
#     ],
#     'object-src': [
#         '\'self\'',  # 自身のPDFを許可
#         'data:'  # Base64エンコードされたPDFを許可
#     ]
# }

# talisman = Talisman(content_security_policy=csp)

# def wait_for_db(app):
#     """Wait for the database to be ready."""
#     retries = 10
#     while retries > 0:
#         try:
#             with app.app_context():
#                 # 単純なクエリを投げてDBと通信できるか確認
#                 db.session.execute(text('SELECT 1'))  
#             print("Database is ready!")
#             return
#         except OperationalError:
#             retries -= 1
#             print(f"Database not ready, retrying... ({5 - retries}/5)")
#             time.sleep(3)
#     raise Exception("Database is not ready after 5 retries")

def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(os.getcwd(), 'templates'),
        static_folder=os.path.join(os.getcwd(), 'static')
    )
    app.config.from_object(Config)

    # SQLAlchemy と Flask-Migrate の初期化
    db.init_app(app)
    migrate.init_app(app, db)

    # talisman.init_app(app)

    # limiter.init_app(app)

    # Blueprint の登録
    app.register_blueprint(main_bp)
    app.register_blueprint(auth)

    # アプリコンテキストで実行
    with app.app_context():
        # 1. DB 接続が完了するまで待機
        # wait_for_db(app)

        # 2. テーブルを先に作成
        db.create_all()

        # 3. テーブル作成後にシードデータを投入
        seed_data()

    return app

def seed_data():
    """初期データをデータベースに登録する関数"""
    # User テーブルの初期登録
    if not User.query.first():
        initial_user = User(
            id=1,
            username='daodao', 
            password_hash=generate_password_hash('DefaultTakuma', method='pbkdf2:sha256')
        )
        db.session.add(initial_user)

    if not Public_User.query.first():
        initial_user = Public_User(
            id=1,
            username='Shake', 
            password_hash=generate_password_hash('Shake', method='pbkdf2:sha256')
        )
        db.session.add(initial_user)

    # Text テーブルの初期登録
    if not Text.query.first():
        base_texts = [
            {
                "title": "クローラー",
                "pdf_path": "uploads/星1クローラー.pdf",
                "text_png": "uploads/クローラー.png",
                "context": "みんな大好きクローラー。凸凹な地形も走れる",
                "mechanism": ["クローラー", "走る"],
                "stars": 1
            },
            {
                "title": "ロボットハンド",
                "pdf_path": "uploads/星1ロボットハンド.pdf",
                "text_png": "uploads/ロボットハンド.png",
                "context": "めっちゃ簡単なロボットハンド。UFOキャッチャーなどでつかえるかも？",
                "mechanism": ["リンク機構"],
                "stars": 1
            },
            {
                "title": "たじたじくん",
                "pdf_path": "uploads/星1たじたじくん.pdf",
                "text_png": "uploads/たじたじくん.png",
                "context": "歩きも走りもしない、不思議なロボット。一方向にしか回転しないよ。",
                "mechanism": ["ラチェット", "すり足"],
                "stars": 1
            },
            {
                "title": "エレベーター",
                "pdf_path": "uploads/星2エレベーター.pdf",
                "text_png": "uploads/エレベーター.png",
                "context": "ラックギアを使ったエレベーター。簡単にレールを伸ばせるよ。",
                "mechanism": ["ラックギア", "昇降機構"],
                "stars": 2
            },
            {
                "title": "ターンテーブル",
                "pdf_path": "uploads/星2ターンテーブル.pdf",
                "text_png": "uploads/ターンテーブル.png",
                "context": "回転する土台だね。",
                "mechanism": ["ターンテーブル", "回転する台"],
                "stars": 2
            },
            {
                "title": "モノレール",
                "pdf_path": "uploads/星3モノレール.pdf",
                "text_png": "uploads/モノレール.png",
                "context": "カラーセンサーを使って駅に止まれるよ。輪ゴムではなく、ベベルギアを使ってみよう‼",
                "mechanism": ["べべルギア", "カラーセンサー"],
                "stars": 3
            },
            {
                "title": "ステアリングカー",
                "pdf_path": "uploads/星3ステアリングカー.pdf",
                "text_png": "uploads/ステアリングカー.png",
                "context": "タイヤ4つだけど曲がれるくるま。プログラムが難しいかも",
                "mechanism": ["べべルギア", "走る", "ターンテーブル"],
                "stars": 3
            },
            {
                "title": "ライントレース",
                "pdf_path": "uploads/星3ライントレース.pdf",
                "text_png": "uploads/ライントレース.png",
                "context": "モーター1つで左右に曲がれるよ。走らせるラインが必要だよ。",
                "mechanism": ["べべルギア", "カラーセンサー", "ライントレース"],
                "stars": 3
            },
            {
                "title": "二足歩行ロボット",
                "pdf_path": "uploads/星3二足歩行ロボット.pdf",
                "text_png": "uploads/二足歩行ロボット.png",
                "context": "重心を移動させながらペンギン歩き。",
                "mechanism": ["歩行", "重心移動"],
                "stars": 3
            },
            {
                "title": "六足歩行ロボット",
                "pdf_path": "uploads/星4六足歩行ロボット.pdf",
                "text_png": "uploads/六足歩行ロボット.png",
                "context": "6本の足でとことこ歩くよ。上級者向けだね‼",
                "mechanism": ["歩行", "リンク機構", "ノブホイールギア"],
                "stars": 4
            },
        ]
        for text_data in base_texts:
            new_text = Text(
                title=text_data["title"],
                pdf_path=text_data["pdf_path"],
                text_png=text_data["text_png"],
                context=text_data["context"],
                mechanism=", ".join(text_data["mechanism"]),
                stars=text_data["stars"]
            )
            db.session.add(new_text)

    db.session.commit()
    print('初期データの登録が完了しました。')