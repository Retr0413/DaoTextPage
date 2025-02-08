from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Public_User
from app.main.models import db

def register_service(data):
    """
    新しいユーザーを登録するサービス関数。
    """
    try:
        hashed_password = generate_password_hash(data['password'], method='sha256')
       
        user = User(username=data['username'], password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
     
        return {'id': user.id, 'username': user.username}
    except Exception as e:
        db.session.rollback()
        return {'message': 'ユーザー登録中にエラーが発生しました。', 'error': str(e)}

def login_service(data):
    """
    ユーザーのログインを処理するサービス関数。
    """
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password_hash, data['password']):
        return {'id': user.id, 'username': user.username, 'message': 'ログインしました。', 'user_type': "User"}
    
    public_user = Public_User.query.filter_by(username=data['username']).first()
    if public_user and check_password_hash(public_user.password_hash, data['password']):
        return {'id': public_user.id, 'username':public_user.username, 'message': 'ログインしました。', 'user_type': "Public_User"}
     

    return {'message': 'ユーザー名またはパスワードが違います。'}, 401