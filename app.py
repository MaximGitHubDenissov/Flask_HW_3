from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from flask_wtf import CSRFProtect
from models import db, User
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'c48cdcd33d0ab98719cef621e1b663d5bbc26fdd7b64997f8add7dbec9f6fa0b'
db.init_app(app)
csrf = CSRFProtect(app)


# >>> import secrets
# >>> secrets.token_hex()

@app.cli.command('init-db')
def init_db():
    db.create_all()
    print('База данных создана')


@app.route('/')
def base():
    res = make_response(redirect(url_for('login')))
    res.delete_cookie('user_name')
    return res


@app.route('/login/', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    context = {'title': 'login',
               'form': form}
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data
        check = User.query.filter_by(user_email=email).first()
        print(email)
        print(check)
        if check and check.user_email == email:
            if check.user_password == password:
                res = make_response(redirect(url_for('main')))
                res.set_cookie('user_name', check.user_name, max_age=60 * 60 * 24 * 365 * 2)
                flash('Авторизация успешна!', 'success')
                return res
            flash('Неправильный пароль!', 'danger')
            return redirect(url_for('login'))
        flash('Пользователь с таким email не зарегистрирован!', 'danger')
        return redirect(url_for('login'))

    return render_template('login.html', **context)


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    form = RegistrationForm()
    context = {'title': 'registration',
               'form': form}
    if request.method == 'POST' and form.validate():
        print(form.user_name.data, form.user_last_name.data, form.user_email.data, form.user_password.data)
        user = User(user_name=form.user_name.data,
                    user_last_name=form.user_last_name.data,
                    user_password=form.user_password.data,
                    user_email=form.user_email.data)
        check = User.query.filter_by(user_email=user.user_email).first()
        if check is not None and check.user_email == user.user_email:
            flash('Пользователь с таким email уже добавлен!', 'danger')
            return redirect(url_for('registration'))
        else:
            db.session.add(user)
            db.session.commit()
            print('User добавлен')
            flash('Учетная запись создана!', 'success')
            return redirect(url_for('login'))
    return render_template('registration.html', **context)


@app.route('/main/')
def main():
    context = {'title': 'main',
               'user': None
               }
    if not request.cookies.get('user_name'):
        context['user'] = 'Незнакомец'
    else:
        context['user'] = request.cookies.get('user_name')
    return render_template('main.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
