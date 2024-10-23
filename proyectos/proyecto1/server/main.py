"""
    para comenzar a correr en el localhost, usamos el siguiente comando
        uvicorn main:app --port 5300 --reload

        Es importante saber que esta pequeña app, nos va a ayudar a trabajar con todo el tema que se necesita para organizar la compraventa
        comenzamos con el back, trabajando todo desde la consola, y por último hacemos todo el front. Cuando terminemos, le diremos a mi papá,
        para que pueda usarlo y comprobar que todo esté funcionando correctamente.

    BASE DE DATOS
    Siempre comprometer la consulta SQL con la propiedad de la conexión conn.commit()
    Para leer información:
        - leer un dato, comprometemos con cursor.fetchone()
        - leer todos lo datos, comprometemos con cursor.fetchall()


"""
# ----- Compraventa el poblado --------
from fastapi import FastAPI, Body  # type: ignore
import requests as req  # type: ignore
import sqlite3
import os.path as path
from pydantic import BaseModel  # type: ignore
import mysql.connector  # type: ignore

app = FastAPI()
app.title = 'Compraventa el Poblado'

""" MODELOS: estos modelos nos ayudan a volver objetos lo que llega en una petición POST"""


class Cliente(BaseModel):
    name: str
    surname: str
    document: str
    email: str


class Contrato(BaseModel):
    customer_id: int
    contrato: int
    fecha: str
    valor: int
    adicional: int
    abono: int
    renovaciones: int
    articulo: str


""" FIN MODELOS """


"""
    UTILIDADES -> funciones adicionales
"""


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


""" CUSTOMERS """


@app.get('/get_customers', tags=['customers'])
def get_customers():
    """ cargamos la información de los clientes"""

    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="Maria123.",
            database='CVP_DB')

        cur = conn.cursor()
        cur.execute("SELECT * FROM customers_")
        customers = cur.fetchall()
        conn.close()

        return {
            'info': db2json(customers, cur.column_names),
            'column_names': cur.column_names
        }
    except:
        return -1


@app.get('/get_customer_by_id/{id}', tags=['customers'])
def get_customer_by_id(id: int):
    """ Buscamos un cliente por id """
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="Maria123.",
            database='CVP_DB')

        cur = conn.cursor()  # con cursor, podemos ejecutar todas la concultas a la base de datos
        cur.execute(f"SELECT * FROM customers_ where id = %i" % (id))
        cliente = cur.fetchone()
        conn.close()

        return {
            'info': db2json_one(cliente, cur.column_names),
            'column_names': cur.column_names
        }
    except:
        return -1


@app.get('/get_customer_by_document/{document}', tags=['customers'])
def get_customer_by_document(document: str):
    """ Buscamos un cliente por documento """
    # print(documento)
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="Maria123.",
            database='CVP_DB')

        cur = conn.cursor()
        cur.execute(
            f'SELECT * FROM customers_ where document = "%s"' % (document))
        customer = cur.fetchone()
        conn.close()
        return {
            'info': db2json_one(customer, cur.column_names),
            'column_names': cur.column_names
        }
    except:
        return -1


@ app.post('/add_customer', tags=['customers'])
def add_customer(customer: Cliente):
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="Maria123.",
            database='CVP_DB')
        cur = conn.cursor()
        values = (customer.name, customer.surname,
                  customer.document, customer.email)
        cur.execute(
            f'INSERT INTO customers_ (name, surname, document, email) VALUES ("%s","%s","%s","%s")' % values)
        conn.commit()
        conn.close()
        return {
            "mensaje": "Se ha añadido correctamente"
        }
    except:
        return {
            "mensaje": "No se añadido correctamente, intenta más tarde"
        }


""" CONTRATOS """


@ app.post('/add_contract', tags=['contracts'])
def add_contract(contract: Contrato):

    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="Maria123.",
            database='CVP_DB')

        cur = conn.cursor()
        total = contract.valor + contract.adicional - contract.abono
        values = (contract.contract, contract.fecha, contract.valor, contract.adicional,
                  contract.abono, total, contract.renovaciones, contract.articulo, contract.customer_id)
        cur.execute('INSERT INTO contracts (contract,date,value,additional,payment,total, renewal,article, customer_id) VALUES (%i,"%s",%i,%i,%i,%i,%i,"%s",%i)' % values)
        conn.commit()
        conn.close()

        return {
            "mensaje": "Se ha añadido correctamente"
        }
    except:
        return {
            "mensaje": "No se añadido correctamente, intenta más tarde"
        }


@ app.get('/get_contracts', tags=['contracts'])
def get_contracts():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="Maria123.",
        database='CVP_DB')

    cur = conn.cursor()
    cur.execute('SELECT * FROM contracts')
    contracts = cur.fetchall()
    conn.close()
    return {
        'info': db2json(contracts, cur.column_names),
        'column_names': cur.column_names
    }


@ app.get('/get_contract_by_contract/{_contract}', tags=['contracts'])
def get_contracts(_contract: int):
    conn = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="Maria123.",
        database='CVP_DB')

    cur = conn.cursor()
    cur.execute('SELECT * FROM contracts WHERE contract = %i' % (_contract))
    contract = cur.fetchone()
    conn.close()
    return {
        'info': db2json_one(contract, cur.column_names),
        'column_names': cur.column_names
    }


@ app.get('/get_contracts_by_customer_id/{customer_id}', tags=['contracts'])
def get_contracts(customer_id: int):
    conn = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="Maria123.",
        database='CVP_DB')

    cur = conn.cursor()
    cur.execute('SELECT * FROM contracts WHERE customer_id = %i' %
                (customer_id))
    contracts = cur.fetchall()
    conn.close()
    return {
        'info': db2json(contracts, cur.column_names),
        'column_names': cur.column_names
    }


""" UTILIDADES """


@app.get('/fecha_actual', tags=['utilidades'])
def home():
    url = "http://worldtimeapi.org/api/timezone/America/Bogota"
    data = req.get(url)
    reponse_json = data.json()
    return reponse_json['datetime']


@app.get('/get_contracts_names', tags=['utilidades'])
def get_contracts_names():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="Maria123.",
        database='CVP_DB')

    cur = conn.cursor()
    cur.execute('SELECT * FROM contracts')
    conn.close()
    return cur.column_names
