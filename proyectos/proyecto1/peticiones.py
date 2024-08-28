import PySimpleGUI as sg
import requests
import sqlite3

con = sqlite3.connect("elpobladoDb.db")
cur = con.cursor()  # con cursor, podemos ejecutar todas la concultas a la base de datos
cur.execute('SELECT name FROM PRAGMA_TABLE_INFO("clientes");')
nombres = cur.fetchall()
_nombres = []
_headings = []
for nombre in nombres:
    _nombres.append(nombre[0])
    _headings.append(f'{nombre[0]}           ')

sg.theme('DarkAmber')

# ventada mostrar información cliente encontrado


def customer_info_window(customer):
    layout = [[sg.Text(text='Información Cliente',
                       font=('Arial Bold', 20),
                       size=20,
                       expand_x=True,
                       justification='center')],
              [sg.Text('Id\t'), sg.Input(f'{customer['id']}',
                                         key='-input_documento-', disabled=True)],
              [sg.Text('Nombre\t'), sg.Input(f'{customer['nombre']}',
                                             key='-input_documento-', disabled=True)],
              [sg.Text('Cédula\t'), sg.Input(f'{customer['documento']}',
                                             key='-input_documento-', disabled=True)],
              [sg.Text('Correo\t'), sg.Input(f'{customer['correo']}',
                                             key='-input_documento-', disabled=True)],
              [sg.Text('Teléfono\t'), sg.Input(f'{customer['telefono']}',
                                               key='-input_documento-', disabled=True)],
              [sg.Button('Salir\t', key='-salir-')]
              ]

    window = sg.Window('HelloWorld', layout)

    while True:
        event, values = window.read()

        if event == '-salir-':
            break

    window.close()


# Main Window--------------------
layout = [[sg.Text(text='Compraventa el Poblado',
                   font=('Arial Bold', 20),
                   size=20,
                   expand_x=True,
                   justification='center')],
          [sg.Input(key='-input_documento-'),
           sg.Button('Buscar', key='-buscar-')],
          [sg.Button('Lista clientes', key='-mostrar-'),
           sg.Button('Mostrar info cliente', key='-seleccionar-')],
          [sg.Table(values=[], headings=_headings,
                    key='-tabla-', text_color='White', justification='left')],

          [sg.Button('Salir', key='-salir-')]
          ]

window = sg.Window('HelloWorld', layout)

while True:
    event, values = window.read()
    if event == '-buscar-':
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
                customer_data = []
                for _nombre in _nombres:  # función json2table
                    customer_data.append(customer[f'{_nombre}'])

                customer_info_window(customer)
                window['-tabla-'].update([customer_data])

    if event == '-mostrar-':
        url = "http://127.0.0.1:8000/home_clientes"
        data = requests.get(url)
        customers = data.json()

        customer_data = []
        customers_array = []
        for customer in customers:
            for _nombre in _nombres:  # función json2table
                customer_data.append(customer[f'{_nombre}'])
            customers_array.append(customer_data)
            customer_data = []
       # print(customers_array)
       # print(reponse_json)
        window['-tabla-'].update(customers_array)

    elif event == '-seleccionar-':
        url = f"http://127.0.0.1:8000/encontrar_cliente/{
            (values['-tabla-'][0]+1)}"
        data = requests.get(url)
        customer = data.json()
        # print(customer)

        for _nombre in _nombres:  # función json2table
            customer_data.append(customer[f'{_nombre}'])

        window['-tabla-'].update([customer_data])
        customer_info_window(customer)

    elif event == '-salir-':
        break

window.close()
