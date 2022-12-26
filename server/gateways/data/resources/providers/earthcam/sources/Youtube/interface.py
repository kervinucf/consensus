from server.gateways.data.resources.providers.earthcam.sources.Youtube.helpers import find_earth_streams_by_location, \
    find_available_earth_streams


class YoutubeEarthCamProvider:

    def __init__(self):
        pass

    @staticmethod
    def get_streams(location=None):
        return find_earth_streams_by_location(target_location=location, radius_in_km=100)

    @staticmethod
    def get_all_streams():
        return find_available_earth_streams()