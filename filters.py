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
