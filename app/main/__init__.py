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
        base_texts = [
            {"title": "クローラー", "pdf_path": "uploads/星1クローラー.pdf", "text_png" : "uploads/クローラー.png", "context": "みんな大好きクローラー。凸凹な地形も走れる", "mechanism": "クローラー" "走る", "stars": 1},
            {"title": "ロボットハンド", "pdf_path": "uploads/星1ロボットハンド.pdf", "text_png" : "uploads/ロボットハンド.png", "context": "めっちゃ簡単なロボットハンド。UFOキャッチャーなどでつかえるかも？", "mechanism": "リンク機構", "stars": 1},
            {"title": "たじたじくん", "pdf_path": "uploads/星1たじたじくん.pdf", "text_png" : "uploads/たじたじくん.png", "context": "歩きも走りもしない、不思議なロボット。一方向にしか回転しないよ。", "mechanism": "ラチェット" "すり足", "stars": 1},
            {"title": "エレベーター", "pdf_path": "uploads/星2エレベーター.pdf", "text_png" : "uploads/エレベーター.png", "context": "ラックギアを使ったエレベーター。簡単にレールを伸ばせるよ。", "mechanism": "ラックギア" "昇降機構", "stars": 2},
            {"title": "ターンテーブル", "pdf_path": "uploads/星2ターンテーブル.pdf", "text_png" : "uploads/ターンテーブル.png", "context": "回転する土台だね。", "mechanism": "ターンテーブル" "回転する台", "stars": 2},
            {"title": "モノレール", "pdf_path": "uploads/星3モノレール.pdf", "text_png" : "uploads/モノレール.png", "context": "カラーセンサーを使って駅に止まれるよ。輪ゴムではなく、ベベルギアを使ってみよう‼", "mechanism": "べべルギア" "カラーセンサー", "stars": 3},
            {"title": "ステアリングカー", "pdf_path": "uploads/星3ステアリングカー.pdf", "text_png" : "uploads/ステアリングカー.png", "context": "タイヤ4つだけど曲がれるくるま。プログラムが難しいかも", "mechanism": "べべルギア" "走る" "ターンテーブル", "stars": 3},
            {"title": "ライントレース", "pdf_path": "uploads/星3ライントレース.pdf", "text_png" : "uploads/ライントレース.png", "context": "モーター1つで左右に曲がれるよ。走らせるラインが必要だよ。", "mechanism": "べべルギア" "カラーセンサー" "ライントレース", "stars": 3},
            {"title": "二足歩行ロボット", "pdf_path": "uploads/星3二足歩行ロボット.pdf", "text_png" : "uploads/二足歩行ロボット.png", "context": "重心を移動させながらペンギン歩き。", "mechanism": "歩行" "重心移動", "stars": 3},
            {"title": "六足歩行ロボット", "pdf_path": "uploads/星4六足歩行ロボット.pdf", "text_png" : "uploads/六足歩行ロボット.png", "context": "6本の足でとことこ歩くよ。上級者向けだね‼", "mechanism": "歩行" "リンク機構" "ノブホイールギア", "stars": 4},
        ]
        for text in base_texts:
            new_text = Text(title=text["title"], pdf_path=text["pdf_path"], text_png=text["text_png"], context=text["context"], mechanism=text["mechanism"], stars=text["stars"])
            db.session.add(new_text)
        db.session.commit()
        print("初期データが登録されました。")
