from flask import Flask, render_template, session, request, redirect, url_for

app = Flask(__name__)
app.secret_key = b'test'  # <--- väldigt osäkert


@app.route("/")
def index():
    # if 'username' in session:
    #    return f'Logged in as {session["username"]}'
    # return 'You are not logged in'
    return render_template('index.html')


@app.route("/login", methods=['GET', 'POST'])
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
        return redirect(url_for('index'))
        # else skapa konto
        # return redirect(url_for('create'))

    return render_template('login.html')


@app.route('/create_user', methods=('GET', 'POST'))
def create_user():
    if request.method == 'POST':
        pass
        # för hashing använd
        # from werkzeug.security import check_password_hash, generate_password_hash

        # 1. ta in username, password från request.form
        # 2. kolla så att fälten inte är tomma
        # 3. kolla så att användaren inte redan finns i databasen
        # 4. lägg till username, password i databasen men hasha password först
        # 5. redirect user
    return '''<p> SKAPA EN ANVÄNDARE </p>'''

# behöver en function before_app_request för att kolla vilken användare som gör requesten,  g.user
# https://flask.palletsprojects.com/en/2.1.x/api/#flask.Blueprint.before_app_request


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route("/private")
def private():
    return render_template('private.html')


@app.route("/product")
def product():
    return render_template('product.html')


@app.route("/test")
def test():
    return render_template('test.html')
