from flask import Flask, render_template, request
app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/private")
def private():
    return render_template('private.html')

@app.route("/product")
def product():
    return render_template('product.html')


