from flask import Blueprint, render_template, request, redirect, url_for, session, flash, send_from_directory
from app.main.models import db, Text
from werkzeug.utils import secure_filename
from PyPDF2 import PdfFileReader
import os
from sqlalchemy import or_

main_bp = Blueprint('main', __name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')  
ALLOWED_EXTENSIONS = {'pdf'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def login_required(func):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@main_bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@main_bp.route('/')
def index():
    selected_mechanisms = request.args.getlist('mechanisms')
    print(f"Selected mechanisms: {selected_mechanisms}")  # デバッグ用
    texts = Text.query
    if selected_mechanisms:
        filters = [Text.mechanism.contains(mechanism) for mechanism in selected_mechanisms]
        texts = texts.filter(or_(*filters))
    texts = texts.all()

    texts_by_star = {}
    for text in texts:
        texts_by_star.setdefault(text.stars, []).append(text)

    return render_template('index.html', texts_by_star=texts_by_star, selected_mechanism=selected_mechanisms)

@main_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        title = request.form['title']
        file = request.files['file']

        if 'file' not in request.files or file.filename == '':
            flash('ファイルがアップロードされていません。')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            reader = PdfFileReader(file_path)
            pdf_content = ""
            for page in reader.pages:
                pdf_content += page.extract_text()

            text = Text(title=title, context=pdf_content, pdf_path=filename)
            db.session.add(text)
            db.session.commit()
            return redirect(url_for('main.index'))

    return render_template('add.html')

@main_bp.route('/text/<int:id>')
def text_detail(id):
    text = Text.query.get_or_404(id)
    return render_template('text.html', text=text)

@main_bp.route('/mechanism', methods=['GET', 'POST'])
def mechanism():
    return render_template('mechanism.html')

@main_bp.route('/mechanism/gears', methods=['GET'])
def gears():
    return render_template('gear_mechanism.html')

@main_bp.route('/mechanism/movement', methods=['GET'])
def movement():
    return render_template('movement_mechanism.html')

@main_bp.route('/mechanism/basic', methods=['GET'])
def basic_mechanisms():
    return render_template('basic_mechanism.html')

@main_bp.route('/mechanism/sensors', methods=['GET'])
def sensors():
    return render_template('sensors_mechanism.html')

@main_bp.route('/mechanism/special', methods=['GET'])
def special_mechanisms():
    return render_template('special_mechanism.html')