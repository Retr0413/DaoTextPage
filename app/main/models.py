from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Text(db.Model):
    __tablename__ = 'texts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    context = db.Column(db.Text, nullable=True)
    pdf_path = db.Column(db.String(200), nullable=True)