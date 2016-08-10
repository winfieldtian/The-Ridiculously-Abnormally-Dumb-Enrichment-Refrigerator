"""simple moving average (SMA) based on the close tick data values"""

from __future__ import absolute_import

from models.stream_array import StreamArray

class SimpleMovingAverage(StreamArray):
    """class that contains the simple moving average"""

    def __init__(self, period=20, history_period=5):
        """initialize the SMA. if no history_period is specified
           will default to recording the last 4 SMA ticks

        """
        StreamArray.__init__(self, history_period)
        self.period = period


    def calc(self, market_data):
        """calculates the simple moving average
           for the first self.period values and
           appends to list
        """
        if not market_data.saturated():
            return

        period = self.period
        if len(market_data) < period:
            raise RuntimeError('not enough market values man!')

        sma = 0
        for i in range(period):
            sma += market_data[i]
        sma /= period

        self.push(sma)
