from google.cloud import storage
import os

def get_gcs_url(file_path):
    """Cloud Storage から指定されたファイルのURLを取得"""
    bucket_name = os.getenv("GCS_BUCKET_NAME", "daodaotext-data")

    # すでにURLならそのまま返す
    if file_path.startswith("http"):
        return file_path

    # Cloud Storage の公開 URL を返す
    return f"https://storage.googleapis.com/{bucket_name}/{os.path.basename(file_path)}"
