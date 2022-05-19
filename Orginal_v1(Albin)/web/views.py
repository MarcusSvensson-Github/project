from flask import Blueprint, render_template, session, request, redirect, url_for

views = Blueprint('views', __name__)


@views.route('/')
@views.route('/home')
def home():
    return render_template('index.html')
