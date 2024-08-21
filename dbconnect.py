import psycopg2 as psql

def query(db_name='postgres',db_user='postgres',db_password='1',queries=['SELECT * FROM raw.game;']):
    try:
        #connects to and adds controller to database
        db = psql.connect(dbname=db_name, user=db_user, password=db_password)
        ctrl = db.cursor()

        #print all from game
        for query in queries:
            ctrl.execute(query)
            print(ctrl.fetchall())

        #close comms
        ctrl.close()
        db.close()
        return 0
    except:
        return 1

if __name__ == '__main__':
    #gets database info (defaults in brackets)
    db_name = input('DB Name (postgres): ')
    db_user = input('User (postgres): ')
    db_password = input('Password (1): ')
    print(query())

