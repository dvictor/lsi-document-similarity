import MySQLdb

db_name = 'lsi_experiment'
db_user = 'username'
db_pass = 'password'

db = MySQLdb.connect('127.0.0.1', db_user, db_pass, db_name, charset='utf8')


def get_cursor():
    c = db.cursor()
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')
    return c
