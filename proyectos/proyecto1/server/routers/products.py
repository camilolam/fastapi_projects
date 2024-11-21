from fastapi import APIRouter, HTTPException
from utilities import utilities, models

router = APIRouter()


@ router.post('/contract', status_code=201, tags=['contracts'])
async def add_contract(contract: models.Contract):
    conn, cur = utilities.db_conn()
    total = contract.value + contract.aditional - contract.payment
    values = (contract.date, contract.value, contract.aditional,
              contract.payment, total, contract.renewal, contract.article, contract.customer_id)
    cur.execute('INSERT INTO contracts (date,value,additional,payment,total, renewal,article, customer_id) VALUES ("%s",%i,%i,%i,%i,%i,"%s",%i)' % values)
    conn.commit()
    conn.close()

    return contract


@ router.get('/contracts', status_code=200, tags=['contracts'])
async def get_contracts():
    conn, cur = utilities.db_conn()
    cur.execute('SELECT * FROM contracts')
    contracts = cur.fetchall()
    conn.close()

    return utilities.db2json(contracts, cur.column_names),


@ router.get('/contract/{contract_id}', status_code=200, tags=['contracts'])
async def get_contract(contract_id: int):
    conn, cur = utilities.db_conn()
    cur.execute('SELECT * FROM contracts WHERE contract = %i' %
                (contract_id))
    contract = cur.fetchone()
    conn.close()
    if contract == None:
        raise HTTPException(
            status_code=404, detail="No se ha encontrado el contrato")
    else:
        return utilities.db2json_one(contract, cur.column_names),


@ router.get('/contracts/customer/{customer_id}', tags=['contracts'])
async def get_contracts_by_customer_id(customer_id: int):

    conn, cur = utilities.db_conn()
    cur.execute('SELECT * FROM contracts WHERE customer_id = %i' %
                (customer_id))
    contracts = cur.fetchall()
    conn.close()
    if contracts == []:
        raise HTTPException(
            status_code=404, content="No hay contratos asignados")
    else:
        return utilities.db2json(contracts, cur.column_names)
