import PySimpleGUI as sg
import requests
import sqlite3

import mysql.connector

conn = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="Maria123.")

cur = conn.cursor()
cur.execute('use CVP_DB')
cur.execute('select * from contracts')
names = cur.column_names


conn.close()
sg.theme('DarkAmber')

# Funciones auxiliares


def db_conn(db_name):
    conn = mysql.connector.connect(
        host="localhost", user="root", passwd="Maria123.")
    cur = conn.cursor()
    cur.execute(f'use {db_name}')


def query_one(conn, query):
    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchone()


def query_all(conn, query):
    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()


def json2table(data):
    data_arrow = []
    data_array = []
    for dat in data:
        for name in names:  # función json2table
            customer_data.append(customer[f'{_nombre}'])
        customers_array.append(customer_data)
        customer_data = []
    return customers_array

# ventada mostrar información cliente encontrados


def customer_info_window(customer):
    layout = [[sg.Text(text='Información Cliente',
                       font=('Arial Bold', 20),
                       size=20,
                       expand_x=True,
                       justification='center')],
              [sg.Text('Id\t'), sg.Input(f'{customer['id']}',
                                         key='-input_documento-', disabled=True,
                                         text_color='white')],
              [sg.Text('Nombre\t'), sg.Input(f'{customer['nombre']}',
                                             key='-input_documento-', disabled=True, text_color='white')],
              [sg.Text('Cédula\t'), sg.Input(f'{customer['documento']}',
                                             key='-input_documento-', disabled=True, text_color='white')],
              [sg.Text('Correo\t'), sg.Input(f'{customer['correo']}',
                                             key='-input_documento-', disabled=True, text_color='white')],
              [sg.Text('Teléfono\t'), sg.Input(f'{customer['telefono']}',
                                               key='-input_documento-', disabled=True, text_color='white')],
              [sg.Button('Salir\t', key='-salir-')]
              ]

    window = sg.Window('HelloWorld', layout)

    while True:
        event, values = window.read()

        if event == '-salir-':
            break

    window.close()


# ----------------------------- Main Window ------------------------------------

column_customer_info = [[sg.Text(text='Información Cliente',
                                 font=('Arial Bold', 15),
                                 size=20,
                                 expand_x=True,
                                 justification='center')],
                        [sg.Text('Id\t'), sg.Input(
                            key='-input_id-', disabled=True, text_color='white')],
                        [sg.Text('Nombre\t'), sg.Input(key=f'-input_nombre-',
                                                       disabled=True, text_color='white')],
                        [sg.Text('Cédula\t'), sg.Input(key='-input_documento_info-',
                                                       disabled=True, text_color='white')],
                        [sg.Text('Correo\t'), sg.Input(key='-input_correo-',
                                                       disabled=True, text_color='white')],
                        [sg.Text('Teléfono\t'), sg.Input(
                            key='-input_telefono-', disabled=True, text_color='white')],
                        [sg.Text(text='Contratos',
                                 font=('Arial Bold', 10),
                                 size=20,
                                 expand_x=True,
                                 justification='center')],
                        [sg.Button(
                            'Mostrar', key='-contratos_mostrar-', visible=False), sg.Button(
                            'Añadir', key='-contratos_anadir-', visible=False), sg.Button(
                            'Modificar', key='-contratos_modificar-')]

                        ]

column_buscar_info = [
    [sg.Text(text='Busqueda de información',
             font=('Arial Bold', 15),
             size=20,
             expand_x=True,
             justification='center')],
    [sg.Text('Documento')],
    [sg.Input(key='-input_documento-'),
     sg.Button('Buscar', key='-buscar_documento-')],
    [sg.Text('Contrato')],
    [sg.Input(key='-input_contrato-'),
     sg.Button('Buscar', key='-buscar_contrato-')],
]

layout = [[sg.Text(text='CVP',
                   font=('Arial Bold', 15),
                   size=20,
                   expand_x=True,
                   justification='center')],
          [sg.Column(column_buscar_info), sg.VerticalSeparator(),
           sg.Column(column_customer_info)],
          [sg.Button('Lista clientes', key='-mostrar-'),
           sg.Button('Mostrar info cliente', key='-seleccionar-')],
          [sg.Table(values=[], headings=names,
                    key='-tabla-', text_color='White', justification='left', expand_x=True)],

          [sg.Button('Salir', key='-salir-')]
          ]

window = sg.Window('cvp_app', layout, finalize=True)
window.Maximize()

while True:
    event, values = window.read()
    if event == '-buscar_documento-':
        input_documento = values['-input_documento-']
        print(input_documento)
        if input_documento == "":
            sg.popup('Ingresa un documento')
        else:
            url = f"http://127.0.0.1:8000/encontrar_cliente_documento/{
                input_documento}"
            data = requests.get(url)
            customer = data.json()

            if customer == -1:
                sg.popup('Usuario no encontrado, ingresa documento válido')
            else:
                window['-input_id-'].update(customer['id'])
                window['-input_nombre-'].update(customer['nombre'])
                window['-input_documento_info-'].update(customer['documento'])
                window['-input_correo-'].update(customer['correo'])
                window['-input_telefono-'].update(customer['telefono'])
                window['-contratos_documento-'].update(visible=True)

    if event == '-mostrar-':
        url = "http://127.0.0.1:8000/home_clientes"
        data = requests.get(url)
        contracts = data.json()

        # table_data = json2table(contracts)

        # window['-tabla-'].update(table_data)

    elif event == '-seleccionar-':
        id_tabla = values['-tabla-']
        if (id_tabla == []):
            sg.popup('Selecciona una opción en la tabla')
        else:
            url = f"http://127.0.0.1:8000/encontrar_cliente/{(id_tabla[0]+1)}"
            data = requests.get(url)
            customer = data.json()

            window['-input_id-'].update(customer['id'])
            window['-input_nombre-'].update(customer['nombre'])
            window['-input_documento_info-'].update(customer['documento'])
            window['-input_correo-'].update(customer['correo'])
            window['-input_telefono-'].update(customer['telefono'])
            window['-contratos_mostrar-'].update(visible=True)
            window['-contratos_anadir-'].update(visible=True)
            window['-contratos_modificar-'].update(visible=True)

    elif event == '-buscar_contratos_documento-':
        sg.popup('Estas intentando buscar contratos')
    elif event == '-salir-':
        break

window.close()
