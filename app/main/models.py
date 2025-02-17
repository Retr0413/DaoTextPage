import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.main.utils import get_gcs_url 

class Text(db.Model):
    __tablename__ = 'texts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    context = db.Column(db.Text, nullable=True)
    mechanism = db.Column(db.String(100), nullable=True)
    pdf_path = db.Column(db.String(200), nullable=True)
    text_png = db.Column(db.String(200), nullable=True)
    stars = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False, default=0)

    @property
    def pdf_url(self):
        """GCS から署名付きURLを取得"""
        return get_gcs_url(self.pdf_path)

    @property
    def image_url(self):
        """GCS から画像の署名付きURLを取得"""
        return get_gcs_url(self.text_png)

class PublicPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creator_name = db.Column(db.String(100), nullable=False)
    image_path = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<PublicPost {self.creator_name}>'