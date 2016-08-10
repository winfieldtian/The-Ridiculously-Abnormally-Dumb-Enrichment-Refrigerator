"""holds each market data tick value in a stream array"""

from __future__ import absolute_import

from models.stream_array import StreamArray

class MarketDataStream(object):
    """class that contains the simple moving average"""

    def __init__(self, period):
        """initialize four stream arrays to the past 4 ticks"""

        self.open = StreamArray(period)
        self.high = StreamArray(period)
        self.low = StreamArray(period)
        self.close = StreamArray(period)


    def update(self, open_tick, high_tick, low_tick, close_tick):
        """update each stream array"""

        self.open.push(open_tick)
        self.high.push(high_tick)
        self.low.push(low_tick)
        self.close.push(close_tick)
