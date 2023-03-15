import json
import requests

class PostalCodeAPI:
    
    def __init__(self):
        self.url = "https://apicp.softfortoday.com/api/v1/"
        self.states = {}
        self.towns = {}
        self.postal_code_info = {}
        
    def get_states(self):
        """
        Obtiene la lista de estados de la API de códigos postales
        """
        url = 'estados'
        request = requests.get(self.url + url)
        if request.status_code == 200:
            response = json.loads(request.text)
            for state in response['respuesta']['estados']:
                self.states[state['clave']] = state['estado']
            return self.states
        return response

    def get_towns(self, state_code):
        """
        Obtiene la lista de municipioss pasando el codigo del estado
        """
        url = f'municipios/{state_code}'
        request = requests.get(self.url + url)
        if request.status_code == 200:
            response = json.loads(request.text)
            for town in response['respuesta']['municipios']:
                self.towns[town['clave']] = town['municipio']
            return self.towns
        return response
    
    def get_postal_code(self, postal_code):
        """
        Obtiene la información del código postal 
        """
        url = f'codigos_postales/{postal_code}'
        response = requests.get(self.url + url).json()
        if response.get('respuesta'):
            codigos_postales = response['respuesta']['codigos_postales']
            for cp in codigos_postales:
                codigo_postal = cp['codigo_postal']
                if codigo_postal not in self.postal_code_info:
                    self.postal_code_info[codigo_postal] = {
                        'codigo_postal': codigo_postal,
                        'asentamiento': [cp['asentamiento']],
                        'tipo_asentamiento': cp['tipo_asentamiento'],
                        'zona': cp['zona'],
                        'municipio': cp['municipio'],
                        'estado': cp['estado'],
                        'pais': cp['pais']
                    }
                else:
                    self.postal_code_info[codigo_postal]['asentamiento'].append(cp['asentamiento'])
            return self.postal_code_info
        return response