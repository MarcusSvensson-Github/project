from pymysql import IntegrityError
from .auth import login_required  
from .db import get_db
from flask import Blueprint, render_template, session, request, redirect, url_for, g, flash
import datetime, time

views = Blueprint('views', __name__)


@views.route('/')
@views.route('/home')
def home():
    db = get_db()
    db.ping()

    with db:
        with db.cursor() as cursor:   # hämta produkterna i våran sql för att visa på index sidan
            sql = 'SELECT * FROM sell inner join product on sell.product=product.productID'
            cursor.execute(sql)
            g.IndexProducts = cursor.fetchall()
    return render_template('index.html')

@views.route('/buy/<productID>', methods=('GET', 'POST'))
@login_required  
def buy(productID):
    if request.method == 'POST': #om någon klickar på köp knappen
        db = get_db()
        db.ping() 
        with db:
            with db.cursor() as cursor:   #hämta produkterna i våran sql för att visa på index sidan
                sqlinfo = 'SELECT * FROM sell inner join product on sell.product=product.productID where productID=%s'
                if cursor.execute(sqlinfo, (productID)) == 0: #kollar om produkten finns i databas
                    return redirect(url_for('views.fail')) 
                else:    
                    sqlinfo = cursor.fetchone()
                    date = datetime.datetime.now()
                    buyer = g.user['username']
                    productID = sqlinfo['productID']

                    db.begin()  # börja transaktion 
                    sql = 'INSERT INTO buy VALUES(%s, %s, %s)' #lägg till i buy tabell 
                    cursor.execute(sql, (buyer, productID, date)) 

                    sql = 'DELETE FROM sell where product=%s' #tar bort product i sell tabell
                    cursor.execute(sql, (productID))
                    
                    db.commit()            # commit (avslutar transaktionen)

                    msg = 'Your bought an item :)'
                    flash(msg)
                    return redirect(url_for('views.home'))

    db = get_db()
    db.ping()  

    #finns produkten kvar i databasen?
    with db:
        with db.cursor() as cursor:  
            sql = 'SELECT * FROM sell inner join product on sell.product=product.productID where productID=%s'
            if cursor.execute(sql, (productID)) == 0:
                return redirect(url_for('views.fail'))
            else:
                g.buyProducts = cursor.fetchone()
    return render_template('buy.html')

@views.route('/fail')
@login_required  
def fail():
    return render_template('fail.html')


@views.route('/sell', methods=('GET', 'POST'))
@login_required  
def sell():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        price = request.form['price']

        # g.user['username'])
        # nu ska anonnsen registreras i databasen med fälten
        # title, description, pris, användare

        error = None

        if not title:
            error = "Title is empty"
        elif not description:
            error = "Description is empty"
        elif not price:
            error = "Price is empty"

        if error is None:  # alla fält har hämtats korrekt och vi kan lägga till i databasen
            db = get_db()
            db.ping()

            try:
                with db:
                    with db.cursor() as cursor:   #insertar produkt i sql
                        sql = (
                            'INSERT INTO product(title, price, description) VALUES (%s, %s, %s)')
                       
                        cursor.execute(sql, (title, price, description))
                        db.commit()

                    with db.cursor() as cursor:     #hämtar först ID från senast produkt i sql så vi får ett unikt ID att koppla informationen av produkten till
                        sql = 'SELECT productID FROM product where title=%s AND description=%s'
                        cursor.execute(sql, (title, description))
                        sellID = cursor.fetchone()
                        sellID = sellID['productID']
                        userID = g.user['username']
                        date = datetime.datetime.now()
                        sql = (
                            'INSERT INTO sell(user, product, creationDATE) VALUES(%s, %s, %s)'
                        )
                        cursor.execute(sql, (userID, sellID, date))
                        db.commit()

                    return redirect(url_for('views.home'))
            except db.IntegrityError:
                flash('något gick fel i databsen')

        else:
            flash(error)

    return render_template('product.html')
