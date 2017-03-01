import MySQLdb as mysli
import pandas as pd
#from scipy.stats import pearsonr

def collaborativeFiltering(userid, isbn, db):

    cursor = db.cursor()

    #All ratings about the book
    arv_sql = "SELECT * FROM `BX-Book-Ratings` WHERE `ISBN`='%s' AND NOT `User-ID`=%s" % (isbn,userid)
    try:
        cursor.execute(arv_sql)
        ratings_of_the_book = cursor.fetchall()

    except mysli.Error as err:
        print err

    # Finding other users that have rated the book
    other_users_that_have_rated = {}
    print ratings_of_the_book
    for row in ratings_of_the_book:
        other_user = row[0]
        other_rating = row[2]
        other_users_that_have_rated[other_user] = other_rating


    rewiews_by_user_sql = "SELECT * FROM `BX-Book-Ratings` WHERE `User-ID`=%s" % userid
    try:
        cursor.execute(rewiews_by_user_sql)
        rewiews_by_user = cursor.fetchall()


    except mysli.Error as err:
        print err

    matrix = pd.DataFrame()

    for other_user in other_users_that_have_rated:
        reviews_by_other_sql = "SELECT * FROM `BX-Book-Ratings` WHERE `User-ID`=%s" % other_user
        try:
            cursor.execute(reviews_by_other_sql)
            reviews_by_the_other = cursor.fetchall()
            """Selecting the reviews of others users, that have rated at least one common book with the user
            for book_other in reviews_by_the_other[:2]:
                for book in rewiews_by_user[:2]:
                    if book_other is book is not  isbn:"""
            for review in reviews_by_the_other:
                    book_isbn = review[1]
                    rating = review[2]
                    """print review
                    print 'uli'
                    print rating"""
                    new_key = {book_isbn: rating}
                    matrix.loc[-1] = new_key

        except mysli.Error as err:
            print err


def bookInfo(isbn, db):
    cursor = db.cursor()
    arv_sql = "SELECT * FROM `BX-Books` WHERE `ISBN`='%s'" % (isbn)
    try:
        cursor.execute(arv_sql)
        book = cursor.fetchall()
    except mysli.Error as err:
        print err
    info = {}
    for row in book:
        info['Book-Title'] = row[1]
        info['Book-Author'] = row[2]
        info['Year-Of-Publication'] = row[3]
        info['Publisher'] = row[4]
        info['Image-URL-M'] = row[6]

    return info