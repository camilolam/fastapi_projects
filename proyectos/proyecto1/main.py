"""
    para comenzar a correr en el localhost, usamos el siguiente comando
        uvicorn main:app --port 5300 --reload

        Es importante saber que esta pequeña app, nos va a ayudar a trabajar con todo el tema que se necesita para organizar la compraventa
        comenzamos con el back, trabajando todo desde la consola, y por último hacemos todo el front. Cuando terminemos, le diremos a mi papá,
        para que pueda usarlo y comprobar que todo esté funcionando correctamente.

"""
# ----- Compraventa el poblado --------
from fastapi import FastAPI, Body  # type: ignore
import requests as req  # type: ignore
import sqlite3
import os.path as path
from pydantic import BaseModel

app = FastAPI()
app.title = 'Compraventa el Poblado'


class Cliente(BaseModel):
    nombre: str
    documento: str
    correo: str
    telefono: str


class Contrato(BaseModel):
    id_cliente: int
    fecha: str
    valor: int
    adicional: int
    abono: int
    renovaciones: int
    articulo: str

# creamos y guardamos la base de datos que vamos a usa
# con = sqlite3.connect("elpobladoDb.db")
# cur = con.cursor()  # con cursor, podemos ejecutar todas la concultas a la base de datos


"""
    para usar la base de datos, necesitamos saber algo

    si necesitmos ingredar datos a la base -> ejecutamos la consulta y usamos el comento commit
    Si leemos un dato -> ejecutamos la consulta y usamos el comando fetchone (para un solo dato ) o fetchall (para una lista de datos)
"""

# Funciones adicionales ----------

# función para crear lectura de una base de datos relacionales (sqlite,mysql), formato json (diccionaris en python)


def crear_json(cur, cliente):
    cur.execute('SELECT name FROM PRAGMA_TABLE_INFO("clientes");')
    nombres = cur.fetchall()
    data = {}
    for i in range(len(nombres)):
        data[f'{nombres[i][0]}'] = cliente[i]
    # print('Se ha convertido en json')
    return data

# fin funciones adicionales ------------


@app.get('/home_clientes', tags=['clientes'])
def home_clientes():
    """ cargamos la información de los clientes"""
    clientes_json = []
    con = sqlite3.connect("elpobladoDb.db")
    cur = con.cursor()  # con cursor, podemos ejecutar todas la concultas a la base de datos
    res = cur.execute("SELECT * FROM clientes")
    clientes = res.fetchall()
    # print(clientes)
    for cliente in clientes:
        clientes_json.append(
            crear_json(cur, cliente)
        )

    con.close()
    return clientes_json


@app.get('/encontrar_cliente/{id}', tags=['clientes'])
def encontrar_clientes(id: int):
    """ Buscamos un cliente por id """
    # print(id)
    try:
        con = sqlite3.connect("elpobladoDb.db")
        cur = con.cursor()  # con cursor, podemos ejecutar todas la concultas a la base de datos
        res = cur.execute(f"SELECT * FROM clientes where id = {id}")
        cliente = res.fetchone()

        respuesta = crear_json(cur, cliente)
        con.close()

        return respuesta
    except:
        return -1


@app.get('/encontrar_cliente_documento/{documento}', tags=['clientes'])
def encontrar_clientes_documento(documento: str):
    """ Buscamos un cliente por documento """
    # print(documento)
    try:
        con = sqlite3.connect("elpobladoDb.db")
        cur = con.cursor()  # con cursor, podemos ejecutar todas la concultas a la base de datos
        res = cur.execute(
            f'SELECT * FROM clientes where documento = "{documento}"')
        cliente = res.fetchone()

        respuesta = crear_json(cur, cliente)
        con.close()
        print('se ha completado el código')
        return respuesta
    except:
        print('problema en la ejecución del código')
        return -1


@app.post('/anadir_cliente', tags=['clientes'])
def anadir_cliente(cliente: Cliente):
    try:
        con = sqlite3.connect("elpobladoDb.db")
        cur = con.cursor()
        # cur.execute('SELECT name FROM PRAGMA_TABLE_INFO("clientes");')
        cur.execute(f'INSERT INTO clientes (nombre, documento, correo, telefono) VALUES ("{
                    cliente.nombre}","{cliente.documento}","{cliente.correo}","{cliente.telefono}")')
        con.commit()
        con.close()
        return {
            "mensaje": "Se ha añadido correctamente"
        }
    except:
        return {
            "mensaje": "No se añadido correctamente, intenta más tarde"
        }


@ app.get('/fecha_actual', tags=['utilidades'])
def home():
    url = "http://worldtimeapi.org/api/timezone/America/Bogota"
    data = req.get(url)
    reponse_json = data.json()
    return reponse_json['datetime']


# ¿Cual es la diferencia en fastApi entre el método get y el post?


@app.post('/anadir_contrato', tags=['contratos'])
def anadir_cliente(contrato: Contrato):
    try:
        con = sqlite3.connect("elpobladoDb.db")
        cur = con.cursor()
        # cur.execute('SELECT name FROM PRAGMA_TABLE_INFO("clientes");')
        total = contrato.valor + contrato.adicional - contrato.abono
        print(total)
        cur.execute(f'INSERT INTO contratos (id_cliente, fecha, valor, adicional,abono,total, renovaciones, articulo) VALUES ({contrato.id_cliente},"{
                    contrato.fecha}",{contrato.valor},{contrato.adicional},{contrato.abono},{total},{contrato.renovaciones},"{contrato.articulo}")')
        con.commit()
        con.close()
        return {
            "mensaje": "Se ha añadido correctamente"
        }
    except:
        return {
            "mensaje": "No se añadido correctamente, intenta más tarde"
        }
