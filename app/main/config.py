import os

class Config:
    SECRET_KEY = 'SecretKey'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:password@db:3306/flaskdb?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = False