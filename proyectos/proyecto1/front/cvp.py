import PySimpleGUI as sg  # type: ignore
import requests  # type: ignore
from pathlib import Path
import json

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


def fill_table(window, customer):
    window['-input_id-'].update(customer['id'])
    window['-input_name-'].update('%s %s' % (customer['name'],
                                             customer['surname']))
    window['-input_document-'].update(customer['document'])
    window['-input_email-'].update(customer['email'])


def query(url):
    data = requests.get(url)
    response = data.json()
    return response


def save_selected(window, contract, customer):
    window['-selected_info_text-'].update(
        "información seleccionada: \t Cliente: %s - Contrato: %i" % (customer['name'], contract['contract']))
    with open('../tmp/tmp.json', 'w') as json_file:
        new_data = {
            "contract": contract,
            "customer": customer
        }
        data = json.dump(new_data, json_file)


""" MAIN WINDOW """

data = query('http://127.0.0.1:8000/get_contracts')
contracts = data['info']
names = data['column_names']
tabla = json2table(contracts, names)

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
    [sg.Text('id  \t\t'), sg.Input(key=f'-input_id-',
                                   disabled=True)],
    [sg.Text('Nombre Completo  \t'), sg.Input(key=f'-input_name-',
                                              disabled=True)],
    [sg.Text('Documento\t'), sg.Input(key='-input_document-',
                                      disabled=True)],
    [sg.Text('Correo Electrónico  \t'), sg.Input(key='-input_email-',
                                                 disabled=True)],
    [sg.Text('No se ha seleccinado informacion  \t', key='-selected_info_text-')],
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
    [
        sg.Button('Inicio', key='-show_all-'),
        sg.Button('Seleccionar contrato', key='-select_contract-'),
        sg.Button('Nuevo Contrato', key='-add_contract-'),
        sg.Button('Adicional', key='-additinal_contract-'),
        sg.Button('Abono', key='-payment_contract-'),
        sg.Button('Renovación', key='-renewal_contract-')
    ],
    [sg.Table(values=tabla,
              headings=names,
              key='-tabla-',
              text_color='black',
              justification='left',
              background_color='white',
              expand_x=True,
              enable_click_events=True)],

    [sg.Button('Salir', key='-salir-')]
]

window = sg.Window('Compraventa el Poblado', layout)

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
                data = query("http://127.0.0.1:8000/get_customer_by_document/%i" % (
                    int(input_search)))

                if data == -1:
                    sg.popup('Usuario no encontrado')
                else:
                    window['-selected_info_text-'].update(
                        'No se ha seleccinado informacion')
                    with open('../tmp/tmp.json', 'w') as json_file:
                        data = json.dump('', json_file)
                    customer = data['info']
                    data = query("http://127.0.0.1:8000/get_contracts_by_customer_id/%i" % (
                        int(customer['id'])))
                    contracts = data['info']
                    names = data['column_names']
                    data_table = json2table(contracts, names)
                    fill_table(window, customer)
                    window['-tabla-'].update(values=data_table)

            if option_search == 'Contrato':
                data = query("http://127.0.0.1:8000/get_contract_by_contract/%i" % (
                    int(input_search)))

                if data == -1:
                    sg.popup('Contrato no encontrado, ingresa contrato valido')
                else:
                    contract = data['info']
                    names = data['column_names']
                    data = query("http://127.0.0.1:8000/get_customer_by_id/%i" % (
                        contract['customer_id']))
                    customer = data['info']

                    data_table = json2table([contract], names)
                    window['-tabla-'].update(values=data_table)
                    fill_table(window, customer)
                    save_selected(window, contract, customer)

    elif event == '-show_all-':
        with open('../tmp/tmp.json', 'w') as json_file:
            data = json.dump('', json_file)
        window['-selected_info_text-'].update(
            'No se ha seleccinado informacion')
        data = query("http://127.0.0.1:8000/get_contracts")
        contracts = data['info']
        names = data['column_names']
        table_data = json2table(contracts, names)

        window['-tabla-'].update(table_data)
        window['-input_id-'].update('')
        window['-input_name-'].update('')
        window['-input_document-'].update('')
        window['-input_email-'].update('')

    elif event == '-select_contract-':
        print(values)

        customer_id = values['-input_id-']

        if (values['-tabla-'] == []):
            sg.popup('Selecciona una opción en la tabla')
        else:
            id_tabla = values['-tabla-'][0]
            if customer_id == '':
                data = query("http://127.0.0.1:8000/get_contracts")
            else:
                data = query("http://127.0.0.1:8000/get_contracts_by_customer_id/%i" % (
                    int(customer_id)))

            contract_selected = data['info'][id_tabla]
            names = data['column_names']

            data = query("http://127.0.0.1:8000/get_customer_by_id/%i" % (
                int(contract_selected['customer_id'])))
            customer = data['info']
            data_table = json2table([contract_selected], names)
            fill_table(window, customer)
            save_selected(window, contract_selected, customer)
            window['-tabla-'].update(values=data_table)

    elif event == '-salir-':
        break


window.close()

# if isinstance(event, tuple): Esta es la forma de hacer que cuando seleccione alguna celda en la tabla, se pueda hacer sin un botón

#     # TABLE CLICKED Event has value in format ('-TABLE=', '+CLICKED+', (row,col))
#     if event[0] == '-tabla-':
#         print(values['-tabla-'])
#         window['-tabla-']
