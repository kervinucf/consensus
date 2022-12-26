from server.gateways.data.resources.providers.twtr.sources.Twitter.api.interface import TwitterInterface

from server.gateways.data.resources.providers.twtr.sources.Twitter.api.helpers.stream import filtered_stream
from server.gateways.data.resources.providers.twtr.sources.Twitter.api.helpers.tweets import lookup_tweets, search_tweets,\
    lookup_user_tweets, search_conversation
from server.gateways.data.resources.providers.twtr.sources.Twitter.api.helpers.spaces import lookup_spaces, search_spaces
from server.gateways.data.resources.providers.twtr.sources.Twitter.api.helpers.trends import search_trends_from
from server.gateways.data.resources.providers.twtr.sources.Twitter.api.helpers.stream_rules import get_rules, set_rules, delete_rules
from server.gateways.data.resources.providers.twtr.sources.Twitter.api.helpers.users import lookup_users


def mergeEntities(entityList, byID):
    mergedEntities = {}
    for entity in entityList:
        entityDict = entity.__dict__
        entityID = entityDict[byID]['id']
        mergedEntities[entityID] = entityDict
    return mergedEntities


# dictByID -> mergeEntities
def TwitterQuery(conversation_id=None, tweet_search=None, tweet_id_list=None, space_search=None, space_id=None,
                 user_tweets=None,
                 user_name=None, latest_trends_in=None, get_stream_rules=False,
                 rules_to_set=None, rules_to_delete=None, delete_all_rules=False, track_filtered_stream=False,
                 dictByID=False, max_results=10):

    # #######################################################################
    # todo: add user endpoint
    # #######################################################################
    if conversation_id:
        response = TwitterInterface(
            endpoint_creator=search_conversation, parameters=conversation_id, tweet_endpoint=True,
            num_results=max_results)

    if tweet_search:
        response = TwitterInterface(
            endpoint_creator=search_tweets, parameters=tweet_search, tweet_endpoint=True, num_results=max_results)

    if tweet_id_list:
        response = TwitterInterface(
            endpoint_creator=lookup_tweets, parameters=tweet_id_list, tweet_endpoint=True)

    if user_tweets:
        response = TwitterInterface(
            endpoint_creator=lookup_user_tweets, parameters=user_tweets, tweet_endpoint=True)

    if space_search:
        response = TwitterInterface(
            endpoint_creator=search_spaces, parameters=space_search, space_endpoint=True)

    if space_id:
        response = TwitterInterface(
            endpoint_creator=lookup_spaces, parameters=space_id, space_endpoint=True)

    if latest_trends_in:
        response = TwitterInterface(
            endpoint_creator=search_trends_from, parameters=find_woeID_for(place=latest_trends_in), trend_endpoint=True)

    if user_name:
        response = TwitterInterface(
            endpoint_creator=lookup_users, parameters=user_name, user_endpoint=True)
    if get_stream_rules:
        response = TwitterInterface(
            endpoint_creator=get_rules, rule_endpoint=True)

    if rules_to_set:
        response = TwitterInterface(
            endpoint_creator=set_rules, parameters=rules_to_set, rule_endpoint=True)
    if rules_to_delete:
        return TwitterInterface(
            endpoint_creator=delete_rules, parameters=rules_to_delete, rule_endpoint=True)
    if delete_all_rules:
        rules_to_delete = TwitterQuery(
            get_stream_rules=True).rules_found.keys()
        return TwitterInterface(rules_to_delete=list(rules_to_delete))

    if track_filtered_stream:
        # returning filtered stream function to be started when initialized
        return TwitterInterface(endpoint_creator=filtered_stream, parameters=track_filtered_stream, stream=True)

    if dictByID:
        return mergeEntities(response, byID=dictByID)
    else:
        return response
    # #######################################################################
    # #######################################################################


def find_woeID_for(place=None):

    try:
        if place:
            places = {'WORLDWIDE': 1, 'WINNIPEG': 2972, 'OTTAWA': 3369, 'QUEBEC': 3444, 'MONTREAL': 3534,
                      'TORONTO': 4118, 'EDMONTON': 8676, 'CALGARY': 8775, 'VANCOUVER': 9807, 'BIRMINGHAM': 2364559,
                      'BLACKPOOL': 12903, 'BOURNEMOUTH': 13383, 'BRIGHTON': 13911, 'BRISTOL': 13963, 'CARDIFF': 15127,
                      'COVENTRY': 17044, 'DERBY': 18114, 'EDINBURGH': 19344, 'GLASGOW': 21125, 'HULL': 25211,
                      'LEEDS': 26042, 'LEICESTER': 26062, 'LIVERPOOL': 26734, 'MANCHESTER': 28218,
                      'MIDDLESBROUGH': 28869, 'NEWCASTLE': 30079, 'NOTTINGHAM': 30720, 'PLYMOUTH': 32185,
                      'PORTSMOUTH': 32452, 'PRESTON': 32566, 'SHEFFIELD': 34503, 'STOKE-ON-TRENT': 36240,
                      'SWANSEA': 36758, 'LONDON': 44418, 'BELFAST': 44544, 'SANTO DOMINGO': 76456,
                      'GUATEMALA CITY': 83123, 'ACAPULCO': 110978, 'AGUASCALIENTES': 111579, 'CHIHUAHUA': 115958,
                      'MEXICO CITY': 116545, 'CIUDAD JUAREZ': 116556, 'NEZAHUALCÓYOTL': 116564, 'CULIACÁN': 117994,
                      'ECATEPEC DE MORELOS': 118466, 'GUADALAJARA': 124162, 'HERMOSILLO': 124785, 'LEÓN': 131068,
                      'MÉRIDA': 133327, 'MEXICALI': 133475, 'MONTERREY': 134047, 'MORELIA': 134091,
                      'NAUCALPAN DE JUÁREZ': 134395, 'PUEBLA': 137612, 'QUERÉTARO': 138045, 'SALTILLO': 141272,
                      'SAN LUIS POTOSÍ': 144265, 'TIJUANA': 149361, 'TOLUCA': 149769, 'ZAPOPAN': 151582,
                      'MENDOZA': 332471, 'SANTIAGO': 349859, 'CONCEPCION': 349860, 'VALPARAISO': 349861,
                      'BOGOTÁ': 368148, 'CALI': 368149, 'MEDELLÍN': 368150, 'BARRANQUILLA': 368151, 'QUITO': 375732,
                      'GUAYAQUIL': 375733, 'CARACAS': 395269, 'MARACAIBO': 395270, 'MARACAY': 395271,
                      'VALENCIA': 776688, 'BARCELONA': 753692, 'CIUDAD GUAYANA': 395275, 'TURMERO': 395277,
                      'LIMA': 418440, 'BRASÍLIA': 455819, 'BELÉM': 455820, 'BELO HORIZONTE': 455821, 'CURITIBA': 455822,
                      'PORTO ALEGRE': 455823, 'RECIFE': 455824, 'RIO DE JANEIRO': 455825, 'SALVADOR': 455826,
                      'SÃO PAULO': 455827, 'CAMPINAS': 455828, 'FORTALEZA': 455830, 'GOIÂNIA': 455831, 'MANAUS': 455833,
                      'SÃO LUÍS': 455834, 'GUARULHOS': 455867, 'CÓRDOBA': 466861, 'ROSARIO': 466862,
                      'BARQUISIMETO': 468382, 'MATURÍN': 468384, 'BUENOS AIRES': 468739, 'GDAŃSK': 493417,
                      'KRAKÓW': 502075, 'LODZ': 505120, 'POZNAŃ': 514048, 'WARSAW': 523920, 'WROCLAW': 526363,
                      'VIENNA': 551801, 'CORK': 560472, 'DUBLIN': 560743, 'GALWAY': 560912, 'BORDEAUX': 580778,
                      'LILLE': 608105, 'LYON': 609125, 'MARSEILLE': 610264, 'MONTPELLIER': 612977, 'NANTES': 613858,
                      'PARIS': 615702, 'RENNES': 619163, 'STRASBOURG': 627791, 'TOULOUSE': 628886, 'BERLIN': 638242,
                      'BREMEN': 641142, 'DORTMUND': 645458, 'DRESDEN': 645686, 'DUSSELDORF': 646099, 'ESSEN': 648820,
                      'FRANKFURT': 650272, 'HAMBURG': 656958, 'COLOGNE': 667931, 'LEIPZIG': 671072, 'MUNICH': 676757,
                      'STUTTGART': 698064, 'BOLOGNA': 711080, 'GENOA': 716085, 'MILAN': 718345, 'NAPLES': 719258,
                      'PALERMO': 719846, 'ROME': 721943, 'TURIN': 725003, 'DEN HAAG': 726874, 'AMSTERDAM': 727232,
                      'ROTTERDAM': 733075, 'UTRECHT': 734047, 'BILBAO': 754542, 'LAS PALMAS': 764814, 'MADRID': 766273,
                      'MALAGA': 766356, 'MURCIA': 768026, 'PALMA': 769293, 'SEVILLE': 774508, 'ZARAGOZA': 779063,
                      'GENEVA': 782538, 'LAUSANNE': 783058, 'ZURICH': 784794, 'BREST': 824382, 'GRODNO': 825848,
                      'GOMEL': 825978, 'MINSK': 834463, 'RIGA': 854823, 'BERGEN': 857105, 'OSLO': 862592,
                      'GOTHENBURG': 890869, 'STOCKHOLM': 906057, 'DNIPROPETROVSK': 918981, 'DONETSK': 919163,
                      'KHARKIV': 922137, 'KYIV': 924938, 'LVIV': 924943, 'ODESA': 929398, 'ZAPOROZHYE': 939628,
                      'ATHENS': 946738, 'THESSALONIKI': 963291, 'BEKASI': 1030077, 'DEPOK': 1032539,
                      'PEKANBARU': 1040779, 'SURABAYA': 1044316, 'MAKASSAR': 1046138, 'BANDUNG': 1047180,
                      'JAKARTA': 1047378, 'MEDAN': 1047908, 'PALEMBANG': 1048059, 'SEMARANG': 1048324,
                      'TANGERANG': 1048536, 'SINGAPORE': 23424948, 'PERTH': 1098081, 'ADELAIDE': 1099805,
                      'BRISBANE': 1100661, 'CANBERRA': 1100968, 'DARWIN': 1101597, 'MELBOURNE': 1103816,
                      'SYDNEY': 1105779, 'KITAKYUSHU': 1110809, 'SAITAMA': 1116753, 'CHIBA': 1117034,
                      'FUKUOKA': 1117099, 'HAMAMATSU': 1117155, 'HIROSHIMA': 1117227, 'KAWASAKI': 1117502,
                      'KOBE': 1117545, 'KUMAMOTO': 1117605, 'NAGOYA': 1117817, 'NIIGATA': 1117881,
                      'SAGAMIHARA': 1118072, 'SAPPORO': 1118108, 'SENDAI': 1118129, 'TAKAMATSU': 1118285,
                      'TOKYO': 1118370, 'YOKOHAMA': 1118550, 'GOYANG': 1130853, 'YONGIN': 1132094, 'ANSAN': 1132444,
                      'BUCHEON': 1132445, 'BUSAN': 1132447, 'CHANGWON': 1132449, 'DAEGU': 1132466, 'GWANGJU': 1132481,
                      'INCHEON': 1132496, 'SEONGNAM': 1132559, 'SUWON': 1132567, 'ULSAN': 1132578, 'SEOUL': 1132599,
                      'KAJANG': 1141268, 'IPOH': 1154679, 'JOHOR BAHRU': 1154698, 'KLANG': 1154726,
                      'KUALA LUMPUR': 1154781, 'CALOCAN': 1167715, 'MAKATI': 1180689, 'PASIG': 1187115,
                      'TAGUIG': 1195098, 'ANTIPOLO': 1198785, 'CAGAYAN DE ORO': 1199002, 'CEBU CITY': 1199079,
                      'DAVAO CITY': 1199136, 'MANILA': 1199477, 'QUEZON CITY': 1199682, 'ZAMBOANGA CITY': 1199980,
                      'BANGKOK': 1225448, 'HANOI': 1236594, 'HAI PHONG': 1236690, 'CAN THO': 1252351,
                      'DA NANG': 1252376, 'HO CHI MINH CITY': 1252431, 'ALGIERS': 1253079, 'ACCRA': 1326075,
                      'KUMASI': 1330595, 'BENIN CITY': 1387660, 'IBADAN': 1393672, 'KADUNA': 1396439, 'KANO': 1396803,
                      'LAGOS': 1398823, 'PORT HARCOURT': 1404447, 'GIZA': 1521643, 'CAIRO': 1521894,
                      'ALEXANDRIA': 1522006, 'MOMBASA': 1528335, 'NAIROBI': 1528488, 'DURBAN': 1580913,
                      'JOHANNESBURG': 1582504, 'PORT ELIZABETH': 1586614, 'PRETORIA': 1586638, 'SOWETO': 1587677,
                      'CAPE TOWN': 1591691, 'MEDINA': 1937801, 'DAMMAM': 1939574, 'RIYADH': 1939753, 'JEDDAH': 1939873,
                      'MECCA': 1939897, 'SHARJAH': 1940119, 'ABU DHABI': 1940330, 'DUBAI': 1940345, 'HAIFA': 1967449,
                      'TEL AVIV': 1968212, 'JERUSALEM': 1968222, 'AMMAN': 1968902, 'CHELYABINSK': 1997422,
                      'KHABAROVSK': 2018708, 'KRASNODAR': 2028717, 'KRASNOYARSK': 2029043, 'SAMARA': 2077746,
                      'VORONEZH': 2108210, 'YEKATERINBURG': 2112237, 'IRKUTSK': 2121040, 'KAZAN': 2121267,
                      'MOSCOW': 2122265, 'NIZHNY NOVGOROD': 2122471, 'NOVOSIBIRSK': 2122541, 'OMSK': 2122641,
                      'PERM': 2122814, 'ROSTOV-ON-DON': 2123177, 'SAINT PETERSBURG': 2123260, 'UFA': 2124045,
                      'VLADIVOSTOK': 2124288, 'VOLGOGRAD': 2124298, 'KARACHI': 2211096, 'LAHORE': 2211177,
                      'MULTAN': 2211269, 'RAWALPINDI': 2211387, 'FAISALABAD': 2211574, 'MUSCAT': 2268284,
                      'NAGPUR': 2282863, 'LUCKNOW': 2295377, 'KANPUR': 2295378, 'PATNA': 2295381, 'RANCHI': 2295383,
                      'KOLKATA': 2295386, 'SRINAGAR': 2295387, 'AMRITSAR': 2295388, 'JAIPUR': 2295401,
                      'AHMEDABAD': 2295402, 'RAJKOT': 2295404, 'SURAT': 2295405, 'BHOPAL': 2295407, 'INDORE': 2295408,
                      'THANE': 2295410, 'MUMBAI': 2295411, 'PUNE': 2295412, 'HYDERABAD': 2295414, 'BANGALORE': 2295420,
                      'CHENNAI': 2295424, 'MERSIN': 2323778, 'ADANA': 2343678, 'ANKARA': 2343732, 'ANTALYA': 2343733,
                      'BURSA': 2343843, 'DIYARBAKIR': 2343932, 'ESKIŞEHIR': 2343980, 'GAZIANTEP': 2343999,
                      'ISTANBUL': 2344116, 'IZMIR': 2344117, 'KAYSERI': 2344174, 'KONYA': 2344210, 'OKINAWA': 2345896,
                      'DAEJEON': 2345975, 'AUCKLAND': 2348079, 'ALBUQUERQUE': 2352824, 'ATLANTA': 2357024,
                      'AUSTIN': 2357536, 'BALTIMORE': 2358820, 'BATON ROUGE': 2359991, 'BOSTON': 2367105,
                      'CHARLOTTE': 2378426, 'CHICAGO': 2379574, 'CINCINNATI': 2380358, 'CLEVELAND': 2381475,
                      'COLORADO SPRINGS': 2383489, 'COLUMBUS': 2383660, 'DALLAS-FT. WORTH': 2388929, 'DENVER': 2391279,
                      'DETROIT': 2391585, 'EL PASO': 2397816, 'FRESNO': 2407517, 'GREENSBORO': 2414469,
                      'HARRISBURG': 2418046, 'ETHIOPIA': '', 'HONOLULU': 2423945, 'HOUSTON': 2424766,
                      'INDIANAPOLIS': 2427032, 'JACKSON': 2428184, 'JACKSONVILLE': 2428344, 'KANSAS CITY': 2430683,
                      'LAS VEGAS': 2436704, 'LONG BEACH': 2441472, 'LOS ANGELES': 2442047, 'LOUISVILLE': 2442327,
                      'MEMPHIS': 2449323, 'MESA': 2449808, 'MIAMI': 2450022, 'MILWAUKEE': 2451822,
                      'MINNEAPOLIS': 2452078, 'NASHVILLE': 2457170, 'NEW HAVEN': 2458410, 'NEW ORLEANS': 2458833,
                      'NEW YORK': 2459115, 'NORFOLK': 2460389, 'OKLAHOMA CITY': 2464592, 'OMAHA': 2465512,
                      'ORLANDO': 2466256, 'PHILADELPHIA': 2471217, 'PHOENIX': 2471390, 'PITTSBURGH': 2473224,
                      'PORTLAND': 2475687, 'PROVIDENCE': 2477058, 'RALEIGH': 2478307, 'RICHMOND': 2480894,
                      'SACRAMENTO': 2486340, 'ST. LOUIS': 2486982, 'SALT LAKE CITY': 2487610, 'SAN ANTONIO': 2487796,
                      'SAN DIEGO': 2487889, 'SAN FRANCISCO': 2487956, 'SAN JOSE': 2488042, 'SEATTLE': 2490383,
                      'TALLAHASSEE': 2503713, 'TAMPA': 2503863, 'TUCSON': 2508428, 'VIRGINIA BEACH': 2512636,
                      'WASHINGTON': 2514815, 'OSAKA': 15015370, 'KYOTO': 15015372, 'DELHI': 20070458,
                      'UNITED ARAB EMIRATES': 23424738, 'ALGERIA': 23424740, 'ARGENTINA': 23424747,
                      'AUSTRALIA': 23424748, 'AUSTRIA': 23424750, 'BAHRAIN': 23424753, 'BELGIUM': 23424757,
                      'BELARUS': 23424765, 'BRAZIL': 23424768, 'CANADA': 23424775, 'CHILE': 23424782,
                      'COLOMBIA': 23424787, 'DENMARK': 23424796, 'DOMINICAN REPUBLIC': 23424800, 'ECUADOR': 23424801,
                      'EGYPT': 23424802, 'IRELAND': 23424803, 'FRANCE': 23424819, 'GHANA': 23424824,
                      'GERMANY': 23424829, 'GREECE': 23424833, 'GUATEMALA': 23424834, 'INDONESIA': 23424846,
                      'INDIA': 23424848, 'ISRAEL': 23424852, 'ITALY': 23424853, 'JAPAN': 23424856, 'JORDAN': 23424860,
                      'KENYA': 23424863, 'KOREA': 23424868, 'KUWAIT': 23424870, 'LEBANON': 23424873, 'LATVIA': 23424874,
                      'OMAN': 23424898, 'MEXICO': 23424900, 'MALAYSIA': 23424901, 'NIGERIA': 23424908,
                      'NETHERLANDS': 23424909, 'NORWAY': 23424910, 'NEW ZEALAND': 23424916, 'PERU': 23424919,
                      'PAKISTAN': 23424922, 'POLAND': 23424923, 'PANAMA': 23424924, 'PORTUGAL': 23424925,
                      'QATAR': 23424930, 'PHILIPPINES': 23424934, 'PUERTO RICO': 23424935, 'RUSSIA': 23424936,
                      'SAUDI ARABIA': 23424938, 'SOUTH AFRICA': 23424942, 'SPAIN': 23424950, 'SWEDEN': 23424954,
                      'SWITZERLAND': 23424957, 'THAILAND': 23424960, 'TURKEY': 23424969, 'UNITED KINGDOM': 23424975,
                      'UKRAINE': 23424976, 'UNITED STATES': 23424977, 'VENEZUELA': 23424982, 'VIETNAM': 23424984,
                      'PETALING': 56013632, 'HULU LANGAT': 56013645, 'AHSA': 56120136, 'OKAYAMA': 90036018}
            place = place.upper()
            return places[place]
    except KeyError:
        return None
