from server.gateways.data.resources.providers.finance.sources.YahooFinance.interface import YahooFinanceProvider


class FinanceAggregator:

    yahoo_finance_provider = YahooFinanceProvider()

    def __init__(self, provider=None):
        self.gainers = False
        self.losers = False
        self.most_active = False
        self.crypto = False
        self.currency = False

    def get_markets(self, market=None, detail=None):
        if market == "CRYPTO":
            self.crypto = True
        elif market == "CURRENCY":
            self.currency = True

        if detail == "OVERVIEW":
            pass
        elif detail == "GAINERS":
            self.gainers = True
        elif detail == "LOSERS":
            self.losers = True
        elif detail == "MOST_ACTIVE":
            self.most_active = True

        markets = self.yahoo_finance_provider.search_market(
            gainers=self.gainers, losers=self.losers, most_active=self.most_active,
            crypto=self.crypto, currency=self.currency)

        return vars(markets)
