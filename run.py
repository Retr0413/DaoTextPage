from app.main import create_app
from app.main.models import db
import os

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    is_debug = os.getenv("FLASK_ENV") == "development"
    app.run(debug=True, host="0.0.0.0", port=8080)