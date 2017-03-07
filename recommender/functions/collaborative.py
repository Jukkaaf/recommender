import MySQLdb as mysli
import numpy as np

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


    coefficients = {}
    for other_user in dictionary:
        coefficient = coef_similarity(rewiews_by_user,dictionary[other_user])
        #print dictionary[other_user]
        coefficients[other_user] = coefficient

    coefficients = sorted(coefficients.items(), key=lambda x :x[1])
    #Taking the highest rated book a the most similar user
    #Todo, returning a few books
    highest_rated_isbn = None
    most_similar_user = coefficients[:1][0][0]
    #print most_similar_user
    for ISBN in dictionary[most_similar_user]:
        rating = dictionary[most_similar_user][ISBN]
        #Checking it is not the same book
        if rating > highest_rated_isbn and ISBN != isbn:
            highest_rated_isbn = ISBN


    return highest_rated_isbn



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


def coef_similarity(a_reviews,b_reviews):

    reviews_a = []
    reviews_b = []
    common = 0
    for item_a in a_reviews:
        for item_b in b_reviews:
            if item_a == item_b:
                common += 1
                reviews_a.append(int(a_reviews[item_a]))
                reviews_b.append(int(b_reviews[item_b]))
    #print reviews_a
    #print reviews_b
    corr = np.corrcoef(reviews_a,reviews_b)
    #print corr
    return corr[1,0]
    """mean_a = (sum(a_reviews.values()))/(len(a_reviews))
    mean_b = (sum(b_reviews.values()))/(len(b_reviews))
    covariance = 0
    pow_sum_a = 0
    pow_sum_b = 0
    for item_a in a_reviews:
        for item_b in b_reviews:
            if item_a == item_b:
                rating_a = a_reviews[item_a]
                rating_b = b_reviews[item_a]
                covariance += (rating_a-mean_a)*(rating_b-mean_b)
                pow_sum_a += (rating_a-mean_a)**2
                pow_sum_b += (rating_b - mean_b) ** 2
    if pow_sum_a == 0  or pow_sum_b == 0:
        return 0
    return covariance/ ( sqrt(pow_sum_a) * sqrt(pow_sum_b) )"""
