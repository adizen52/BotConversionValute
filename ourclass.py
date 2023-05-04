import requests
import json

class ConvertException(Exception):
    pass


class ValConv:
    @staticmethod
    def covert_valute(val1, val2, freq):
        with open('basevalute.json', 'r') as data:
            json_obj = json.load(data)

        if val1 == val2:
            raise ConvertException('Нельзя вводить одинаковые валюты.')

        if val1.upper() not in json_obj:
            raise ConvertException(f'Не удалось обработать: {val1}')

        if val2.upper() not in json_obj:
            raise ConvertException(f'Не удалось обработать: {val2}')

        try:
            freq = float(freq)
        except ValueError:
            raise ConvertException(f'Не удалось обработать: {freq}')

        r = requests.get(f'https://v6.exchangerate-api.com/v6/820a7e6fb564ea48ea280740/pair/{val1}/{val2}/{freq}')

        return json.loads(r.content)['conversion_result']