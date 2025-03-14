class Route:
    params = ['station_from', 'station_to','transport_types','departure_time','arrival_time','has_transfers','transfers',
             'details']
    def __init__(self,**kwargs):
        for field in self.__class__.params:
            setattr(self, field, kwargs.get(field, None))

    def __repr__(self):
        return f'Route({self.station_from}-{self.station_to})'

#details содержит объекты типа Trip or Transfer в зависимости от наличия флага is_transfer в объекте
class Trip:
    params = ['title', 'transport_type','express_type', 'carrier','uid','vehicle','from_Station','to_Station','stops',
              'departure','duration']
    def __init__(self,**kwargs):
        for field in self.__class__.params:
            setattr(self, field, kwargs.get(field, None))

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

#добавить


