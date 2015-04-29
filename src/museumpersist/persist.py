import psycopg2

'''
Class for persisting built museums into Postgres database.
'''
class Persist:
    '''
    Create the object with the given database and user. This constructor doesn't actually 
    create the connnection. You need to call start() to create the connection (and finish() will
    end the connection).
    '''
    def __init__(self, dbname, user):
        self.dbname = dbname
        self.user = user
        self.conn = None
        self.cursor = None
    '''
    Connect to the databse.
    '''
    def start(self):
        self.conn = psycopg2.connect("dbname=%s user=%s" % (self.dbname, self.user))
        self.cursor = self.conn.cursor()
    '''
    Create the table. If it already exists, it will be deleted and recreated.
    '''
    def create_tables(self):
        self.cursor.execute("DROP TABLE IF EXISTS museums;")
        self.cursor.execute("CREATE TABLE museums (year int, month int, day int, museum text, primary key(year, month, day));")
        self.conn.commit()

    '''
    Get the museum for the given year, month, and day. If the museum exists, its json string 
    will be returned. Otherwise, None will be returned.
    '''
    def get_museum(self, year, month, day):
        self.cursor.execute("SELECT museum FROM museums WHERE year=%s AND month=%s AND day=%s"
                % (year, month, day))
        self.conn.commit()
        tuples = self.cursor.fetchall()
        if len(tuples) == 0:
            return None
        return tuples[0][0]

    '''
    Store the given museum (string) for the given year, month, and day. If the museum
    already exists, it will be deleted.
    '''
    def persist_museum(self, year, month, day, museum):
        museum = museum.replace("'", "")
        self.cursor.execute("DELETE FROM museums WHERE year=%s AND month=%s AND day=%s;"
                % (year, month, day)) 
        self.cursor.execute("INSERT INTO museums (year, month, day, museum) VALUES (%s, %s, %s, '%s');"
                % (year, month, day, museum))
        self.conn.commit()

    '''
    Close the connection to the database.
    '''
    def finish(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
