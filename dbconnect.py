import psycopg2 as psql

#gets database info (defaults in brackets)
db_name = input('DB Name (postgres): ')
if db_name == '': db_name = 'postgres'
db_user = input('User (postgres): ')
if db_user == '': db_user = 'postgres'
db_password = input('Password (1): ')
if db_password == '': db_password = '1'


#connects to and adds controller to database
db = psql.connect(dbname=db_name, user=db_user, password=db_password)
ctrl = db.cursor()

#print all from game
ctrl.execute('SELECT * FROM raw.game;')
print(ctrl.fetchall())

#close comms
ctrl.close()
db.close()
