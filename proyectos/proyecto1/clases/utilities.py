import sqlite3


class utilities(object):
    _nombres = []

    def __init__(self):
        con = sqlite3.connect("elpobladoDb.db")
        cur = con.cursor()  # con cursor, podemos ejecutar todas la concultas a la base de datos
        cur.execute('SELECT name FROM PRAGMA_TABLE_INFO("clientes");')
        nombres = cur.fetchall()
        self._nombres = []
        for nombre in nombres:
            self._nombres.append(nombre[0])

        print(self._nombres)

    def json2table(self):
        pass
