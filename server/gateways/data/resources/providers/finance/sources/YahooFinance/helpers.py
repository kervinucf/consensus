import requests
import re
from bs4 import BeautifulSoup
from server.gateways.data.resources.providers.finance.sources.YahooFinance.utils import Market


def YahooFinanceAPI(GAINERS=False, LOSERS=False, MOST_ACTIVE=False, CRYPTO=False, CURRENCY=False):

    if GAINERS:
        base = 'https://finance.yahoo.com/gainers'
        market = Market(STOCK=True)
    elif LOSERS:
        base = 'https://finance.yahoo.com/losers'
        market = Market(STOCK=True)
    elif MOST_ACTIVE:
        base = 'https://finance.yahoo.com/most-active'
        market = Market(STOCK=True)
    elif CRYPTO:
        base = 'https://finance.yahoo.com/cryptocurrencies'
        market = Market(CRYPTO=True)
    elif CURRENCY:
        base = 'https://finance.yahoo.com/currencies'
        market = Market(CURRENCY=True)

    offset = "/?offset=0&count=100"

    url = base + offset
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"}
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'html.parser')
    assets = soup.find_all('tr', attrs={"class": "simpTblRow"})
    for asset in assets:
        asset_info = asset.get_text(separator="@").split("@")
        if CRYPTO:
            market_cap = asset_info[6]
            avg_volume = None
            volume = asset_info[5]
        elif CURRENCY:
            volume = None
            market_cap = None
            avg_volume = None
        else:
            market_cap = asset_info[7]
            avg_volume = asset_info[6]
            volume = asset_info[5]
        try:
            percent_change = asset_info[4]
        except IndexError:
            percent_change = None

        market.add_asset(
            symbol=asset_info[0],
            name=asset_info[1],
            price=asset_info[2],
            change=asset_info[3],
            percent_change=percent_change,
            volume=volume,
            avg_volume=avg_volume,
            market_cap=market_cap,
        )
    return market
