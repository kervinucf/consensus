from server.gateways.data.resources.providers.finance.sources.YahooFinance.helpers import YahooFinanceAPI


class YahooFinanceProvider:

    def __init__(self):
        pass

    @staticmethod
    def search_market(gainers=False, losers=False, most_active=False, crypto=False, currency=False):
        if gainers:
            return YahooFinanceAPI(GAINERS=True)
        elif losers:
            return YahooFinanceAPI(LOSERS=True)
        elif most_active:
            return YahooFinanceAPI(MOST_ACTIVE=True)
        elif crypto:
            return YahooFinanceAPI(CRYPTO=True)
        elif currency:
            return YahooFinanceAPI(CURRENCY=True)
