from flask import Flask
from app.main.config import Config
from app.main.routes import main_bp
from app.main.models import db, Text
from app.auth.routes import auth
import os

def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(os.getcwd(), 'templates'),
        static_folder=os.path.join(os.getcwd(), 'static')
        )
    app.config.from_object(Config)

    # データベースの初期化
    db.init_app(app)

    # Blueprint登録
    app.register_blueprint(main_bp)
    app.register_blueprint(auth, url_prefix='/auth')

    # データベースのテーブル作成と初期データ登録
    with app.app_context():
        db.create_all()
        seed_data()  # 初期データ登録関数を呼び出し

    return app

def seed_data():
    """初期データをデータベースに登録する関数"""
    if not Text.query.first():  # データが存在しない場合のみ登録
        sample_texts = [
            {"title": "クローラー", "pdf_path": "uploads/星1クローラー.pdf", "context": "クローラーの内容"},
            {"title": "ロボットハンド", "pdf_path": "uploads/星1ロボットハンド.pdf", "context": "ロボットハンドの内容"},
        ]
        for text in sample_texts:
            new_text = Text(title=text["title"], pdf_path=text["pdf_path"], context=text["context"])
            db.session.add(new_text)
        db.session.commit()
        print("初期データが登録されました。")

