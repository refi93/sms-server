import sqlite3
import atexit
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


conn = sqlite3.connect('database.db')
engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)
session = Session()


def execute_raw(raw_sql):
    return conn.executescript(raw_sql)


def select(table):
    return sqlalchemy.select([table])


def query(table):
    return session.query(table)


def insert(table):
    return sqlalchemy.insert(table)


def update(table):
    return sqlalchemy.update(table)


def close_database():
    conn.close()
    engine.dispose()


atexit.register(close_database)