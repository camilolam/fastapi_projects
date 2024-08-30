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
                                 font=('Arial Bold', 20),
                                 size=20,
                                 expand_x=True,
                                 justification='center')],
                        [sg.Text('Id\t'), sg.Input(
                            key='-input_id-', disabled=True, text_color='white')],
                        [sg.Text('Nombre\t'), sg.Input(key=f'-input_nombre-',
                                                       disabled=True, text_color='white')],
                        [sg.Text('Cédula\t'), sg.Input(key='-input_documento-',
                                                       disabled=True, text_color='white')],
                        [sg.Text('Correo\t'), sg.Input(key='-input_correo-',
                                                       disabled=True, text_color='white')],
                        [sg.Text('Teléfono\t'), sg.Input(
                            key='-input_documento-', disabled=True, text_color='white')]
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
          [sg.Table(values=[], headings=_headings,
                    key='-tabla-', text_color='White', justification='left')],

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
                customer_data = []
                for _nombre in _nombres:  # función json2table
                    customer_data.append(customer[f'{_nombre}'])

                customer_info_window(customer)

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
        id_tabla = values['-tabla-']
        if (id_tabla == []):
            sg.popup('Selecciona una opción en la tabla')
        else:
            url = f"http://127.0.0.1:8000/encontrar_cliente/{(id_tabla[0]+1)}"
            data = requests.get(url)
            customer = data.json()

            for _nombre in _nombres:  # función json2table
                customer_data.append(customer[f'{_nombre}'])

            window['-input_id-']
            window['-input_nombre-']
            window['-input_document-']
            window['-input_document-']
            customer_info_window(customer)

    elif event == '-salir-':
        break

window.close()
