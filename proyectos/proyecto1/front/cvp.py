import PySimpleGUI as sg  # type: ignore
import requests

sg.theme('DarkAmber')

""" UTILITIES """


def json2table(data, names):
    data_array = []
    response = []
    for dat in data:
        for name in names:  # función json2table
            data_array.append(dat[f'{name}'])
        response.append(data_array)
        data_array = []
    return response


""" MAIN WINDOW """
url = f"http://127.0.0.1:8000/get_contracts_names"
names = requests.get(url)
names_json = names.json()

url2 = 'http://127.0.0.1:8000/get_contracts'
contracts = requests.get(url2)
contracts_json = contracts.json()
print('oe estamos aca')

tabla = json2table(contracts_json, names_json)
print(tabla)

column1 = [
    [sg.Text(text='Criterio de búsqueda',
             font=('Arial Bold', 15),
             size=20,
             justification='left')],
    [sg.Combo(['Contrato', 'Cliente'],
              default_value='-Selecciona-', size=(43, 12), key='-search_option-')],
    [sg.Input(key='-input_search-'),
     sg.Button('Buscar', key='-search_button-')],
]

Column2 = [
    [sg.Text(text='Información Del Cliente',
             font=('Arial Bold', 15),
             size=20,
             justification='left')],
    [sg.Text('Nombre Completo  \t'), sg.Input(key=f'-input_name-',
                                              disabled=True)],
    [sg.Text('Documento\t'), sg.Input(key='-input_document-',
                                      disabled=True)],
    [sg.Text('Correo Electrónico  \t'), sg.Input(key='-input_email-',
                                                 disabled=True)],
    [sg.Text()],
]

layout = [
    [sg.Text(text='Compraventa el Poblado',
             font=('Arial Bold', 15),
             size=20,
             expand_x=True,
             justification='center')],
    [sg.Text()],
    [sg.Column(column1), sg.Text(), sg.Column(Column2)],
    [sg.Button('Lista clientes', key='-mostrar-'),
     sg.Button('Mostrar info cliente', key='-seleccionar-')],
    [sg.Table(values=tabla, headings=names_json,
              key='-tabla-', text_color='black', justification='left', background_color='white', expand_x=True)],

    [sg.Button('Salir', key='-salir-')]
]

window = sg.Window('Compravente el Poblado', layout)

while True:
    event, values = window.read()
    if event == '-search_button-':
        option_search = values['-search_option-']
        input_search = values['-input_search-']

        if option_search == '-Selecciona-':
            sg.popup('Selecciona un criterio de búsqueda')
        elif input_search == "":
            sg.popup('Ingresa un documento')

        else:
            if option_search == 'Cliente':
                url = "http://127.0.0.1:8000/get_customer_by_document/%i" % (
                    int(input_search))
                data = requests.get(url)
                customer = data.json()
                if customer == -1:
                    sg.popup('Usuario no encontrado')
                else:
                    window['-input_name-'].update('%s %s' % (customer['name'],
                                                             customer['surname']))
                    window['-input_document-'].update(customer['document'])
                    window['-input_email-'].update(customer['email'])
                    url = "http://127.0.0.1:8000/get_contract_by_customer_id/%i" % (
                        int(customer['id']))
                    data = requests.get(url)
                    contracts = data.json()

                    url = "http://127.0.0.1:8000/get_contracts_names"
                    data_name = requests.get(url)
                    names = data_name.json()

                    data_table = json2table(contracts, names)
                    window['-tabla-'].update(values=data_table)

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
