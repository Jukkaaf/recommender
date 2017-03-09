import MySQLdb as mysli
from random import randint

def coldturkey(db):
    cursor = db.cursor()
    arv_sql = "SELECT `ISBN` FROM `BX-Book-Ratings` WHERE `Book-Rating`='10'"
    try:
        cursor.execute(arv_sql)
        books = cursor.fetchall()
    except mysli.Error as err:
        print err

    counter =  {}

    for book in books:
        if book[0] in counter:
            counter[book[0]] += 1
        else:
            counter[book[0]] = 1

    ordcounter = sorted(counter, key=counter.get, reverse=True)
    split = int(len(ordcounter) * 0.1)

    top = ordcounter[:split]

    return top[randint(0,split-1)]