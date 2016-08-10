"""simple moving average (SMA) based on the close tick data values"""

from __future__ import absolute_import

from sys import maxint
from models.stream_array import StreamArray

class StochasticOscillatorK(StreamArray):
    """class that contains the stochastics k"""

    def __init__(self, period=30, history_period=3):
        """initialize the Stochastics K. if no history_period is specified
           will default to recording the last 4 SMA ticks

        """

        StreamArray.__init__(self, history_period)
        self.period = period


    def calc(self, market_high, market_low, market_close):
        """calculates the stochastic k for the given period length"""
        if not market_high.saturated():
            return

        max_high, min_low = self.get_max_min(market_high, market_low)

        K = 100
        if max_high != min_low:
            K = (100 * (market_close.curr() - min_low)) / (max_high - min_low)
        self.push(K)

    def get_max_min(self, market_high, market_low):
        """helper function to calculate max_high and min_low"""

        max_high = 0
        min_low = maxint

        for i in range(self.period):
            high = market_high[i]
            low = market_low[i]

            if high > max_high:
                max_high = high
            if low < min_low:
                min_low = low

        return max_high, min_low
