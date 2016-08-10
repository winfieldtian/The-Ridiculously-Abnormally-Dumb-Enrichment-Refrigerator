
from __future__ import absolute_import

class StoichRSI(object):
    def __init__(self):
        self.has_bought = False

    def buy(self, portfolio, ticker, price, rsi, stochk, stochd):
        make_transaction = False
        if (
                rsi[0] < 40 and
                stochk[1] < stochd[1] and
                stochk[0] > stochd[0] and
                stochk[0] < 30
            ):
            make_transaction = True
            print "I would've bought at {}".format(price)

        if self.has_bought:
            make_transaction = False
        else:
            if make_transaction:
                self.has_bought = True

        amount = portfolio.cash / price - 1
        return {
            'make_transaction': make_transaction,
            'amount': amount,
            'price': price
        }

    def sell(self, portfolio, ticker, price, rsi, stochk, stochd):
        make_transaction = False
        if (
                rsi[0] > 70 and
                stochk[1] > stochd[1] and
                stochk[0] < stochd[0] and
                stochk[0] > 70
            ):
            make_transaction = True
            print "I would've sold at {}".format(price)

        if self.has_bought:
            if make_transaction:
                self.has_bought = False
        else:
            make_transaction = False

        amount = portfolio.assets[ticker].get('amount', 0)

        return {
            'make_transaction': make_transaction,
            'amount': amount,
            'price': price,
        }

    def other_signal(self):
        return "its high noon"
