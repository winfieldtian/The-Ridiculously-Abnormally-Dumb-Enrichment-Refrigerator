"""instantiates and reads market data from a source"""

from __future__ import absolute_import

import os

from utils import (
    convert_string_to_cents
)

class MarketDataClient(object):
    """class that contains the market data function"""

    def __init__(self, data_path, ticker):
        file_dir = os.path.dirname(os.path.realpath('__file__'))
        filename = os.path.join(file_dir, data_path)
        self.data = open(filename)
        self.ticker = ticker

    def get_tick_data(self):
        """returns a raw data line"""

        return self.data.readline()

    def get_parsed_tick_data(self):
        """returns a dict of parsed data"""

        data = self.data.readline().split(',')
        return {
            'date': data[0],
            'time': data[1],
            'open': convert_string_to_cents(data[2]),
            'high': convert_string_to_cents(data[3]),
            'low': convert_string_to_cents(data[4]),
            'close': convert_string_to_cents(data[5]),
            'volume': data[6].rstrip(),  # rstrip removes \n
        }
