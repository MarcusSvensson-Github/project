from pymysql import IntegrityError
from .auth import login_required  # tror inte detta är ett bra sätt att göra det på
# tror att man kan "registrera funktionen på något sätt"
from .db import get_db
from flask import Blueprint, render_template, session, request, redirect, url_for, g, flash
import datetime

views = Blueprint('views', __name__)


@views.route('/')
@views.route('/home')
def home():
    # vi vill läsa produkter ifrån sql och lägga i en lista 
    db = get_db()

    db.ping()  # <--- magisk skit som fixar allt?


    with db:
        with db.cursor() as cursor:   #hämta produkterna i våran sql för att visa på index sidan, hämtas i 3 listor som gås igenom och printas ut i index.html med jinja
            sql = 'SELECT * FROM sell inner join product on sell.product=product.productID'
            cursor.execute(sql)
            g.IndexProducts = cursor.fetchall()
            print(g.IndexProducts)
     
    return render_template('index.html')


@views.route('/buy/<productID>', methods=('GET', 'POST'))
@login_required  
def buy(productID):
    if request.method == 'POST': #om någon klickar på köp knappen
        db = get_db()
        db.ping()  # <--- magisk skit som fixar allt?

        #finns produkten kvar i databasen?
        with db:
            with db.cursor() as cursor:   #hämta produkterna i våran sql för att visa på index sidan
                sql = 'SELECT * FROM sell inner join product on sell.product=product.productID where productID=%s'
                if cursor.execute(sql, (productID)) == 0: #kollar om produkten finns i databas
                    return 'product not found'
                else:    
                    db.begin()  # börja transaktion 

                    sql = 'DELETE FROM sell where product=%s' #tar bort product i sell tabell
                    cursor.execute(sql, (productID))
                    sql = 'DELETE FROM product where productID=%s' #tar bort product i product tabell
                    cursor.execute(sql, (productID))
                    # ny tabell att spara i där du kan se dina köp?
                    
                    db.commit()            # commit (avslutar transaktionen)
                    
                    return redirect(url_for('views.home'))

    db = get_db()
    db.ping()  # <--- magisk skit som fixar allt?

    #finns produkten kvar i databasen?
    with db:
        with db.cursor() as cursor:   #hämta produkterna i våran sql för att visa på index sidan, hämtas i 3 listor som gås igenom och printas ut i index.html med jinja
            sql = 'SELECT * FROM sell inner join product on sell.product=product.productID where productID=%s'
            if cursor.execute(sql, (productID)) == 0:
                return 'product not found'
            else:
                g.buyProducts = cursor.fetchone()
                print(g.buyProducts)
    return render_template('buy.html')

@views.route('/sell', methods=('GET', 'POST'))
@login_required  
def sell():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        price = request.form['price']

        print(title, description, price)  # g.user['username'])
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

            db.ping()  # <--- magisk skit som fixar allt?

            try:
                with db:
                    with db.cursor() as cursor:   #insertar produkt i sql
                        sql = (
                            'INSERT INTO product(name, price, description) VALUES (%s, %s, %s)')
                       
                        cursor.execute(sql, (title, price, description))
                        db.commit()

                    with db.cursor() as cursor:     #hämtar först ID från senast produkt i sql
                        sql = 'SELECT productID FROM product where name=%s AND description=%s'
                        cursor.execute(sql, (title, description))
                        sellID = cursor.fetchone()
                        sellID = sellID['productID']
                        print(sellID)
                                                    #insertar produktID och säljarID med datum till sell table i sql
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
