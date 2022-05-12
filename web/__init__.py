# vår app, vart den startar och konf. Vi kopplar ihop allt här.

from flask import Flask, render_template, session, request, redirect, url_for

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "EnSträng"   #någonting för säkerhet, hashar strängen till en nyckel av något slag

    from .views import views #här hämtar vi router i views som blueprint ifrån views.py
    from .auth import auth #här hämtar vi router i auth som blueprint ifrån auth.py  

    app.register_blueprint(views, url_prefix='/') #nu registerar vi den och prefix 
    app.register_blueprint(auth, url_prefix='/') #nu registerar vi den och prefix 

    return app