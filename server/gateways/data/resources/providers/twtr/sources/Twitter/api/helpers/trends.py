from server.gateways.data.resources.providers.twtr.sources.Twitter.api.utils.bearer import bearer_oauth


def create_url(_id=None, coordinates=None):
    url = 'https://api.twitter.com/1.1/trends/available.json'
    if coordinates:
        url = 'https://api.twitter.com/1.1/trends/closest.json?lat={}&long={}'.format(coordinates['lat'],
                                                                                      coordinates['lng'])
    if _id is not None:
        url = 'https://api.twitter.com/1.1/trends/place.json?id={}'.format(_id)
    return url


def find_trends_available():
    url = create_url()
    return {
        'url': url,
        'params': None,
        'headers': bearer_oauth,
        "GET": True
    }


def search_trends_from(place):
    url = create_url(_id=place)
    return {
        'url': url,
        'params': None,
        'headers': bearer_oauth,
        "GET": True
    }


def get_trends_closest(lat, lng):
    url = create_url(coordinates={
        'lat': lat,
        'lng': lng
    })
    return {
        'url': url,
        'params': None,
        'headers': bearer_oauth,
        "GET": True
    }
