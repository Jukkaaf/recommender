import MySQLdb as mysli
import numpy as np
from collections import OrderedDict


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
    for row in ratings_of_the_book:
        other_user = row[0]
        other_rating = row[2]
        other_users_that_have_rated[other_user] = other_rating


    rewiews_by_user_sql = "SELECT * FROM `BX-Book-Ratings` WHERE `User-ID`=%s" % userid
    rewiews_by_user = {}
    try:
        cursor.execute(rewiews_by_user_sql)
        rewiews_by_user_tuple = cursor.fetchall()
        for row in rewiews_by_user_tuple:
            book_isbn2 = row[1]
            rating2 = row[2]
            rewiews_by_user[book_isbn2] = rating2
    except mysli.Error as err:
        print err



    dictionary = dict()
    #Adding current user to matrix

    largest_nmbr_of_reviews = 0
    for other_user in other_users_that_have_rated:
        reviews_by_other_sql = "SELECT * FROM `BX-Book-Ratings` WHERE `User-ID`=%s" % other_user
        try:
            cursor.execute(reviews_by_other_sql)
            reviews_by_the_other = cursor.fetchall()
            if other_user not in dictionary:
                dictionary[other_user] = {}
            amount_of_reviews = len(reviews_by_the_other)
            if  amount_of_reviews > largest_nmbr_of_reviews:
                largest_nmbr_of_reviews = amount_of_reviews
            for review in reviews_by_the_other:
                    book_isbn = review[1]
                    rating = review[2]
                    dictionary[other_user][book_isbn]= rating
        except mysli.Error as err:
            print err


    coefficients = OrderedDict()
    for other_user in dictionary:
        coefficient = coef_similarity(rewiews_by_user,dictionary[other_user])
        #print coefficient
        #print dictionary[other_user]
        coefficients[other_user] = coefficient

    coefficients = sorted(coefficients.items(), key=lambda x :x[1], reverse=True)

    #Taking the highest rated book a the most similar user
    highest_rated_isbns = OrderedDict()
    number_of_similar_users = len(coefficients)
    #Number of reviews that must be done will be
    limit_of_books = 50
    number_of_books = 0

    #Palauta orderedDict, avain ISBN, arvo paino

    if len(coefficients) > 0:
        for similar_user,coeff in coefficients:
            # going at most half of the similar users
            half_of_users = number_of_similar_users/2
            if number_of_books <= limit_of_books and similar_user in dictionary:
                for ISBN in dictionary[similar_user]:
                    #print ISBN
                    rating = dictionary[similar_user][ISBN]
                    #Checking it is not the same book
                    if rating >= 5 and ISBN != isbn:
                        highest_rated_isbns[ISBN] = coeff #* coefficient

    return highest_rated_isbns



def bookInfo(isbn, db):
    cursor = db.cursor()
    arv_sql = "SELECT * FROM `BX-Books` WHERE `ISBN`='%s'" % (isbn)
    info = {}
    try:
        cursor.execute(arv_sql)
        book = cursor.fetchall()
        for row in book:
            info['Book-Title'] = row[1]
            info['Book-Author'] = row[2]
            info['Year-Of-Publication'] = row[3]
            info['Publisher'] = row[4]
            info['Image-URL-M'] = row[6]
    except mysli.Error as err:
        print err



    return info


def coef_similarity(a_reviews,b_reviews):

    # Two different users, A and B, have graded the same books,
    # the grades will be put in the same order in both lists
    # same_reviews_a = [grade_for_book1, grade_for_book2 ... ]
    # same_reviews_b = [grade_for_book1, grade_for_book2 ... ]

    same_reviews_a = []
    same_reviews_b = []
    number_of_common_reviews = 0
    for item in a_reviews:
        if item in b_reviews:
            number_of_common_reviews += 1
            same_reviews_a.append(int(a_reviews[item]))
            same_reviews_b.append(int(b_reviews[item]))
    #print same_reviews_a
    #print same_reviews_b
    if number_of_common_reviews > 1:
        # For more than one common review, the correlation is
        # calculated with corrcoef-function of numpy
        correlation = np.corrcoef(same_reviews_a,same_reviews_b)[1,0]
    elif number_of_common_reviews == 1:
        # If there is just one common review, then the corrcoef-function cannot produce result
        # and it is the difference between grades divided by 10
        correlation = 1.0 - ( abs(float(same_reviews_a[0] - same_reviews_b[0]))/10 )
    else:
        correlation = 0.0
    #print correlation
    return correlation

#UUSI FUNKTIO
def collaborativeFiltering_new(userid, isbn, db):
    cursor = db.cursor()

    print userid

    #All reviews done by the user
    #rewiews_by_user_sql = "SELECT * FROM `BX-Book-Ratings` WHERE `User-ID`=%s" % userid
    rewiews_by_user = {}
    try:
        cursor.execute("SELECT * FROM `BX-Book-Ratings` WHERE `User-ID`=%s", (userid,))
        rewiews_by_user_tuple = cursor.fetchall()
        for row in rewiews_by_user_tuple:
            book_isbn2 = row[1]
            rating2 = row[2]
            rewiews_by_user[book_isbn2] = rating2
    except mysli.Error as err:
        print err

    #Finding other users who have rated same books
    dictionary = dict()


    #Union of users that have rated the same books and users that have rated the selected book
    #reviews_by_others_sql = "SELECT * FROM `BX-Book-Ratings` WHERE `ISBN` IN( SELECT `ISBN` FROM `BX-Book-Ratings` WHERE `User-ID`=%s) UNION SELECT * FROM `BX-Book-Ratings` WHERE `ISBN`='%s'" % (userid,isbn)

    try:
        cursor.execute("SELECT * FROM `BX-Book-Ratings` WHERE `ISBN` IN( SELECT `ISBN` FROM `BX-Book-Ratings` WHERE `User-ID`=%s) UNION SELECT * FROM `BX-Book-Ratings` WHERE `ISBN`=%s", (userid,isbn))
        reviews_by_others = cursor.fetchall()
        for review in reviews_by_others:
            other_user = int(review[0])
            if other_user not in dictionary:
                dictionary[other_user] = {}
            book_isbn = review[1]
            rating = review[2]
            dictionary[other_user][book_isbn]= rating
    except mysli.Error as err:
        print err

    coefficients = OrderedDict()
    for other_user in dictionary:
        coefficient = coef_similarity(rewiews_by_user,dictionary[other_user])
        #print coefficient
        coefficients[other_user] = coefficient

    #Coefficienttien lajittelu suuruusjarjestykseen
    coefficients = OrderedDict(sorted(coefficients.items(),key=lambda x:x[1],reverse=True))

    #print coefficients
    highest_rated_isbns = OrderedDict()
    number_of_books = 0
    limit_of_books = 50
    if len(coefficients) > 1:
        for similar_user,coeff in coefficients.items():
            #print similar_user
            if number_of_books <= limit_of_books and similar_user in dictionary.keys():
                for ISBN in dictionary[similar_user]:
                    #print ISBN
                    rating = dictionary[similar_user][ISBN]
                    #Checking it is not the same book
                    if rating >= 0 and ISBN != isbn:
                        number_of_books += 1
                        #The point for the book is the coefficient multiplied by the rating of the book
                        highest_rated_isbns[ISBN] = coeff*rating #coefficient * rating
                        # nan arvot nollaksi
                        if np.isnan(highest_rated_isbns[ISBN]):
                            highest_rated_isbns[ISBN] = float(0)

    highest_rated_isbns = OrderedDict(sorted(highest_rated_isbns.items(),key=lambda x:x[1],reverse=True))
    #print highest_rated_isbns
    return highest_rated_isbns