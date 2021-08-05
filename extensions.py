import requests
import json
from config import keys


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if quote == base:
            raise APIException("Нельзя перевести одинаковые валюты!")

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту {base}")

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту {quote}")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException("Неправилно задано количество целевой валюты!")

        r = requests.get(f'https://api.exchangeratesapi.io/latest?symbols={quote_ticker}&base={base_ticker}')
        result = json.loads(r.content)['rates'][keys[quote]] * amount
        return result
