import json
import requests
from parser import parse_route
from station_finder import StationFinder
from ObjectClasses import select_date,Trip
import locale
from filters import build_api_params
yandex_api_key = '6833833d-d478-4dca-bae0-e0b11d870ecb'
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
#
# finder = StationFinder('stations_list.json')
# station_from,station_to = finder.lookup_from_to()
#
# # Дата поездки в формате YYYY-MM-DD
# date = select_date()

station_from = 'c11116'
station_to = 'c43621'
date ='2025-03-20'
# URL эндпоинта для получения расписания между станциями
url = 'https://api.rasp.yandex.net/v3.0/search/'

# Параметры запроса
base_params = {
    'apikey': yandex_api_key,
    'format': 'json',
    'from': station_from,
    'to': station_to,
    'lang': 'ru_RU',
    'date': date,
    'transfers':True,
}

# 🚇 Выбор транспорта
print("""Укажите типы транспорта через запятую (если хотите выбрать все — оставьте пустым):
  ✈️ plane
  🚆 train
  🚈 suburban
  🚌 bus
  ⛴ water
  🚁 helicopter
""")
types_input = input("Типы транспорта: ").strip()
transport_types = [t.strip() for t in types_input.split(',') if t.strip()] if types_input else []

# 🚫 Прямые маршруты
print("Хотите отфильтровать только прямые маршруты? (y/n)")
direct_only = input().strip().lower() == 'y'

user_filters = {
    'transport_types': transport_types,  # пустой список = все типы
    'direct_only': direct_only
}

params = build_api_params(base_params, user_filters)
# Выполнение GET-запроса
response = requests.get(url, params=params)
parsed = response.json()


if response.status_code == 200:
    data = response.json()
else:
    print(parsed)

routes = [parse_route(seg) for seg in data.get('segments', [])]
print(len(routes))


for route in routes:
    print(route.pretty_print())
    print("="*50)

