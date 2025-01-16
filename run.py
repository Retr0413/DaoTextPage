import os
from app.main import create_app
from app.main.models import db
import logging

app = create_app()

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    db_path = os.path.join('static/uploads', 'app.db')
    if not os.path.exists(db_path):
        with app.app_context():
            db.create_all()
            print(f"Database initialized at: {db_path}")
    app.run(host="0.0.0.0", port=port)
