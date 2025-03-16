import json
import requests
from parser import parse_route
from station_finder import StationFinder
from ObjectClasses import select_date,Trip
import locale
from filters import build_api_params,filter_by_transfer_duration_range,filter_by_non_working_hours,sort_by_duration,sort_by_arrival_time,sort_by_departure_time

yandex_api_key = '6833833d-d478-4dca-bae0-e0b11d870ecb'
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

finder = StationFinder('stations_list.json')
station_from,station_to = finder.lookup_from_to()

# Дата поездки в формате YYYY-MM-DD
date = select_date()

#'это я для быстрой отладки юзал, стерлитамак-лосево
# station_from = 'c11116'
# station_to = 'c43621'
# date ='2025-03-20'

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

# Интервал длительности пересадок
if user_filters['direct_only'] == False:
    print("Укажите допустимую длительность пересадок в минутах (например: 10-90, по умолчанию минимальная пересадка - 1 час):")
    transfer_input = input("Интервал: ").strip()

    transfer_min, transfer_max = 3600, 99999  # значения по умолчанию
    try:
        transfer_min, transfer_max = [int(x) * 60 for x in transfer_input.split('-')]
    except:
        print("⚠️ Неверный формат интервала. Пропускаем фильтрацию по пересадкам.")



print("❓ Оставить только маршруты вне рабочего времени (до 10:00 и после 18:00)? (y/n)")
only_non_working = input().strip().lower() == 'y'



params = build_api_params(base_params, user_filters)
# Выполнение GET-запроса
response = requests.get(url, params=params)
parsed = response.json()


if response.status_code == 200:
    data = response.json()
else:
    print(parsed)

routes = [parse_route(seg) for seg in data.get('segments', [])]
if user_filters['direct_only'] == False:
    routes = filter_by_transfer_duration_range(routes, transfer_min, transfer_max)
if only_non_working:
    routes = filter_by_non_working_hours(routes)


print("""Выберите способ сортировки маршрутов:
1 — По времени отправления
2 — По времени прибытия
3 — По продолжительности поездки
Оставьте пустым, если сортировка не требуется.
""")
sort_choice = input("Ваш выбор: ").strip()

if sort_choice == '1':
    routes = sort_by_departure_time(routes)
elif sort_choice == '2':
    routes = sort_by_arrival_time(routes)
elif sort_choice == '3':
    routes = sort_by_duration(routes)

for route in routes:
    print(route.pretty_print())
    print("="*40)

