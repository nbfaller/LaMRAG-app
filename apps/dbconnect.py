import psycopg2
import pandas as pd
import boto3
import os

endpoint = 'lamrag-database.cxikw2ss0mou.ap-southeast-1.rds.amazonaws.com'
port = 5432
user = 'postgres'
region = 'ap-southeast-1b'

#session = boto3.Session(profile_name = 'eb-cli')
#client = session.client('rds')
#token = client.generate_db_auth_token(
#    DBHostname = endpoint,
#    Port = port,
#    DBUsername = user,
#    Region = region
#)

class dbcreds:
    local = dict(
        host = 'localhost',
        database = 'lamrag-database',
        user = 'postgres',
        port = 5432,
        password = 'password'
    )
    #heroku = dict(
    #    DATABASE_URL = os.environ['database']
    #)
    
def getdblocation():
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