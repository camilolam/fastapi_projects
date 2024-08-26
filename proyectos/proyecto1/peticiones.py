import PySimpleGUI as sg
import requests
import sqlite3


# url = "http://127.0.0.1:5300/home_clientes"
# data = requests.get(url)
# reponse_json = data.json()
# print(reponse_json)

print("Se ha iniciado el programa")

con = sqlite3.connect("elpobladoDb.db")
cur = con.cursor()  # con cursor, podemos ejecutar todas la concultas a la base de datos
cur.execute('SELECT name FROM PRAGMA_TABLE_INFO("clientes");')
nombres = cur.fetchall()
_nombres = []
for nombre in nombres:
    _nombres.append(nombre[0])
# print(_nombres)


def setText(Text):
    for line in Text:
        decodedText = line.decode("utf-8")
        window['-textbox-'].update(value=decodedText)


sg.theme('DarkAmber')
layout = [[sg.Text(text='Compraventa el Poblado',
                   font=('Arial Bold', 20),
                   size=20,
                   expand_x=True,
                   justification='center')],
          [sg.Input(), sg.Button('Buscar', key='-buscar-')],
          [sg.Button('Mostrar info', key='-mostrar-')],
          [sg.Multiline(size=(30, 5), key='-textbox-', autoscroll=False)],

          [sg.Button('Salir', key='-salir-')]
          ]

window = sg.Window('HelloWorld', layout)

while True:
    event, values = window.read()
    if event == '-mostrar-':
        url = "http://127.0.0.1:8000/home_clientes"
        data = requests.get(url)
        reponse_json = data.json()
        setText(data)
        print(reponse_json)
        window['-textbox-'].update(reponse_json)

    if event == '-salir-':
        break

window.close()
