import dotenv
import os
import mysql.connector

# variables de entorno
dotenv.load_dotenv()
API_KEY = os.getenv("API_KEY")
HOST_DB = os.getenv("HOST_DB")
PORT_DB = os.getenv("PORT_DB")
USER_DB = os.getenv("USER_DB")
PASSWORD_DB = os.getenv("PASSWORD_DB")
DB = os.getenv("DB")


def db2json_one(object_db, column_names):
    data = {}
    for i in range(len(column_names)):
        data[f'{column_names[i]}'] = object_db[i]
    return data


def db2json(objects_db, column_names):
    data_array = []
    data = {}
    for object_db in objects_db:
        for i in range(len(column_names)):
            data[f'{column_names[i]}'] = object_db[i]
        data_array.append(data)
        data = {}
    return data_array


def db_conn():
    conn = mysql.connector.connect(
        host=HOST_DB,
        port=PORT_DB,
        user=USER_DB,
        password=PASSWORD_DB,
        database=DB
    )
    cur = conn.cursor()
    return conn, cur
