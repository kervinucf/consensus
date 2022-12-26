from collections import OrderedDict
from operator import getitem


def convert_to_seconds(minutes=None, hours=None, days=None, weeks=None, months=None, years=None):
    if minutes:
        return minutes * 60
    if hours:
        return hours * 3600
    if days:
        return days * 86400
    if weeks:
        return weeks * 604800
    if months:
        return months * 2592000
    if years:
        return years * 31536000


class Market:
    def __init__(self, CRYPTO=False, CURRENCY=False, STOCK=False):
        self.market = {}

    def top_ten(self):
        return list(OrderedDict(sorted(self.market.items(), key=lambda x: getitem(x[1], 'price'))).keys())[:10]

    def bottom_ten(self):
        return list(OrderedDict(sorted(self.market.items(), key=lambda x: getitem(x[1], 'price'), reverse=True)).keys())[:10]

    def add_asset(self, symbol, name, price, change, percent_change, volume, avg_volume, market_cap):
        self.market[symbol] = {
            'name': name,
            'price': price,
            'change': change,
            'percent_change': percent_change,
            'volume': volume,
            'avg_volume': avg_volume,
            'market_cap': market_cap,
        }
