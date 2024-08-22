import psycopg2 as psql
from os import getenv as env
from dotenv import load_dotenv

load_dotenv()

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
            self.ctrl = self.db.cursor()
        except:
            #Error code on connection
            return 1
        
    def query(self,queries=['SELECT * FROM raw.game;']):
        """Queries the database

        Parameters:
            queries - SQL queries passed as a list of strings
        Returns:
            The output of the queries as a list of lists of tuples
            1 - if there is any error
        """
        self.output = []
        try:
            for query in queries:
                self.ctrl.execute(query)
                self.output.append(self.ctrl.fetchall())
            return self.output
        except:
            return 2

    def close(self):
        """Close comms"""
        self.ctrl.close()
        self.db.close()
        return 0


if __name__ == '__main__':
    db = Database()
    print(db.query())

