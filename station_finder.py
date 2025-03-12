import json

# Приоритет типов транспорта
transport_priority = {
    "train": 1,
    "suburban": 2,
    "plane": 3,
    "bus": 4,
    "water": 5,
    "unknown": 99
}

# Названия типов транспорта с иконками
transport_labels = {
    "train": "🚆 Поезда",
    "suburban": "🚉 Пригородные",
    "plane": "✈️ Самолёты",
    "bus": "🚌 Автобусы",
    "water": "⛴ Водный транспорт",
    "unknown": "❓ Неизвестный тип"
}


class StationFinder:
    def __init__(self, json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            self.raw_data = json.load(f)
        self.index = self._build_index()

    def _build_index(self):
        index = {}
        for country in self.raw_data.get("countries", []):
            for region in country.get("regions", []):
                for settlement in region.get("settlements", []):
                    for station in settlement.get("stations", []):
                        name = station.get("title", "").strip().lower()
                        code = station.get("codes", {}).get("yandex_code")
                        if name and code:
                            index.setdefault(name, []).append({
                                "station": station.get("title"),
                                "settlement": settlement.get("title"),
                                "region": region.get("title"),
                                "country": country.get("title"),
                                "code": code,
                                "type": station.get("transport_type") or "unknown"
                            })
        return index

    def search(self, partial_query):
        partial = partial_query.strip().lower()
        results = []
        for name, stations in self.index.items():
            if partial in name:
                results.append((name, stations))
        return results

    def interactive_lookup(self):
        while True:
            query = input("Введите часть названия станции (или 'выход' для выхода): ").strip()
            if query.lower() in ('выход', 'exit', 'q'):
                break

            matches = self.search(query)
            if not matches:
                print("❌ Станции не найдены, попробуйте ещё раз.")
                continue

            # Собираем все подходящие станции
            all_options = []
            for _, station_list in matches:
                all_options.extend(station_list)

            # Сортировка
            all_options.sort(key=lambda s: (transport_priority.get(s['type'], 99), s['station']))

            # Группировка
            print(f"\n🔍 Найдено {len(all_options)} станций:\n")
            grouped = {}
            for s in all_options:
                t = s['type']
                grouped.setdefault(t, []).append(s)

            # Пронумерованный список
            numbered = []
            index = 1
            for t_type in sorted(grouped, key=lambda t: transport_priority.get(t, 99)):
                label = transport_labels.get(t_type, t_type)
                print(f"\n=== {label} ===")
                for s in grouped[t_type]:
                    print(f"{index}. {s['station']} — {s['settlement']}, {s['region']}, {s['country']}")
                    numbered.append(s)
                    index += 1

            # Выбор
            try:
                selection = int(input("\nВведите номер нужной станции: "))
                selected = numbered[selection - 1]
                print(f"\n✅ Код выбранной станции: {selected['code']}\n")
            except (ValueError, IndexError):
                print("⚠️ Некорректный ввод. Попробуйте ещё раз.\n")