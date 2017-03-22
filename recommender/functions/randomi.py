import random
import MySQLdb as mysli

def random_book(db):

    cursor = db.cursor()
    arv_sql = "SELECT DISTINCT * FROM `BX-Books`"
    books = []
    try:
        cursor.execute(arv_sql)
        books = cursor.fetchall()
    except mysli.Error as err:
        print err
        books = [('0195153448','Classical Mythology','Mark P. O. Morford',2002,'Oxford University Press','http://images.amazon.com/images/P/0195153448.01.THUMBZZZ.jpg','http://images.amazon.com/images/P/0195153448.01.MZZZZZZZ.jpg','http://images.amazon.com/images/P/0195153448.01.LZZZZZZZ.jpg')]


    book = random.choice(books)
    isbn = book[0]

    return isbn

def pick_users(db):
    cursor = db.cursor()
    #Ottaa ne kayttajat, jotka ovat arvostelleet eniten
    select_users_sql = "SELECT `User-ID` as user_id ,COUNT(ISBN) AS amount_of_reviews  FROM `BX-Book-Ratings` GROUP BY user_id ORDER BY amount_of_reviews DESC LIMIT 15"
    try:
        cursor.execute(select_users_sql)
        users = []
        rows = cursor.fetchall()
        for row in rows:
            users.append(row[0])
        users = sorted(users)
    except db.Error as err:
        users = [276762, 276925, 113334, 269841, 139835]
    return users