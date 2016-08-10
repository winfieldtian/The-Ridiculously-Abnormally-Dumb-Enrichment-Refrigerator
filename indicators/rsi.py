"""simple moving average (SMA) based on the close tick data values"""

from __future__ import absolute_import

from models.stream_array import StreamArray

class RSI(StreamArray):
    """class that contains the simple moving average"""

    SATURATED_DATA_COUNT = 250

    def __init__(self,
                 market_open,
                 market_close,
                 period=14,
                 history_period=5):
        """initialize the RSI. if no history_period is specified
           will default to recording the last 4 SMA ticks

        """
        StreamArray.__init__(self, history_period)
        self.period = period
        self.average_gain, self.average_loss = self._init_average_gain_loss(
            market_open, market_close)
        self.push(self._calc_rsi())  # init the first RSI
        self.saturate_counter = 0

    def calc(self, market_open, market_close):
        """calculates the simple moving average
           for the first self.period values and
           appends to list
        """
        period = self.period
        diff = market_close.curr() - market_open.curr()
        if diff > 0:
            self.average_gain = (self.average_gain * (period-1) + (diff*100)) / period
            self.average_loss = (self.average_loss * (period-1)) / period
        elif diff < 0:
            self.average_loss = (self.average_loss * (period-1) + abs(diff*100)) / period
            self.average_gain = (self.average_gain * (period-1)) / period
        else:
            self.average_gain = (self.average_gain * (period-1)) / period
            self.average_loss = (self.average_loss * (period-1)) / period

        rsi = self._calc_rsi()
        self.push(rsi)

        # takes READY_DATA_POINTS to fully saturate the RSI
        self.saturate_counter = (self.saturate_counter + 1
                                 if self.saturate_counter < self.SATURATED_DATA_COUNT
                                 else self.SATURATED_DATA_COUNT)

    def _init_average_gain_loss(self, market_open, market_close):
        """the first init of average gain and average loss is the sum"""

        sum_gain = 0
        sum_loss = 0

        for i in range(self.period):
            diff = market_close[i] - market_open[i]
            if diff > 0:
                sum_gain += diff
            else:
                sum_loss += abs(diff)

        sum_gain /= self.period
        sum_loss /= self.period
        return sum_gain, sum_loss

    def _calc_rsi(self):
        rsi = None
        if self.average_gain == 0:
            rsi = 0
        elif self.average_loss == 0:
            rsi = 100
        else:
            rsi = 100 - (
                10000 / (
                    100 + ((100*self.average_gain)/self.average_loss)
                    )
                )
        return rsi

    def saturated(self):
        return self.saturate_counter == self.SATURATED_DATA_COUNT
