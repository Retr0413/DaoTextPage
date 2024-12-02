from flask import Blueprint, render_template, request, redirect, url_for, session
from app.main.models import db, Text

main_bp = Blueprint('main', __name__)

def login_required(func):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


@main_bp.route('/')
def index():
    texts = Text.query.all()
    return render_template('index.html', texts=texts)

@main_bp.route('/add',methods=['GET','POST'])
@login_required
def add():
    if request.method == 'POST':
        title = request.form['title']
        context = request.form['context']
        text = Text(title=title, context=context)
        db.session.add(text)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('add.html')

@main_bp.route('/text/<int:id>')
def text(id):
    text = Text.query.get(id)
    return render_template('text.html', text=text)