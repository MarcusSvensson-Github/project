# Här har vi allt relaterat till authentisering som login, skapa konto och routes till personliga sidor.

from flask import Blueprint, render_template, session, request, redirect, url_for

auth = Blueprint('auth', __name__) #vi lägger till blueprints så vi kan anropa den i annan fil

@auth.route('/login') #finns här men anropas i init
def login():
    return 'login'

@auth.route('/logout') #finns här men anropas i init
def logout():
    return 'logout'

@auth.route('/sign-up') #finns här men anropas i init
def sign_up():
    return 'sign-up'