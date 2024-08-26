import psycopg2 as psql
import psycopg2.extras as psqlx
from os import getenv as env
from dotenv import load_dotenv

load_dotenv()
log = open('log.txt','a')

class Database():
    """A class used to connect to and execute queries on psql databases"""
    def __init__(self) -> None:
        #gets database info (defaults in brackets)
        self.name = env('db_name')
        self.user = env('db_user')
        self.pwd = env('db_password')
        self.connect()
        
    def connect(self):
        """Connects to database using instance variables created in __init__"""
        try:
            #connects to and adds controller to database
            self.db = psql.connect(dbname=self.name, user=self.user, password=self.pwd)
            self.ctrl = self.db.cursor(cursor_factory=psqlx.RealDictCursor)
            self.query(["SAVEPOINT start;","ALTER SEQUENCE raw.game_id_seq RESTART WITH 11;","ALTER SEQUENCE raw.member_id_seq RESTART WITH 1001;","ALTER SEQUENCE raw.member_game_instance_id_seq RESTART WITH 5000;"])
        except BaseException as err:
            print(f'DB connection crash\nError: {err}\n--------------',file=log)
            raise Exception
        
    def query(self,queries=['SELECT * FROM raw.game;']):
        """Queries the database

        Parameters:
            queries - SQL queries passed as a list of strings
        Returns:
            The output of the queries as a list of lists of tuples
        """
        self.output = []
        for query in queries:
            self.ctrl.execute(query)
            if query.upper().startswith('SELECT'):
                self.output.append(self.ctrl.fetchall())
        return self.output
    
    def rollback(self):
        self.query(["ROLLBACK TO SAVEPOINT start;","ALTER SEQUENCE raw.game_id_seq RESTART WITH 11;","ALTER SEQUENCE raw.member_id_seq RESTART WITH 1001;","ALTER SEQUENCE raw.member_game_instance_id_seq RESTART WITH 5000;"])


    def close(self):
        """Close comms"""
        self.ctrl.close()
        self.db.close()
        return 0


if __name__ == '__main__':
    db = Database()
    print(db.query(["INSERT INTO raw.game (game_name) VALUES ('Test');","SELECT * FROM raw.game;"]))
    db.rollback()
    print(db.query(["SELECT * FROM raw.game;"]))

