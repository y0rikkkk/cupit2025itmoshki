from ObjectClasses import Station,Route,Trip,Transfer

def parse_station(data: dict | None):
    if not data:
        return None
    return Station(
        code=data.get("code"),
        title=data.get("title"),
        station_type=data.get("station_type_name"),
        transport_type=data.get("transport_type")
    )

def parse_trip(detail: dict):
    thread = detail.get("thread", {})
    return Trip(
        title=thread.get("title"),
        transport_type=thread.get("transport_type"),
        express_type=thread.get("express_type"),
        carrier=thread.get("carrier"),
        uid=thread.get("uid"),
        vehicle=thread.get("vehicle"),
        from_Station=parse_station(detail.get("from")),
        to_Station=parse_station(detail.get("to")),
        stops=detail.get("stops"),
        departure=detail.get("departure"),
        duration=detail.get("duration"),
    )

def parse_transfer(detail: dict):
    return Transfer(
        duration=detail.get("duration"),
        transfer_point=detail.get("transfer_point", {}).get("title"),
        transfer_from=parse_station(detail.get("transfer_from")),
        transfer_to=parse_station(detail.get("transfer_to"))
    )




def parse_route(segment):
    has_transfers = segment.get('has_transfers', False)

    # Детали маршрута
    details = []
    if has_transfers:
        details = []
        for d in segment.get("details", []):
            if d.get("is_transfer"):
                details.append(parse_transfer(d))
            else:
                details.append(parse_trip(d))

        return Route(
            station_from=parse_station(segment.get("departure_from")),
            station_to=parse_station(segment.get("arrival_to")),
            transport_types=segment.get("transport_types"),
            departure_time=segment.get("departure"),
            arrival_time=segment.get("arrival"),
            has_transfers=segment.get("has_transfers"),
            transfers=segment.get("transfers"),
            details=details
        )
    else:
        trip = parse_trip(segment)
        details.append(trip)

    route = Route(
        station_from=parse_station(segment.get('from')),
        station_to=parse_station(segment.get('to')),
        transport_types=[segment.get('thread', {}).get('transport_type')],
        departure_time=segment.get('departure'),
        arrival_time=segment.get('arrival'),
        has_transfers=has_transfers,
        details=details,
        duration=segment.get('duration'),
        tickets_info=segment.get('tickets_info')
    )
    return route