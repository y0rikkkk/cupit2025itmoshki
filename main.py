import json
import requests
from parser import parse_route
from station_finder import StationFinder
from ObjectClasses import select_date,Trip


yandex_api_key = '6833833d-d478-4dca-bae0-e0b11d870ecb'

finder = StationFinder('stations_list.json')
# station_from,station_to = finder.lookup_from_to()
#
# # Дата поездки в формате YYYY-MM-DD
# date = select_date()

station_from = 'c11116'
station_to = 'c43621'
date ='2025-03-18'
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
    print(route.departure_time)
    for item in route.details:
        if isinstance(item,Trip):
            print(item.departure)

    print(route.arrival_time)


