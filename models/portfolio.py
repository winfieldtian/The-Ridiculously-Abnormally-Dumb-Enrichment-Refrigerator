"""simple moving average (SMA) based on the close tick data values"""

from __future__ import absolute_import

from utils import (
    compute_broker_fee
)

class Portfolio(object):
    """class that contains the portfolio"""

    def __init__(self, tickers, starting_cash=1000000):
        self.cash = starting_cash
        self.assets = {}
        for ticker in tickers:
            self.assets[ticker] = {}
        # assets model is 'ticker': {'num_stocks', 'price_bought'}


    def purchase(self, ticker, amount, price):
        cost_value = amount * price
        broker_fee = compute_broker_fee(amount, price)

        purchase_cost = cost_value + broker_fee
        # if cash < purchase_cost:
        #    raise RuntimeError('cannot buy, not enough cash homie')

        # if we dont have enough cash to purchase the stocks, we'll buy one less stock
        while self.cash < broker_fee:
            amount -= 1

            cost_value = amount * price
            broker_fee = compute_broker_fee(amount, price)

            purchase_cost = cost_value + broker_fee

        self.cash -= purchase_cost
        self.assets[ticker] = {'amount': amount, 'price': price}

    def sale(self, ticker, amount, price):
        yield_value = amount * price
        broker_fee = compute_broker_fee(amount, price)
        sale_yield = yield_value - broker_fee
        # if we dont have enough cash to rebuy our purchase, we'll sell one less stock
        while self.cash < broker_fee:
            amount -= 1

            yield_value = amount * price
            broker_fee = compute_broker_fee(amount, price)

            sale_yield = yield_value - broker_fee

        self.cash += sale_yield
        self.assets[ticker] = {}

    def get_value(self, **ticker_price):
        """ticker_close contains a dict of the current ticker and the market_data price
           ticker_data model is {'ticker': 'price'}
        """

        value = self.cash
        for ticker in self.assets:
            value += ticker_price[ticker] * self.assets[ticker].get('amount', 0)

        return value
