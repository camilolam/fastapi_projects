from fastapi import APIRouter, HTTPException
from utilities import utilities, models
from pydantic import BaseModel  # type: ignore

router = APIRouter()


@router.get('/users', status_code=200, tags=['users'])
async def users():
    """ cargamos la información de los clientes"""

    conn, cur = utilities.db_conn()
    cur.execute("SELECT * FROM customers_")
    users = cur.fetchall()
    conn.close()
    return utilities.db2json(users, cur.column_names)


@router.get('/user/{id}', status_code=200, tags=['users'])
async def customer(id: int):
    conn, cur = utilities.db_conn()
    cur.execute(f"SELECT * FROM customers_ where id = %i" % (id))
    customer = cur.fetchone()
    conn.close()
    if customer == None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    else:
        return utilities.db2json_one(customer, cur.column_names)


@router.get('/user/document/{document}', status_code=200, tags=['users'])
async def customer_doc(document: str):

    conn, cur = utilities.db_conn()
    cur.execute(
        f'SELECT * FROM customers_ where document = "%s"' % (document))
    customer = cur.fetchone()
    conn.close()
    if customer == None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    else:
        return utilities.db2json_one(customer, cur.column_names)


@ router.post('/user', status_code=201, tags=['users'])
async def add_customer(user: models.User):
    conn, cur = utilities.db_conn()
    cur.execute(
        f'SELECT id FROM customers_ WHERE document = "%s"' % (user.document))
    found = cur.fetchone()
    if found == None:
        values = (user.name, user.surname,
                  user.document, user.email)
        cur.execute(
            f'INSERT INTO customers_ (name, surname, document, email) VALUES ("%s","%s","%s","%s")' % values)
        conn.commit()
        conn.close()
        return user
    else:
        raise HTTPException(status_code=404, detail="Usuario ya existe")


@ router.delete('/user/{id}', status_code=200, tags=['users'])
async def delete_customer(id: int):
    conn, cur = utilities.db_conn()
    cur.execute(
        f'DELETE FROM customers_ WHERE id=%i' % (id))
    conn.commit()
    conn.close()

    return "Se ha eliminado el usuario"


@ router.put('/user/{id}', status_code=200, tags=['users'])
async def update_customer(user: models.User, id: int):
    conn, cur = utilities.db_conn()
    values = (user.name, user.surname,
              user.document, user.email, id)
    cur.execute(
        f'UPDATE customers_ SET name = "%s", surname="%s", document="%s", email = "%s" WHERE id = %i' % values)
    conn.commit()
    conn.close()
    return user
