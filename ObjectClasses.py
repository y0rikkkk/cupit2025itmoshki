from datetime import datetime,timedelta

class Route:
    params = ['station_from', 'station_to','transport_types','departure_time','arrival_time','has_transfers','transfers',
             'details','tickets_info','duration']
    def __init__(self,**kwargs):
        for field in self.__class__.params:
            setattr(self, field, kwargs.get(field, None))
        self.departure_time = datetime.fromisoformat(self.departure_time)
        self.arrival_time = datetime.fromisoformat(self.arrival_time)


    def __repr__(self):
        return f'Route({self.station_from}-{self.station_to})'

    def pretty_print(self):
        output = []

        time_diff = self.arrival_time - self.departure_time
        days = time_diff.days
        hours, remainder = divmod(time_diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        # Эмоджи транспорта
        transport_emojis = {
            'plane': '✈️',
            'train': '🚆',
            'suburban': '🚈',
            'bus': '🚌',
            'water': '⛴',
            'helicopter': '🚁'
        }

        # Собираем цепочку только из объектов Trip
        city_chain = []
        arrow_chain = []

        for d in self.details:
            if isinstance(d, Trip):
                if not city_chain:
                    city_chain.append(d.from_Station.title)
                city_chain.append(d.to_Station.title)
                icon = transport_emojis.get(d.transport_type, '❓')
                arrow_chain.append(icon)
        if not city_chain:
            city_string = "Нет маршрута (нет сегментов Trip)"
        else:
            city_string = city_chain[0]
            for i in range(1, len(city_chain)):
                emoji = arrow_chain[i - 1] if i - 1 < len(arrow_chain) else '➡️'
                city_string += f" ➜{emoji}➜ {city_chain[i]}"
        city_string = city_chain[0]
        for i in range(1, len(city_chain)):
            emoji = arrow_chain[i - 1] if i - 1 < len(arrow_chain) else '➡️'
            city_string += f" ➜{emoji}➜ {city_chain[i]}"

        output.append("=" * 60)
        output.append(f"📅 {self.departure_time.strftime('%d %B %Y %H:%M')} ➜ {self.arrival_time.strftime('%d %B %Y %H:%M')}")
        output.append(f"📍 {city_string}")

        duration_str = []
        if days:
            duration_str.append(f"{days} дн.")
        if hours:
            duration_str.append(f"{hours} ч.")
        if minutes:
            duration_str.append(f"{minutes} мин.")

        output.append(f"🕒 В пути: {' '.join(duration_str)}")
        output.append("\n\n")

        output.append(f"🚩 Отправление из {self.station_from.title} в {self.departure_time.strftime('%H:%M, %d %B')}")

        for detail in self.details:
            if isinstance(detail, Trip):
                arrival_time = detail.departure + timedelta(seconds=detail.duration)
                icon = transport_emojis.get(detail.transport_type, '❓')
                output.append(
                    f"🛣 {detail.title} {icon} | "
                    f"{detail.from_Station.title} ({detail.departure.strftime('%H:%M')}) ➜ "
                    f"{detail.to_Station.title} ({arrival_time.strftime('%H:%M')}) "
                    f"⌛ {round(detail.duration / 60)} мин"
                )
            elif isinstance(detail, Transfer):
                from_title = detail.transfer_from.title if detail.transfer_from else "неизвестно"
                to_title = detail.transfer_to.title if detail.transfer_to else "неизвестно"
                transfer_type = getattr(detail, 'transfer_type', 'неизвестно')

                output.append(
                    f"🔁 Пересадка: {from_title} ➜ {to_title} | "
                    f"Тип: {transfer_type} | Длительность: {round(detail.duration / 60)} мин"
                )

        output.append(f"🏁 Прибытие в {self.station_to.title} в {self.arrival_time.strftime('%H:%M, %d %B')}")
        return "\n".join(output)


#details содержит объекты типа Trip or Transfer в зависимости от наличия флага is_transfer в объекте
class Trip:
    params = ['title', 'transport_type','express_type', 'carrier','uid','vehicle','from_Station','to_Station','stops',
              'departure','duration']
    def __init__(self,**kwargs):
        for field in self.__class__.params:
            setattr(self, field, kwargs.get(field, None))
        self.departure = datetime.fromisoformat(self.departure)
    def __repr__(self):
        return f'Trip({self.title})'

class Transfer:
    params = ['duration','transfer_point','transfer_from','transfer_to']
    def __init__(self,**kwargs):
        for field in self.__class__.params:
            setattr(self, field, kwargs.get(field, None))

    def __repr__(self):
        return f'Transfer({self.transfer_point})'

class Station:
    def __init__(self, code:str, title:str, station_type:str=None, transport_type:str=None):
        self.code = code
        self.title = title
        self.station_type = station_type
        self.transport_type = transport_type

    def __repr__(self):
        return f'Station({self.title} - {self.code})'





def select_date():
    while True:
        raw = input("📅 Введите дату в формате ГГГГ-ММ-ДД: ").strip()
        try:
            dt = datetime.strptime(raw, "%Y-%m-%d")
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            print("❌ Неверный формат. Попробуйте ещё раз.")


