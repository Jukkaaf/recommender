import MySQLdb as mdb
import sys

def testfunction():
    text = ""
    try:
        con = mdb.connect('host', 'user', 'password', 'database');
        #con = mdb.connect("localhost", "root", "", "recommender")

        cur = con.cursor()
        cur.execute("SELECT VERSION()")

        ver = cur.fetchone()

        text = "Database version : %s " % ver

    except mdb.Error, e:

        text = "Error %d: %s" % (e.args[0], e.args[1])

    finally:
        if con:
            con.close()
    return(text)