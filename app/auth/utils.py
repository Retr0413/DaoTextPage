from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password):
    return generate_password_hash(password, method='sha256')

def verify_password(password_hash, password):
    return check_password_hash(password_hash, password)

from google.cloud import storage

BUCKET_NAME = "daodaotext-data"

def get_gcs_url(filename):
    return f"https://storage.googleapis.com/{BUCKET_NAME}/{filename}"