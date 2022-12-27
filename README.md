
# Project Title: Consensus

Consensus is a Flask server that provides endpoints for accessing various types of information and data from different sources. These endpoints are:

# Endpoints

Endpoint | Path | Description | Example
--- | --- | --- | ---
Livestream | /data/cams/streams | Returns a list of available livestreams and allows users to search for the closest one based on a given location. | `{"location": "New York"}`
Finance | /data/finance/markets | Returns market data from the Yahoo Finance website. | `{"market": "standard", "detail": "gainers"}`
Country | /data/geo/countries | Returns general information about a specified country, including population, coordinates, and region. | `{"country": "United States"}`
City | /data/geo/cities | Returns general information about a specified city, including population, coordinates, and region. | `{"city": "New York"}`
Coordinate | /data/geo/coordinates | Provides the coordinates for a given location. | `{"location": "Eiffel Tower"}`
Sports | /data/sports/events | Returns information about sporting events from the ESPN API. | `{"league": "nba", "status": "scheduled"}`
Weather | /data/weather/forecasts | Gives forecast information for a given location. | `{"location": "Orlando", "timeframe": "forecast"}`
Weather | /data/weather/earthquakes | Returns information about earthquakes. | N/A
Twitter | /data/twitter/tweets | Allows users to search for tweets. | `{"search_term": "Chargers", "count": 10}`
Twitter | /data/twitter/spaces | Allows users to search for spaces. | `{"search_term": "Bitcoin", "count": 10}`
Twitter | /data/twitter/trends | Returns trending topics. | `{"location": "London"}`
Twitter | /data/twitter/users | Allows users to search for specific users. | `{"user_name": "Cristiano"}`

