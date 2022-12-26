import json
from server.lib.utils.database import get_transaction, get_from_db, update_record, get_db

from geopy.geocoders import Nominatim
from geonamescache import GeonamesCache
from logging import getLogger
logger = getLogger(__name__)


def get_coordinates(location):

    try:
        geolocator = Nominatim(user_agent="conversation-globe")
        coordinates = geolocator.geocode(location)
        return {
            'lat': coordinates.latitude,
            'lng': coordinates.longitude
        }
    except Exception as e:
        if "geopy.exc.GeocoderUnavailable" in str(e):
            logger.debug("geopy is unavailable")

from tzwhere import tzwhere


def get_timezone(lat, lng):
    t = tzwhere.tzwhere()
    timezone_str = t.tzNameAt(lat, lng)
    return timezone_str


def get_country_list():
    country_list = ['Andorra', 'United Arab Emirates', 'Afghanistan', 'Antigua and Barbuda', 'Anguilla', 'Albania',
                    'Armenia', 'Angola', 'Antarctica', 'Argentina', 'American Samoa', 'Austria', 'Australia', 'Aruba',
                    'Aland Islands', 'Azerbaijan', 'Bosnia and Herzegovina', 'Barbados', 'Bangladesh', 'Belgium',
                    'Burkina Faso', 'Bulgaria', 'Bahrain', 'Burundi', 'Benin', 'Saint Barthelemy', 'Bermuda', 'Brunei',
                    'Bolivia', 'Bonaire, Saint Eustatius and Saba ', 'Brazil', 'Bahamas', 'Bhutan', 'Bouvet Island',
                    'Botswana', 'Belarus', 'Belize', 'Canada', 'Cocos Islands', 'Democratic Republic of the Congo',
                    'Central African Republic', 'Republic of the Congo', 'Switzerland', 'Ivory Coast', 'Cook Islands',
                    'Chile', 'Cameroon', 'China', 'Colombia', 'Costa Rica', 'Cuba', 'Cape Verde', 'Curacao',
                    'Christmas Island', 'Cyprus', 'Czech Republic', 'Germany', 'Djibouti', 'Denmark', 'Dominica',
                    'Dominican Republic', 'Algeria', 'Ecuador', 'Estonia', 'Egypt', 'Western Sahara', 'Eritrea',
                    'Spain', 'Ethiopia', 'Finland', 'Fiji', 'Falkland Islands', 'Micronesia', 'Faroe Islands', 'France',
                    'Gabon', 'United Kingdom', 'Grenada', 'Georgia', 'French Guiana', 'Guernsey', 'Ghana', 'Gibraltar',
                    'Greenland', 'Gambia', 'Guinea', 'Guadeloupe', 'Equatorial Guinea', 'Greece',
                    'South Georgia and the South Sandwich Islands', 'Guatemala', 'Guam', 'Guinea-Bissau', 'Guyana',
                    'Hong Kong', 'Heard Island and McDonald Islands', 'Honduras', 'Croatia', 'Haiti', 'Hungary',
                    'Indonesia', 'Ireland', 'Israel', 'Isle of Man', 'India', 'British Indian Ocean Territory', 'Iraq',
                    'Iran', 'Iceland', 'Italy', 'Jersey', 'Jamaica', 'Jordan', 'Japan', 'Kenya', 'Kyrgyzstan',
                    'Cambodia', 'Kiribati', 'Comoros', 'Saint Kitts and Nevis', 'North Korea', 'South Korea', 'Kosovo',
                    'Kuwait', 'Cayman Islands', 'Kazakhstan', 'Laos', 'Lebanon', 'Saint Lucia', 'Liechtenstein',
                    'Sri Lanka', 'Liberia', 'Lesotho', 'Lithuania', 'Luxembourg', 'Latvia', 'Libya', 'Morocco',
                    'Monaco', 'Moldova', 'Montenegro', 'Saint Martin', 'Madagascar', 'Marshall Islands', 'Macedonia',
                    'Mali', 'Myanmar', 'Mongolia', 'Macao', 'Northern Mariana Islands', 'Martinique', 'Mauritania',
                    'Montserrat', 'Malta', 'Mauritius', 'Maldives', 'Malawi', 'Mexico', 'Malaysia', 'Mozambique',
                    'Namibia', 'New Caledonia', 'Niger', 'Norfolk Island', 'Nigeria', 'Nicaragua', 'Netherlands',
                    'Norway', 'Nepal', 'Nauru', 'Niue', 'New Zealand', 'Oman', 'Panama', 'Peru', 'French Polynesia',
                    'Papua New Guinea', 'Philippines', 'Pakistan', 'Poland', 'Saint Pierre and Miquelon', 'Pitcairn',
                    'Puerto Rico', 'Palestinian Territory', 'Portugal', 'Palau', 'Paraguay', 'Qatar', 'Reunion',
                    'Romania', 'Serbia', 'Russia', 'Rwanda', 'Saudi Arabia', 'Solomon Islands', 'Seychelles', 'Sudan',
                    'South Sudan', 'Sweden', 'Singapore', 'Saint Helena', 'Slovenia', 'Svalbard and Jan Mayen',
                    'Slovakia', 'Sierra Leone', 'San Marino', 'Senegal', 'Somalia', 'Suriname', 'Sao Tome and Principe',
                    'El Salvador', 'Sint Maarten', 'Syria', 'Swaziland', 'Turks and Caicos Islands', 'Chad',
                    'French Southern Territories', 'Togo', 'Thailand', 'Tajikistan', 'Tokelau', 'East Timor',
                    'Turkmenistan', 'Tunisia', 'Tonga', 'Turkey', 'Trinidad and Tobago', 'Tuvalu', 'Taiwan', 'Tanzania',
                    'Ukraine', 'Uganda', 'United States Minor Outlying Islands', 'United States', 'Uruguay',
                    'Uzbekistan', 'Vatican', 'Saint Vincent and the Grenadines', 'Venezuela', 'British Virgin Islands',
                    'U.S. Virgin Islands', 'Vietnam', 'Vanuatu', 'Wallis and Futuna', 'Samoa', 'Yemen', 'Mayotte',
                    'South Africa', 'Zambia', 'Zimbabwe', 'Serbia and Montenegro', 'Netherlands Antilles']
    return country_list


def get_continent_list():
    continent_list = ['AF', 'AS', 'EU', 'NA', 'OC', 'SA', 'AN']
    return continent_list


def get_city_list():
    p = "/Users/kervin/Desktop/code/npc_tv/consensus_node/server/server/gateways/data/data/Nominatim/assets/geonames-all-cities-with-a-population-1000.json"
    try:
        f = open(p)
        data = json.load(f)
        # returns JSON object as
        # a dictionary

        cities = [x["fields"]["name"] for x in data]
        return cities
    except FileNotFoundError:
        logger.error("File not found")
        return None

