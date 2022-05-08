import requests
import json

class ConvertExeption(Exception):
    pass

class ApiExeption(Exception):
    pass

class Cryptoconverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertExeption(f'Невозможно перевести одинаковые валюты{base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertExeption(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertExeption(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertExeption(f'Не удалось обработать количество {amount}')