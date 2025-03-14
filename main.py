import json
import requests
from parser import parse_route
from station_finder import StationFinder
from ObjectClasses import select_date


yandex_api_key = '6833833d-d478-4dca-bae0-e0b11d870ecb'

finder = StationFinder('stations_list.json')
station_from,station_to = finder.lookup_from_to()

# Дата поездки в формате YYYY-MM-DD
date = select_date()

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
else:
    print(parsed)

routes = [parse_route(seg) for seg in data.get('segments', [])]

for route in routes:
    print(route.details)
    print(route.duration, 'sec' )
    print(route.tickets_info)


