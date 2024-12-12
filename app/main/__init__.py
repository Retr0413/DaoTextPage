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

    db.init_app(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(auth)

    with app.app_context():
        db.create_all()
        seed_data()  

    return app

def seed_data():
    """初期データをデータベースに登録する関数"""
    if not Text.query.first():  
        sample_texts = [
            {"title": "クローラー", "pdf_path": "uploads/星1クローラー.pdf", "text_png" : "uploads/クローラー.png", "context": "クローラーの内容", "mechanism": "クローラー" "走る", "stars": 1},
            {"title": "ロボットハンド", "pdf_path": "uploads/星1ロボットハンド.pdf", "text_png" : "uploads/ロボットハンド.png", "context": "ロボットハンドの内容", "mechanism": "リンク機構", "stars": 1},
            {"title": "たじたじくん", "pdf_path": "uploads/星1たじたじくん.pdf", "text_png" : "uploads/たじたじくん.png", "context": "たじたじくんの内容", "mechanism": "ラチェット" "すり足", "stars": 1},
            {"title": "エレベーター", "pdf_path": "uploads/星2エレベーター.pdf", "text_png" : "uploads/エレベーター.png", "context": "エレベーターの内容", "mechanism": "ラックギア", "stars": 2},
            {"title": "ターンテーブル", "pdf_path": "uploads/星2ターンテーブル.pdf", "text_png" : "uploads/ターンテーブル.png", "context": "ターンテーブルの内容", "mechanism": "ターンテーブル", "stars": 2},
            {"title": "モノレール", "pdf_path": "uploads/星3モノレール.pdf", "text_png" : "uploads/モノレール.png", "context": "モノレールの内容", "mechanism": "べべルギア", "stars": 3},
            {"title": "ステアリングカー", "pdf_path": "uploads/星3ステアリングカー.pdf", "text_png" : "uploads/ステアリングカー.png", "context": "ステアリングカーの内容", "mechanism": "べべルギア", "stars": 3},
            {"title": "ライントレース", "pdf_path": "uploads/星3ライントレース.pdf", "text_png" : "uploads/ライントレース.png", "context": "ライントレースの内容", "mechanism": "べべルギア", "stars": 3},
            {"title": "二足歩行ロボット", "pdf_path": "uploads/星3二足歩行ロボット.pdf", "text_png" : "uploads/二足歩行ロボット.png", "context": "二足歩行ロボットの内容", "mechanism": "歩行", "stars": 3},
            {"title": "六足歩行ロボット", "pdf_path": "uploads/星4六足歩行ロボット.pdf", "text_png" : "uploads/六足歩行ロボット.png", "context": "六足歩行ロボットの内容", "mechanism": "歩行", "stars": 4},
        ]
        for text in sample_texts:
            new_text = Text(title=text["title"], pdf_path=text["pdf_path"], text_png=text["text_png"], context=text["context"], mechanism=text["mechanism"], stars=text["stars"])
            db.session.add(new_text)
        db.session.commit()
        print("初期データが登録されました。")
