from collaborative import bookInfo, coef_similarity
import MySQLdb as mysli

def publisherWeight(recommenderBooks, selectedBook):
    for book in recommenderBooks:
        if recommenderBooks[book]['Publisher'] == selectedBook['Publisher']:
            recommenderBooks[book]['Score'] = recommenderBooks[book]['Score'] * float(1.7)
    return recommenderBooks

def bookSimilarityWeight(recommenderBooks, selectedBook, db):
    cursor = db.cursor()

    # haetaan arvostelut valitulle kirjalle
    reviews_of_selected_sql = "SELECT * FROM `BX-Book-Ratings` WHERE `ISBN`='%s'" % selectedBook['ISBN']
    reviews_of_selected = {}
    try:
        cursor.execute(reviews_of_selected_sql)
        reviews_of_selected_tuple = cursor.fetchall()
        for row in reviews_of_selected_tuple:
            book_isbn2 = row[1]
            rating2 = row[2]
            reviews_of_selected[book_isbn2] = rating2
    except mysli.Error as err:
        print err

    # haetaan arvostelut muille kirjoille ja lasketaan coef similarity
    for book in recommenderBooks:
        reviews_sql = "SELECT * FROM `BX-Book-Ratings` WHERE `ISBN`='%s'" % recommenderBooks[book]['ISBN']
        reviews = {}
        try:
            cursor.execute(reviews_sql)
            reviews_tuple = cursor.fetchall()
            for row in reviews_tuple:
                book_isbn2 = row[1]
                rating2 = row[2]
                reviews[book_isbn2] = rating2

            # lasketaan similarity
            coefficient = coef_similarity(reviews_of_selected, reviews)
            # kerrotaan pisteet tuloksella + 1
            recommenderBooks[book]['Score'] = recommenderBooks[book]['Score'] * float(coefficient + 1.0)
            #print recommenderBooks[book]['ISBN'], float(coefficient)
        except mysli.Error as err:
            print err


    return recommenderBooks