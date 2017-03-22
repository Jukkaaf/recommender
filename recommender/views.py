from pyramid.view import view_config
from functions.test import testfunction
from functions.collaborative import collaborativeFiltering,collaborativeFiltering_new, bookInfo
from functions.randomi import random_book,pick_users
from functions.coldturkey import coldturkey
from functions.weight import publisherWeight, bookSimilarityWeight
from collections import OrderedDict
import MySQLdb as mysli

@view_config(route_name='home', renderer='templates/mytemplate.jinja2')
def my_view(request):
    return {'project': 'recommender'}

@view_config(route_name='test', renderer='templates/test.jinja2')
def test(request):
    result = testfunction()
    return {'test': 'testi teksti',
            'result': result
            }

@view_config(route_name='collab', renderer='templates/collab.jinja2')
def collab(request):
    settings = request.registry.settings
    db = mysli.connect(settings['mysql.host'], settings['mysql.user'], settings['mysql.password'], settings['mysql.database'])

    coldbook = coldturkey(db)
    coldbookinfo = bookInfo(coldbook, db)

    isbn = random_book(db)
    print isbn
    return {'action': request.matchdict.get('action'),
            'coldbookinfo': coldbookinfo
            }

#                                                                Muutettu collab.jinja -> collab2.jinja
@view_config(route_name='collab_action', match_param='action=filter', renderer='templates/collab2.jinja2')
def collab_filter(request):
    params = request.POST

    settings = request.registry.settings
    db = mysli.connect(settings['mysql.host'], settings['mysql.user'], settings['mysql.password'], settings['mysql.database'])

    #Alkuperainen
    #result = collaborativeFiltering(params["User-ID"].encode("utf-8"), params["ISBN"].encode("utf-8"), db)
    #Uusi
    result = collaborativeFiltering_new(params["User-ID"].encode("utf-8"), params["ISBN"].encode("utf-8"), db)

    selectedBook = bookInfo(params["ISBN"].encode("utf-8"), db)
    #temp isbn, vaihda result
    recommendedBook = bookInfo("0446310786", db)
    if len(result) > 0:
        recommendedBook = bookInfo(result.items()[0][0],db)

    #Kaikkien kirjojen palautus
    allRecommendedBooks = OrderedDict()
    for isbn in result:
        info = bookInfo(isbn,db)
        if info:
            try:
                info['Book-Title'] = info['Book-Title'].encode('utf-8')
                info['Score'] = result[isbn]
                allRecommendedBooks[isbn] = info
            except UnicodeDecodeError:
                print "error with " + str(isbn)
                pass
    try:
        # jos kayttaja haluaa painottaa kirjoja julkaisijan perusteella
        if params['pWeight']:
            allRecommendedBooks = publisherWeight(allRecommendedBooks, selectedBook)
        if params['sWeight']:
            allRecommendedBooks = bookSimilarityWeight(allRecommendedBooks, selectedBook)
        # jarjestetaan kirjat uudestaan painotuksien jalkeen
        allRecommendedBooks = OrderedDict(sorted(allRecommendedBooks.iteritems(), key=lambda x: x[1]['Score'], reverse=True))
        print allRecommendedBooks
    except:
        print "something went wrong"

    return {'params': params,
            'action': request.matchdict.get('action'),
            'selectedBook': selectedBook,
            'recommendedBook': recommendedBook,
            'allRecommendedBooks': allRecommendedBooks
            }
@view_config(route_name='select_book',renderer='templates/select_book.jinja2')
def select_book(request):
    parameters = request.POST



    settings = request.registry.settings
    db = mysli.connect(settings['mysql.host'], settings['mysql.user'], settings['mysql.password'],
                       settings['mysql.database'])
    return_all_books = True
    top_books_isbns = coldturkey(db,return_all_books)

    users = pick_users(db)

    top_books = {}
    for isbn in top_books_isbns:
        #Isbn 84.02.05006.9 aiheuttaa sql-virheen (1064, "You have an error in your...
        info = bookInfo(isbn,db)
        if info:
            try:
                #Jos kirjan nimessa on ei-ascii-merkkeja, tulostettaessa tulee error: UnicodeDecodeError: 'ascii' codec can't decode byte...
                #Tassa voi tulla UnicodeDecodeError ja kyseista kirjaa ei panna top_booksiin
                info['Book-Title'] = info['Book-Title'].encode('utf-8')
                top_books[isbn] = bookInfo(isbn, db)
                top_books[isbn]['Book-ISBN'] = isbn
            except UnicodeDecodeError:
                pass


    return{'action': request.matchdict.get('action'),
           'top_books': top_books,
           'users': users}