from server.gateways.data.resources.providers.earthcam.sources.Youtube.interface import YoutubeEarthCamProvider

class EarthCamAggregator:
    youtube_provider = YoutubeEarthCamProvider()

    def __init__(self, provider=None):
        pass

    # ##################################################################################################################
    # LIVE ENDPOINTS     ###############################################################################################
    # ##################################################################################################################

    def get_streams(self, location=None):
        # check if location is provided
        # aggregate streams from all data
        # return streams
        streams = self.youtube_provider.get_streams(location)
        return streams

    def get_all_streams(self):
        # check if location is provided
        # aggregate streams from all data
        # return streams
        streams = self.youtube_provider.get_all_streams()
        return streams

