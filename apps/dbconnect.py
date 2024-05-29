import psycopg2
import pandas as pd
import os

class dbcreds:
    local = dict(
        host = 'localhost',
        database = 'lamrag-database',
        user = 'postgres',
        port = 5433,
        password = 'password'
    )
    #heroku = dict(
    #    DATABASE_URL = os.environ['database']
    #)

def getdblocation():
    #local = True
    local = False
    if local:
        # Define connection details
        creds = dbcreds.local
        db = psycopg2.connect(
            host = creds['host'],
            database = creds['database'],
            user = creds['user'],
            port = creds['port'],
            password = creds['password']
        )
    else:
        DATABASE_URL = os.environ['DATABASE_URL']
        db = psycopg2.connect(DATABASE_URL, sslmode = 'require')
    # return connection details
    return db

def modifydatabase(sql, values):
    db = getdblocation()
    cursor = db.cursor()
    cursor.execute(sql, values)
    db.commit()
    db.close()

def querydatafromdatabase(sql, values, dfcolumns):
    db = getdblocation()
    cursor = db.cursor()
    cursor.execute(sql, values)
    rows = pd.DataFrame(cursor.fetchall(), columns = dfcolumns)
    db.close()
    return rows