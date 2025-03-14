import json

# Названия категорий объектов
station_type_labels = {
    "train_station": "🚉 Вокзалы",
    "platform": "🏁 Платформы",
    "bus_station": "🚌 Автовокзалы",
    "bus_stop": "🛑 Автобусные остановки",
    "airport": "🛫 Аэропорты",
    "station": "🚉 Станции (другие)",
    "water": "⛴ Водный транспорт",
    "unknown": "❓ Прочее",
    "region": "🌍 Регионы",
    "settlement": "🏙 Города",
    "country": "🗺 Страны"
}


class StationFinder:
    def __init__(self, json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            self.raw_data = json.load(f)
        self.index = self._build_index()

    def _build_index(self):
        index = {}
        for country in self.raw_data.get("countries", []):
            country_title = country.get("title")
            for region in country.get("regions", []):
                region_title = region.get("title")
                for settlement in region.get("settlements", []):
                    settlement_title = settlement.get("title")

                    # Сохраняем город
                    self._add_to_index(index, settlement_title, {
                        "title": settlement_title,
                        "settlement": settlement_title,
                        "region": region_title,
                        "country": country_title,
                        "code": settlement.get("codes", {}).get("yandex_code"),
                        "station_type": "settlement"
                    })

                    for station in settlement.get("stations", []):
                        station_title = station.get("title", "").strip()
                        code = station.get("codes", {}).get("yandex_code")
                        station_type = station.get("station_type") or "unknown"

                        if station_title and code:
                            self._add_to_index(index, station_title, {
                                "title": station_title,
                                "settlement": settlement_title,
                                "region": region_title,
                                "country": country_title,
                                "code": code,
                                "station_type": station_type
                            })

                # Добавляем регион
                self._add_to_index(index, region_title, {
                    "title": region_title,
                    "settlement": "",
                    "region": region_title,
                    "country": country_title,
                    "code": region.get("codes", {}).get("yandex_code"),
                    "station_type": "region"
                })

            # Добавляем страну
            self._add_to_index(index, country_title, {
                "title": country_title,
                "settlement": "",
                "region": "",
                "country": country_title,
                "code": country.get("codes", {}).get("yandex_code"),
                "station_type": "country"
            })

        return index

    def _add_to_index(self, index, key, data):
        key = key.strip().lower()
        index.setdefault(key, []).append(data)

    def search(self, partial_query):
        partial = partial_query.strip().lower()
        results = []

        # Поиск по названию
        for name, stations in self.index.items():
            if partial in name:
                results.extend(stations)

        # Расширенный поиск: добавим аэропорты, у которых settlement == partial
        for station_list in self.index.values():
            for station in station_list:
                if (
                    station["station_type"] == "airport"
                    and station.get("settlement", "").strip().lower() == partial
                    and station not in results
                ):
                    results.append(station)

        return results

    def interactive_lookup(self):
        while True:
            query = input("Введите часть названия станции (или 'выход' для выхода): ").strip()
            if query.lower() in ('выход', 'exit', 'q'):
                break

            code = self._lookup_single_station(query)
            if code:
                print(f"\n✅ Код выбранной точки: {code}\n")

    def _lookup_single_station(self, query):
        matches = self.search(query)
        if not matches:
            print("❌ Ничего не найдено, попробуйте ещё раз.")
            return None

        # Группировка по типу станции
        grouped = {}
        for s in matches:
            grouped.setdefault(s['station_type'], []).append(s)

        # Вывод
        numbered = []
        index = 1
        for stype in sorted(grouped, key=self._station_sort_priority):
            label = station_type_labels.get(stype, stype)
            print(f"\n=== {label} ===")
            for s in grouped[stype]:
                loc = ", ".join(filter(None, [s['settlement'], s['region'], s['country']]))
                print(f"{index}. {s['title']} — {loc} ({label})")
                numbered.append(s)
                index += 1

        try:
            selection = int(input("\nВведите номер нужной станции: "))
            selected = numbered[selection - 1]
            return selected['code']
        except (ValueError, IndexError):
            print("⚠️ Некорректный ввод. Попробуйте ещё раз.\n")
            return None

    def lookup_from_to(self):
        print("\n🔎 Поиск точки отправления:")
        from_code = None
        while not from_code:
            query = input("Введите название точки отправления: ")
            if query.lower() in ("выход", "exit", "q"):
                return None, None
            from_code = self._lookup_single_station(query)

        print("\n🔎 Поиск точки прибытия:")
        to_code = None
        while not to_code:
            query = input("Введите название точки прибытия: ")
            if query.lower() in ("выход", "exit", "q"):
                return None, None
            to_code = self._lookup_single_station(query)

        return from_code, to_code

    def _station_sort_priority(self, station_type):
        # Чем меньше число — тем выше в списке
        priorities = {
            "settlement": 1,
            "train_station": 3,
            "airport": 2,
            "bus_station": 4,
            "platform": 5,
            "station": 6,
            "bus_stop": 7,
            "region": 8,
            "country": 9,
            "unknown": 99,
        }
        return priorities.get(station_type, 99)