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

