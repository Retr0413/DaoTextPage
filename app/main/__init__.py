from flask import Flask
from app.main.config import Config
from app.main.routes import main_bp
from app.main.models import db

def create_app():
    app = Flask(__name__, template_folder='../../templates', static_folder='../static')
    app.config.from_object(Config)

    # SQLAlchemyの初期化
    db.init_app(app)

    # Blueprint登録
    app.register_blueprint(main_bp)

    # データベースの初期化
    with app.app_context():
        db.create_all()

    return app
