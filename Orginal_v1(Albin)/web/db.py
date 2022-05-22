import click
import pymysql.cursors

from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(host='127.0.0.1',
                               user='root',
                               password='password123'.encode().decode('latin1'),
                               database='projekt',
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


""" def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command) """


""" connection = pymysql.connect(host='dsd400.port0.org',
                             user='dsd400',
                             password='krångligt_'.encode().decode('latin1'),
                             database='mindatabas',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
with connection:
    with connection.cursor() as cursor:
        # Read records
        cursor.execute("SELECT * FROM Student")
        result = cursor.fetchall()
        pprint.pp(result)
        
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO Student (namn, telefonnr) VALUES (%s, %s)"
        cursor.execute(sql, ('Cecilia', '232323')) """
