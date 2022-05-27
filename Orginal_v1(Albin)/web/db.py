import click
import pymysql.cursors

from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(host='127.0.0.1',
                               user='root',
                               password='12345'.encode().decode('latin1'),
                               database='market',
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)

    return g.db

