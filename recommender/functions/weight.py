from collaborative import bookInfo, coef_similarity
import math
import operator
import MySQLdb as mysli

def publisherWeight(recommenderBooks, selectedBook):
    for book in recommenderBooks:
        if recommenderBooks[book]['Publisher'] == selectedBook['Publisher']:
            recommenderBooks[book]['Score'] = recommenderBooks[book]['Score'] * float(1.7)
    return recommenderBooks

def cosineSimilarity(a_reviews,b_reviews):
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
        product = dot_product(same_reviews_a, same_reviews_b)
        len1 = math.sqrt(dot_product(same_reviews_a, same_reviews_b))
        len2 = math.sqrt(dot_product(same_reviews_a, same_reviews_b))
        similarity = product / (len1 * len2)
    elif number_of_common_reviews == 1:
        similarity = 1.0 - (abs(float(same_reviews_a[0] - same_reviews_b[0])) / 10)
    else:
        similarity = 0.0
    print similarity
    return similarity

def dot_product(v1, v2):
    return sum(map(operator.mul, v1, v2))

def bookSimilarityWeight(recommenderBooks, selectedBook, db):
    cursor = db.cursor()

    # haetaan arvostelut valitulle kirjalle
    reviews_of_selected_sql = "SELECT * FROM `BX-Book-Ratings` WHERE `ISBN`='%s'" % selectedBook['ISBN']
    reviews_of_selected = {}
    try:
        cursor.execute(reviews_of_selected_sql)
        #cursor.execute("SELECT * FROM `BX-Book-Ratings` WHERE `ISBN`='%s'", (selectedBook['ISBN'],))
        reviews_of_selected_tuple = cursor.fetchall()
        for row in reviews_of_selected_tuple:
            rating2 = row[2]
            user_id2 = row[0]
            reviews_of_selected[user_id2] = rating2
    except mysli.Error as err:
        print err

    # haetaan arvostelut muille kirjoille ja lasketaan cosini similarity
    for book in recommenderBooks:
        reviews_sql = "SELECT * FROM `BX-Book-Ratings` WHERE `ISBN`='%s'" % recommenderBooks[book]['ISBN']
        reviews = {}
        try:
            cursor.execute(reviews_sql)
            #SQL injektion estava tapa
            #cursor.execute("SELECT * FROM `BX-Book-Ratings` WHERE `ISBN`='%s'" , (recommenderBooks[book]['ISBN'],))
            reviews_tuple = cursor.fetchall()
            for row in reviews_tuple:
                user_id2 = row[0]
                rating2 = row[2]
                reviews[user_id2] = rating2

            # lasketaan coef_similarity
            #coefficient = coef_similarity(reviews_of_selected, reviews)
            # Lasketaan cosini similarity
            cos_similarity = cosineSimilarity(reviews_of_selected, reviews)
            # kerrotaan pisteet tuloksella + 1
            recommenderBooks[book]['Score'] = recommenderBooks[book]['Score'] * float(cos_similarity + 1.0)
            #print recommenderBooks[book]['ISBN'], float(coefficient)
        except mysli.Error as err:
            print err


    return recommenderBooks