# Här kommer vi ha alla våra routes till olika sidor som utgör hemsidan

from flask import Blueprint, render_template, session, request, redirect, url_for

views = Blueprint('views', __name__) #vi lägger till blueprints så vi kan anropa den i annan fil

@views.route('/') #finns här men anropas i init
def home():
    return 'Home'