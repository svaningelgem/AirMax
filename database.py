import sqlite3
from config import Config
import logging


class Cursor:
    def __init__(self, db):
        if isinstance(db, Database):
            self.db = db.db
        elif isinstance(db, sqlite3.Connection):
            self.db = db
        else:
            raise ValueError("Invalid database passed!")

    def __enter__(self):
        self.cursor = self.db.cursor()
        self.cursor.execute("begin")
        return self.cursor

    def __exit__(self, *exc):
        if exc[0]:
            self.cursor.execute("rollback")
        else:
            self.cursor.execute("commit")
        self.cursor.close()

        return not bool(exc[0])  # propagates exceptions

    def execute(self, *args, **kwargs):
        return self.cursor.execute(*args, **kwargs)


class Database:
    def __init__(self):
        self.db = sqlite3.connect(Config.cache_dir + '/database.sqlite3')
        self.db.isolation_level = None
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS air_quality(
                date DATETIME,
                latitude DECIMAL,
                longitude DECIMAL,
                country CHAR(2),
                city VARCHAR(200),
                location CHAR(7),
                value FLOAT,
                unit CHAR(10),
                parameter VARCHAR(200),
                sourceType VARCHAR(200),
                sourceName VARCHAR(200),
                PRIMARY KEY(date, latitude, longitude, parameter)
            )""")

    def __del__(self):
        if self.db and isinstance(self.db, sqlite3.Connection):
            self.db.close()

    def cleanup(self):
        with Cursor(self.db) as c:
            c.execute("DELETE FROM air_quality WHERE date < DATETIME('now') - 3*60*60")

    def add_measurement(self, date, latitude, longitude, country, city, location, value, unit, parameter, sourceType, sourceName):
        data = (date, latitude, longitude, country, city, location, value, unit, parameter, sourceType, sourceName)
        print(">> Adding ", data)

        with Cursor(self.db) as c:
            c.execute(  # I use REPLACE because I think later data could provide corrections on earlier received information
                "REPLACE INTO air_quality(date, latitude, longitude, country, city, location, value, unit, parameter, sourceType, sourceName) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                data
            )
