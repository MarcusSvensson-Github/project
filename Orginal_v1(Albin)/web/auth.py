from flask import Blueprint, render_template, session, request, redirect, url_for, flash

# funktion för att läsa databas
from .db import get_db

from werkzeug.security import check_password_hash, generate_password_hash


auth = Blueprint('auth', __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 1. ta in username, password från request.form
        # 2. kolla om username finns i databas
        # 2.1 om det inte finns ge error. Användaren har inte konto
        # 3. hasha lösenord och jämför med det hashade i databasen
        # 3.1 matchar det inte ge error. fel lösenord.
        # 4. sätt session['user_id'] = unikt id för användaren från databas
        # 5. redirecta användaren till lämplig sida ex index.

        # OBS INTE KORREKT SÄTT ATT GÖRA DETTA PÅ följ stegen ovan istället
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        print(session['username'], session['password'])

        # hämta user från databas
        #session['user_id'] = user['id']
        return redirect(url_for('views.home'))
        # else skapa konto
        # return redirect(url_for('create'))

    return render_template('login.html')


@auth.route('/logout')
def logout():
    session.clear()
    return 'logout'


@auth.route('/sign-up', methods=('GET', 'POST'))
def create_user():
    if request.method == 'POST':
        pass
        # för hashing använd
        # from werkzeug.security import check_password_hash, generate_password_hash

        # 1. ta in username, password från request.form
        username = request.form['username']
        password = request.form['password']
        phone = request.form['phone']
        mail = request.form['mail']

        # 2. kolla så att fälten inte är tomma
        error = None
        if not username:
            error = 'Username is required'
        elif not password:
            error = 'password is required'
        elif not phone:
            error = 'phone number is required'
        elif not mail:
            error = 'mail is required'

        # 3. kolla så att användaren inte redan finns i databasen
        db = get_db()
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

    # 4. lägg till username, password i databasen men hasha password först
    # 5. redirect user
    # return '''<p> SKAPA EN ANVÄNDARE </p>'''
