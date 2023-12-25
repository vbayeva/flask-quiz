from tabnanny import check
from flask import Blueprint, render_template, request, g, redirect, url_for, session
from flask_login import login_user, current_user, logout_user

from app.extenstions import db
from app.models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['login']
        password = request.form['password']

        user = User.query.filter_by(name=name).first()
        print(user)

        if not user or not user.check_password(password):
            return render_template('login.html', error_message = 'Nie udało się zalogować. Spróbuj ponownie')

        else:
            login_user(user)
            create_user_session(user)
            return redirect(url_for('main.index'))

    return render_template('login.html')

@auth.route('/logout')
def logout():
    logout_user()
    session.clear()
    return render_template('logout.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['username']
        unhashed_password = request.form['password']
        confirm_password = request.form['confirm_password']
        nickname = request.form['nickname']

        errors = []
        if (unhashed_password != confirm_password):
            errors.append('Hasła się nie zgadzają!')
        
        if not User.query.filter_by(name=name).first() is None:
            errors.append('Taki login już istnieje. Wybierz inny')

        if not User.query.filter_by(nickname=nickname).first() is None:
            errors.append('Taki pseudonim już istnieje. Wybierz inny')

        if errors:
            return render_template('register.html', errors=errors)

        user = User(
            name=name, 
            unhashed_password=unhashed_password, 
            nickname=nickname, 
            main_score=0, 
            is_admin=False
        )

        db.session.add(user)
        db.session.commit()

        login_user(user)
        create_user_session(user)

        return redirect(url_for('main.index'))
    
    return render_template('register.html')

def create_user_session(user):
    session['user_id'] = user.id
    session['user_nickname'] = user.nickname
    session['question_asked'] = 0