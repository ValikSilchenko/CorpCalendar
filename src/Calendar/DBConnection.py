import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class DBConnection:
    def __init__(self):
        self.connection = psycopg2.connect(user="postgres",
                                           password="postgres",
                                           host="127.0.0.1",
                                           port="1946",
                                           database="events")
        self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cursor = self.connection.cursor()

    def __del__(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()

    def add_to_db(self, theme: str, place: str, time: str, beginning_date: str, ending_date: str, comment: str):
        self.cursor.execute("""INSERT INTO events 
        (theme, place, time, beginning_date, ending_date, comment)
         VALUES (%s, %s, %s, %s, %s, %s);""", (theme, place, time, beginning_date, ending_date, comment))
        self.connection.commit()

# cursor.execute('''create table if not exists events ();''')
