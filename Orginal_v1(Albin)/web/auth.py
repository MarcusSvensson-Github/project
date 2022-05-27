from flask import Blueprint, render_template, session, request, redirect, url_for, flash, g
import functools
from .db import get_db # funktion för att läsa databas
from werkzeug.security import check_password_hash, generate_password_hash

auth = Blueprint('auth', __name__)

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if g.user is not None:
        return redirect(url_for('views.home'))
    if request.method == 'POST':
        # 1. ta in username, password från request.form
        username = request.form['username']
        password = request.form['password']

        error = None
        # 2. kolla om username finns i databas
        db = get_db()
        db.ping()

        with db:
            with db.cursor() as cursor:

                sql = 'SELECT * FROM customers WHERE username= %s'

                cursor.execute(sql, (username))
                user = cursor.fetchone()

                if user is None:
                    error = 'Wrong username'
                elif not check_password_hash(user['password'], password):
                    error = 'Wrong password'

                if error is None:
                    session.clear()
                    session['user'] = user['username']
                    return redirect(url_for('views.home'))
                    
                flash(error)
    
    return render_template('login.html')


@auth.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('views.home'))


@auth.route('/sign_up', methods=('GET', 'POST'))
def sign_up():
    if request.method == 'POST':
        # för hashing använd
        # from werkzeug.security import check_password_hash, generate_password_hash

        #  ta in username, password från request.form
        username = request.form['username']
        password = request.form['password']
        phone = request.form['phone']
        mail = request.form['mail']

        # kolla så att fälten inte är tomma
        error = None
        if not username:
            error = 'Username is required'
        elif not password:
            error = 'password is required'
        elif not phone:
            error = 'phone number is required'
        elif not mail:
            error = 'mail is required'

        # kolla så att användaren inte redan finns i databasen
        db = get_db()
        db.ping()
        if error is None:
            try:
                with db:
                    with db.cursor() as cursor:
                        sql = "INSERT INTO customers(username, password, phone, email) VALUES (%s, %s, %s, %s)"
                        cursor.execute(
                            sql, (username, generate_password_hash(password), phone, mail))
                    db.commit()
            except db.IntegrityError:
                error = f'user {username} is already registered'
                
            else:
                return redirect(url_for('auth.login'))
        flash(error)

    return render_template('sign-up.html')


@auth.before_app_request
def load_logged_in_user():
    user = session.get('user')
    if user is None:
        g.user = None
    else:
        db = get_db()
        sql = 'SELECT * FROM customers WHERE username=%s'
        with db:
            with db.cursor() as cursor:
                cursor.execute(sql, (user))
                g.user = cursor.fetchone()



