from flask import Blueprint, render_template, request, redirect, url_for, session, flash, send_from_directory, make_response, jsonify, current_app
from app.main.models import db, Text, PublicPost
from werkzeug.utils import secure_filename
from PyPDF2 import PdfFileReader
import os
from sqlalchemy import or_

main_bp = Blueprint('main', __name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static/uploads')  
ALLOWED_EXTENSIONS = {'pdf', 'png'}
PDF_COOKIE_NAME = "text_access_token"
PDF_COOKIE_VALUE = "text_secure_token"

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

@main_bp.route('/public_post', methods=['GET', 'POST'])
def public_post():
    if 'user_type' not in session:
        flash('ログインしてください。')
        return redirect(url_for('main.login'))

    if request.method == 'POST':
        creator_name = request.form['creator_name']
        image_file = request.files.get('image_file')
        if not creator_name or not image_file:
            flash('必要な情報を入力してください。')
            return redirect(url_for('main.public_post'))
        
        filename = secure_filename(image_file.filename)
        upload_path = os.path.join(current_app.config.get("UPLOAD_FOLDER", "static/uploads"), filename)
        image_file.save(upload_path)

        new_post = PublicPost(creator_name=creator_name, image_path=filename)
        db.session.add(new_post)
        db.session.commit()

        flash('新しい投稿が追加されました。')
        return redirect(url_for('main.public_post'))
    
    return render_template('public_post.html')

@main_bp.route('/public_posts')
def public_posts():
    posts = PublicPost.query.order_by(PublicPost.id.desc()).all()
    return render_template('public_posts.html', posts=posts)

@main_bp.route('/delete_post/<int:id>', methods=['POST'])
def delete_post(id):
    if session.get('user_type') != 'User':
        flash("権限がありません")
        return redirect(url_for('main.public_post'))
    post = PublicPost.query.get(id)
    if post:
        db.session.delete(post)
        db.session.commit()
        flash('投稿を削除しました。')
    else:
        flash('投稿が見つかりません。')
    
    return redirect(url_for('main.public_posts'))

@main_bp.route('/set_pdf_cookie')
def set_pdf_cookie():
    response = make_response(redirect(url_for('main.index')))
    response.set_cookie(PDF_COOKIE_NAME, PDF_COOKIE_VALUE)
    flash('Cookieを設定しました。')
    return response

@main_bp.route('/secure_pdf/<path:filename>')
def secure_pdf(filename):
    token = request.cookies.get(PDF_COOKIE_NAME)
    if token != PDF_COOKIE_VALUE:
        return redirect(url_for('main.index'))

    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=False)
    else:
        return redirect(url_for('main.index'))

@main_bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@main_bp.route('/')
def index():
    selected_mechanisms = request.args.getlist('mechanisms')
    sort_by_likes = request.args.get('sort_by_likes') == 'on'
    print(f"Selected mechanisms: {selected_mechanisms}")  # デバッグ用
    texts = Text.query
    if selected_mechanisms:
        filters = [Text.mechanism.contains(mechanism) for mechanism in selected_mechanisms]
        texts = texts.filter(or_(*filters))
    texts = texts.all()

    texts_by_star = {}
    for text in texts:
        texts_by_star.setdefault(text.stars, []).append(text)

    if sort_by_likes:
        for star in texts_by_star:
            texts_by_star[star] = sorted(texts_by_star[star], key=lambda x: x.likes, reverse=True)

    return render_template('index.html', texts_by_star=texts_by_star, selected_mechanism=selected_mechanisms)

@main_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        title = request.form['title']
        stars = int(request.form['stars'])
        mechanism = request.form['mechanism']
        pdf_file = request.files.get('pdf_file')
        png_file = request.files.get('png_file')

        if not title or not stars or not pdf_file or not png_file:
            flash('すべての項目を入力してください。')
            return redirect(request.url)
        
        if pdf_file and allowed_file(pdf_file.filename) and png_file and allowed_file(png_file.filename):
            pdf_filename = secure_filename(pdf_file.filename)
            png_filename = secure_filename(png_file.filename)

            pdf_path = os.path.join(UPLOAD_FOLDER, pdf_filename)
            png_path = os.path.join(UPLOAD_FOLDER, png_filename)
            pdf_file.save(pdf_path)
            png_file.save(png_path)

            pdf_context = ""
            try:
                reader = PdfFileReader(pdf_path)
                for page in reader.pages:
                    pdf_context += page.extract_text()
            except Exception as e:
                flash(f'PDFファイルの読み込みに失敗しました: {e}')
                return redirect(request.url)
            
            new_text = Text(
                title=title,
                pdf_path=f'uploads/{pdf_filename}',
                text_png=f'uploads/{png_filename}',
                context=pdf_context,
                mechanism=mechanism,
                stars=stars
            )
            db.session.add(new_text)
            db.session.commit()

            flash('新しいテキストが追加されました。')
            return redirect(url_for('main.index'))
        
        flash('PDFファイルとPNGファイルをアップロードしてください。')
        return redirect(request.url)
    
    return render_template('add.html')

@main_bp.route('/text/<int:id>')
def text_detail(id):
    text = Text.query.get_or_404(id)
    return render_template('text.html', text=text)

@main_bp.route('/like/<int:id>', methods=['POST'])
def like_text(id):
    text = Text.query.get_or_404(id)
    text.likes += 1
    db.session.commit()
    return jsonify({'id': text.id, 'likes': text.likes})

@main_bp.route('/reset_like/<int:id>', methods=['POST'])
def reset_like_text(id):
    if session.get('user_type') != 'User':
        return jsonify({'error': '権限がありません'}), 403
    text = Text.query.get_or_404(id)
    text.likes = 0
    db.session.commit()
    return jsonify({'id': text.id, 'likes': text.likes})

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