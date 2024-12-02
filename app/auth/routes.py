from flask import jsonify, request, render_template, redirect, url_for, session, Blueprint, flash
from . import auth
from .services import login_service, register_service

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.json
        user = register_service(data)
        if user:
            return redirect(url_for('auth.login'))
        else:
            return render_template('register.html', error='ユーザー登録に失敗しました。')
    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = login_service(username, password)
        
        if user: # ログイン成功
            session['user_id'] = user['id']
            return redirect(url_for('main.add'))
        else: # ログイン失敗
            flash('ログインに失敗しました。')
            return redirect(url_for('auth.login'))
        
    return render_template('login.html')