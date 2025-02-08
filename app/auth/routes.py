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
        result = login_service({'username': username, 'password': password})

        if isinstance(result, tuple):
            data, status_code = result
            flash(data.get('message', 'ログイン失敗'), 'danger')
            return render_template('login.html'), status_code

        if 'id' in result:
            session['user_id'] = result['id']
            session['username'] = result['username']
            session['user_type'] = result['user_type']  

            flash('ログインしました。', 'success')
            return redirect(url_for('main.index'))
        else:
            flash(result.get('message', 'ログイン失敗'), 'danger')
            return render_template('login.html')

    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.clear()
    flash('ログアウト', 'info')
    return redirect(url_for('auth.login'))