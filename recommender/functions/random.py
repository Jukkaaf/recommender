import random
import MySQLdb as mysli

def random_user():
    db = mysli.connect("localhost","root","","recommender")
    kannassa = False
    while not kannassa:
        #Slee
        id = random.randint(1,278858)
        #Tarkistetaan, onko tietokannassa
