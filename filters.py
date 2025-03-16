from ObjectClasses import Transfer,Trip
from datetime import datetime,timedelta

def build_api_params(base_params, user_filters):
    params = base_params.copy()

    # Фильтр "типы транспорта"
    if 'transport_types' in user_filters and user_filters['transport_types']:
        params['transport_types'] = ','.join(user_filters['transport_types'])

    # Фильтр "только прямые маршруты"
    if user_filters.get('direct_only') is True:
        params['transfers'] = False
    else:
        params['transfers'] = True

    return params


def filter_by_transfer_duration_range(routes, min_sec, max_sec):
    filtered = []
    for r in routes:
        transfers = [d for d in r.details if isinstance(d, Transfer)]
        if all(min_sec <= t.duration <= max_sec for t in transfers):
            filtered.append(r)
    return filtered


def filter_by_non_working_hours(routes, work_start=10, work_end=18):
    filtered = []
    for r in routes:
        valid = True
        for detail in r.details:
            if isinstance(detail, Trip):
                dep_hour = detail.departure.hour
                arr_hour = (detail.departure + timedelta(seconds=detail.duration)).hour
                if work_start <= dep_hour < work_end or work_start <= arr_hour < work_end:
                    valid = False
                    break
        if valid:
            filtered.append(r)
    return filtered


def sort_by_departure_time(routes):
    return sorted(routes, key=lambda r: r.departure_time)

def sort_by_arrival_time(routes):
    return sorted(routes, key=lambda r: r.arrival_time)

def sort_by_duration(routes):
    return sorted(
        routes,
        key=lambda r: (r.arrival_time - r.departure_time).total_seconds()
    )
    return sorted(routes, key=lambda r: r.duration or float('inf'))
