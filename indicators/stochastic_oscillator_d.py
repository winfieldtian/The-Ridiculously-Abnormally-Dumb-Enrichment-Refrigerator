"""simple moving average (SMA) based on the close tick data values"""

from __future__ import absolute_import

from models.stream_array import StreamArray

class StochasticOscillatorD(StreamArray):
    """class that contains the stochastics d
       which is the moving average of k
    """

    def __init__(self, period=3, history_period=3):
        """initialize the Stochastics D. if no history_period is specified
           will default to recording the last 3 SMA ticks

        """

        StreamArray.__init__(self, history_period)
        self.period = period


    def calc(self, stochastics_k):
        """calculates the stochastic d for the given period length"""
        if not stochastics_k.saturated():
            return

        period = self.period
        if len(stochastics_k) < period:
            raise RuntimeError('not enough stochastic_k values man!')

        D = 0
        for i in range(period):
            D += stochastics_k[i]
        D /= period

        self.push(D)
