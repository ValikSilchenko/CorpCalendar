import psycopg2
import datetime
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
        self.cursor.execute('''INSERT INTO events 
        (theme, place, time, beginning_date, ending_date, comment)
         VALUES (%s, %s, %s, %s, %s, %s);''', (theme, place, time, beginning_date, ending_date, comment))
        self.connection.commit()

    def get_dates_with_events(self) -> list:
        self.cursor.execute('''SELECT DISTINCT beginning_date FROM events;''')
        dates = list(map(lambda x: x[0].strftime("%Y-%m-%d"), self.cursor.fetchall()))
        # self.cursor.execute('''SELECT DISTINCT ending_date FROM events;''')
        # for date in list(map(lambda x: x[0].strftime("%Y-%m-%d"), self.cursor.fetchall())):
        #     dates.add(date)
        return dates

    def get_events_by_date(self, date: str):
        self.cursor.execute('''SELECT * FROM events WHERE beginning_date = %s;''', (date,))
        return self.cursor.fetchall()
