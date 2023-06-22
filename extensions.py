import requests
import json
import time
from config import API, currency_list

tym = time.localtime()
opt = time.strftime("%d/%m/%Y, %H:%M:%S", tym)

class ValuesException(Exception):
    pass

class CryptoConvertor:
    @staticmethod
    def convert(quote, base, amount):
        try:
            quote_key = currency_list[quote.lower()]
        except KeyError:
            raise ValuesException(f'Валюта "{quote}" не найдена!')
        try:
            base_key = currency_list[base.lower()]
        except KeyError:
            raise ValuesException(f'Валюта "{base}" не найдена!')
        if base_key == quote_key:
            raise ValuesException(f'Невозможно конвертировать валюту "{base.lower()}" в валюту "{quote.lower()}"!')
        try:
            amount = float(amount)
        except ValueError:
            raise ValuesException(f'Не удалось обработать количество {amount}!')

        url = (f'https://api.apilayer.com/currency_data/convert?to={quote_key}&from={base_key}&amount={amount}')
        headers = {"apikey": API}
        response = requests.request("GET", url, headers=headers)
        result = json.loads(response.text)
        text = f'На {opt}  стоимость  {round(float(amount),2)}  {base.lower()}  составляет  {round(float(result["result"]),2)}  {quote.lower()}'

        return text