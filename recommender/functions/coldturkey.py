import MySQLdb as mysli
from random import randint

def coldturkey(db,return_all_books = False):
    cursor = db.cursor()
    arv_sql = "SELECT `*` FROM `BX-Book-Ratings`"
    try:
        cursor.execute(arv_sql)
        books = cursor.fetchall()
    except mysli.Error as err:
        print err

    score = {}
    ammount = {}

    for book in books:
        if book[0] in ammount:
            ammount[book[1]] += 1
            score[book[1]] += int(book[2])
        else:
            ammount[book[1]] = 1
            score[book[1]] = int(book[2])
    points = {}
    for book in ammount:
        points[book] = score[book] / ammount[book]

    ordcounter = sorted(points, key=points.get, reverse=True)
    split = int(len(ordcounter) * 0.005)
    top = ordcounter[:split]

    if return_all_books:
        return top
    else:
        return top[randint(0,split-1)]