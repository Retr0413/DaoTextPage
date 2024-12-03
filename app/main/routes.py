from flask import Blueprint, render_template, request, redirect, url_for, session, flash, send_from_directory
from app.main.models import db, Text
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
import os

main_bp = Blueprint('main', __name__)

# DaoTextPage直下のuploadsフォルダを指定
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')  
ALLOWED_EXTENSIONS = {'pdf'}

# アップロードフォルダが存在しない場合は作成
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    """許可された拡張子か確認"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def login_required(func):
    """ログイン必須デコレータ"""
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@main_bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """プロジェクト直下のuploadsフォルダ内のファイルを提供"""
    return send_from_directory(UPLOAD_FOLDER, filename)

@main_bp.route('/')
def index():
    """テキスト一覧ページ"""
    texts = Text.query.all()
    return render_template('index.html', texts=texts)

@main_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    """新しいPDFをアップロードして登録"""
    if request.method == 'POST':
        title = request.form['title']
        file = request.files['file']

        # ファイルがアップロードされていない場合
        if 'file' not in request.files or file.filename == '':
            flash('ファイルがアップロードされていません。')
            return redirect(request.url)

        # ファイルが許可された形式か確認
        if file and allowed_file(file.filename):
            # ファイルの保存
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            # PDFの内容を抽出
            reader = PdfReader(file_path)
            pdf_content = ""
            for page in reader.pages:
                pdf_content += page.extract_text()

            # データベースに保存
            text = Text(title=title, context=pdf_content, pdf_path=filename)
            db.session.add(text)
            db.session.commit()
            return redirect(url_for('main.index'))

    return render_template('add.html')

@main_bp.route('/text/<int:id>')
def text_detail(id):
    """個別のPDFテキスト表示"""
    text = Text.query.get_or_404(id)
    return render_template('text.html', text=text)
