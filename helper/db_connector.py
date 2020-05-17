import mysql.connector as mysql
from dotenv import load_dotenv
import os

class MySQL:
    def __init__(self):
        load_dotenv('.env')
        self.conn = mysql.connect(
            host=os.getenv('host'),
            user=os.getenv('username'),
            password=os.getenv('password'),
            database=os.getenv('database')
        )
        self.cur = self.conn.cursor(dictionary=True)
    
    def get_data(self, query):
        self.cur.execute(query)
        return self.cur.fetchall()

    def close(self):
        self.conn.close()
