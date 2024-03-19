import psycopg2
import pandas as pd

def getdblocation():
    # Define connection details
    db = psycopg2.connect(
        host = 'localhost',
        database = 'LaMRAG-database',
        user = 'postgres',
        port = 5432,
        password = 'password'
    )
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