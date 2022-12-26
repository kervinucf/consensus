from server.gateways.data.resources.providers.earthcam.sources.Youtube.utils import get_distance, youtube_live_streams
from server.gateways.data.resources.providers.geo.sources.Nominatim.helpers import \
    find_coordinates


def find_earth_streams_by_location(target_location, radius_in_km):
    earth_streams = {}
    target_coordinates = find_coordinates(location=target_location)
    if target_coordinates:
        target_coordinates = tuple(target_coordinates.values())
        for location_stream in find_available_earth_streams():
            stream_coordinates = tuple(location_stream['coordinates'].values())
            stream_distance_from_target = get_distance(
                target_coordinates, stream_coordinates)
            print(
                f"STREAM DISTANCE FROM TARGET -> {location_stream['location']}: ", stream_distance_from_target)
            distance_in_km = round(stream_distance_from_target, 3)
            location_stream['distance'] = distance_in_km
            if stream_distance_from_target <= radius_in_km:
                try:
                    streams = earth_streams[distance_in_km]
                    streams.append(location_stream)
                    earth_streams[distance_in_km] = streams
                except KeyError:
                    earth_streams[distance_in_km] = [location_stream]

    else:
        earth_streams = None
    return earth_streams


def find_available_earth_streams():
    return youtube_live_streams
