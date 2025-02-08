
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Text(db.Model):
    __tablename__ = 'texts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    context = db.Column(db.Text, nullable=True)
    mechanism = db.Column(db.String(100), nullable=True)
    pdf_path = db.Column(db.String(200), nullable=True)
    text_png = db.Column(db.String(200), nullable=True)
    stars = db.Column(db.Integer, nullable=False)

class PublicPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creator_name = db.Column(db.String(100), nullable=False)
    image_path = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<PublicPost {self.creator_name}>'
