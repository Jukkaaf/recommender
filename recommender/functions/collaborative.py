import MySQLdb as mysli

def collaborativeFiltering(userid, isbn):

    #Yhteys tietokantaan, localhost, mulla kayttaja = root, salasana = "", tietokannan nimi = reommender
    #db = mysli.connect("localhost", "root", "", "recommender")
    db = mysli.connect('host', 'user', 'password', 'database')

    cursor = db.cursor()

    #Kaikki arvostelut kirjasta
    arv_sql = "SELECT * FROM `bx-book-ratings` WHERE `ISBN`=%s ORDER BY `Book-Rating` DESC" % isbn

    #Kayttaja, joka on antanut parhaan arvion kirjalle
    kirjat = []

    try:
        cursor.execute(arv_sql)
        arvostelut = cursor.fetchall()
        for arvostelu in arvostelut:
            while len(kirjat) < 1:
                tekija = arvostelu[0]
                #Haetaan tekijan tekemat arvostelue
                tek_sql = "SELECT * FROM `bx-book-ratings` WHERE `User-ID`=%d ORDER BY `Book-Rating` DESC" % (tekija)
                cursor.execute(tek_sql)
                tekijan_arvostelut = cursor.fetchall()
                cursor.execute("SELECT COUNT(*) FROM `bx-book-ratings` WHERE `User-ID`=%d" % (tekija))
                maara = cursor.fetchone()[0]
                if (maara > 0):
                    kirjat.append(tekijan_arvostelut[0][1])

    except mysli.Error as err:
        print err

    return kirjat

    """"Alkuperainen hahmotelma laskemiselle
    user_sql = "SELECT * FROM `bx-book-ratings` WHERE `User-ID`=%d" % userid
    #Arvostelujen maara
    maara_sql = "SELECT COUNT(`ISBN`) FROM `bx-book-ratings` WHERE `User-ID`=%d" % userid

    print "rolo"
    try:
        cursor.execute(user_sql)
        kayttajan_arvostelut = cursor.fetchall()

    except mysli.Error as err:
        print err



    for arvostelu in kayttajan_arvostelut:

        kirja = arvostelu[1]

        if kirja is not isbn:

            #Muiden ratingit kyseista kirjasta
            rat_sql = "SELECT * FROM `bx-book-ratings` WHERE `ISBN` =%d ORDER BY `Book-Rating` DESCENDING" % isbn

            similarity = 0

            try:
                cursor.execute(rat_sql)
                arvostelut_kirjasta = cursor.fetchone()

                for arvostelu in arvostelut_kirjasta:
                    toisen_arvosana = arvostelu[2]
                    #KESKEN


            except mysli.Error as err:
                print err"""
