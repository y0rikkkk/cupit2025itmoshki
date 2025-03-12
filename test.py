import json
import requests
from parser import parse_route
from station_finder import StationFinder

#Получаем коды станций
# mane = StationFinder('stations_list.json')
# mane.interactive_lookup()



yandex_api_key = '6833833d-d478-4dca-bae0-e0b11d870ecb'
station_from = 's9748489'  # Остановка Стерлитамак
station_to = 's9602742'    # Осатновка в Тамбове

# Дата поездки в формате YYYY-MM-DD
date = '2025-03-14'

# URL эндпоинта для получения расписания между станциями
url = 'https://api.rasp.yandex.net/v3.0/search/'

# Параметры запроса
params = {
    'apikey': yandex_api_key,
    'format': 'json',
    'from': station_from,
    'to': station_to,
    'lang': 'ru_RU',
    'date': date,
    'transfers':True,
}

# Выполнение GET-запроса
response = requests.get(url, params=params)
parsed = response.json()


if response.status_code == 200:
    data = response.json()

routes = [parse_route(seg) for seg in data.get('segments', [])]

for route in routes:
    print(route.details)



