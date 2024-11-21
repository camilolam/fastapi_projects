import requests
import json


class Utilities(object):
    def __init__(self, window):
        self.window = window

    def blink_button(self, state):
        self.window['-add_contract-'].update(disabled=state)
        self.window['-additinal_contract-'].update(disabled=state)
        self.window['-payment_contract-'].update(disabled=state)
        self. window['-renewal_contract-'].update(disabled=state)

    def json2table(self, data, names):
        """ 
        convierte datos json en listas, para usar en tablas de pysimple gui. 
        * si solo se necesita un dato, pasarlo como una lista con un único valor
        """
        data_array = []
        response = []
        for dat in data:
            for name in names:  # función json2table
                data_array.append(dat[f'{name}'])
            response.append(data_array)
            data_array = []
        return response

    def fill_table(self, customer):
        self.window['-input_id-'].update(customer['id'])
        self.window['-input_name-'].update('%s %s' % (customer['name'],
                                                      customer['surname']))
        self.window['-input_document-'].update(customer['document'])
        self.window['-input_email-'].update(customer['email'])

    def query(url):
        data = requests.get(url)
        response = data.json()
        return response

    def save_selected(self, contract, customer):
        self.window['-selected_info_text-'].update(
            "información seleccionada: \t Cliente: %s - Contrato: %i" % (customer['name'], contract['contract']))
        with open('../tmp/tmp.json', 'w') as json_file:
            new_data = {
                "contract": contract,
                "customer": customer
            }
            data = json.dump(new_data, json_file)

        self.blink_button(False)

    def str_op(self):
        print("la clase está funcionando")
