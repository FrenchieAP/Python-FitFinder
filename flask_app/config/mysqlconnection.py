from dotenv import load_dotenv
import os
# a cursor is the object we use to interact with the database
import pymysql.cursors

load_dotenv()

DB_PASSWORD = os.environ.get("DB_PASSWORD")
print(f"DB PASSWORD: {DB_PASSWORD}")
HOST = os.environ.get("HOST")
# this class will give us an instance of a connection to our database
class MySQLConnection:
    def __init__(self, db):
        # change the user and password as needed
        self.connection = pymysql.connect(host=(f"{HOST}"),
                                    user="avnadmin", 
                                    password=(f"{DB_PASSWORD}"), 
                                    db = "defaultdb",
                                    port= 27829,
                                    charset = 'utf8mb4',
                                    cursorclass = pymysql.cursors.DictCursor,
                                    autocommit = True)
    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)

                cursor.execute(query, data)
                if query.lower().find("insert") >= 0:
                # INSERT queries will return the ID NUMBER of the row inserted
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                # SELECT queries will return the data from the database as a LIST OF DICTIONARIES
                    result = cursor.fetchall()
                    return result
                else:
                # UPDATE and DELETE queries will return nothing
                    self.connection.commit()
            except Exception as e:
            # if the query fails, the method will return FALSE
                print("*********Something went wrong*********", e)
                return False
            finally:
            # close the connection
                self.connection.close() 
# connectToMySQL receives the database we're using and uses it to create an instance of MySQLConnection
def connectToMySQL(db):
    return MySQLConnection(db)

