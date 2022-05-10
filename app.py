from flask import Flask, render_template, request
app = Flask(__name__)


@app.route("/") #välkomnssida som kan skicka dig till login eller skapa konto
def index():
    return render_template('index.html')

@app.route("/login", methods['GET', 'POST'])
def login():   
    if request.method == 'POST':
        return do_login() #ej skapad funktion, bör skapa session?
    else:
        render_template('login.html') # vanliga loginsidan vi möts av vid login

@app.route("/private")
def private():
    return render_template('private.html')

@app.route("/product")
def product():
    return render_template('product.html')