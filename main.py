"""primary script to run to test algorithmic program
to run, do `python main.py` in this directory
"""

from __future__ import absolute_import

import sys

from market_data_client.stooq_client import MarketDataClient
from models.market_data_stream import MarketDataStream
from models.portfolio import Portfolio
from signals.noobtheory import NoobTheory as AlgoSignals
#from signals.stoich_rsi import StoichRSI as AlgoSignals

from indicators.simple_moving_average import SimpleMovingAverage
from indicators.stochastic_oscillator_k import StochasticOscillatorK
from indicators.stochastic_oscillator_d import StochasticOscillatorD
from indicators.rsi import RSI

STREAM_PERIOD = 50
WARMUP_DATA_COUNT = STREAM_PERIOD

def main(ticker):
    """engine to run script"""

    TIME_DEBUG = 0
    MAX_ITER_DEBUG = 1000
    CONTROL_BOUGHT = None
    CONTROL_SALE = None
    CONTROL_BEGIN = None
    CONTROL_END = None

    market_data_client = MarketDataClient('data/stooq_hourly/wmt.us.txt', ticker)
    market_data_stream = MarketDataStream(STREAM_PERIOD)
    portfolio = Portfolio([ticker])
    decision_client = AlgoSignals()

    try:
        for _ in range(WARMUP_DATA_COUNT):
            # saturate the stream
            tick_data = market_data_client.get_parsed_tick_data()
            market_data_stream.update(
                tick_data['open'],
                tick_data['high'],
                tick_data['low'],
                tick_data['close'])
            CONTROL_BEGIN = tick_data['date']
            CONTROL_BOUGHT = tick_data['open']

        sma = SimpleMovingAverage()
        stochk = StochasticOscillatorK()
        stochd = StochasticOscillatorD()
        stochdslow = StochasticOscillatorD()
        rsi = RSI(market_data_stream.open, market_data_stream.close)

        while True:
            tick_data = market_data_client.get_parsed_tick_data()
            market_data_stream.update(
                tick_data['open'],
                tick_data['high'],
                tick_data['low'],
                tick_data['close'])

            sma.calc(market_data_stream.close)
            stochk.calc(market_data_stream.high, market_data_stream.low, market_data_stream.close)
            stochd.calc(stochk)
            stochdslow.calc(stochd)
            rsi.calc(market_data_stream.open, market_data_stream.close)

            if (
                    sma.saturated() and
                    stochk.saturated() and
                    stochd.saturated() and
                    rsi.saturated()
                ):
                # ASSET TRANSACTION LOGIC, THIS CUSTOM LOGIC ENSURES
                # THAT BUYING AND SELLING CANNOT HAPPEN AT THE SAME TIME
                # this is changeable
                decision = decision_client.buy(
                    portfolio,
                    market_data_client.ticker,
                    market_data_stream.close.curr(),
                    rsi,
                    stochk,
                    stochd)

                TIME_DEBUG += 1
                MAX_ITER_DEBUG -= 1

                if decision['make_transaction']:
                    print 'Buying {} at {} after {} ticks'.format(
                        decision['amount'], decision['price'], TIME_DEBUG)
                    TIME_DEBUG = 0
                    print portfolio.cash
                    print sma
                    print stochk
                    print stochd
                    print stochdslow
                    print rsi
                    portfolio.purchase(
                        market_data_client.ticker, decision['amount'], decision['price'])
                    #input('Press enter to continue: ')
                    continue
                decision = decision_client.sell(
                    portfolio,
                    market_data_client.ticker,
                    market_data_stream.close.curr(),
                    rsi,
                    stochk,
                    stochd)

                if decision['make_transaction']:
                    print 'Selling {} at {} after {} ticks'.format(
                        decision['amount'], decision['price'], TIME_DEBUG)
                    portfolio.sale(ticker, decision['amount'], decision['price'])
                    print 'cash at hand: {}'.format(portfolio.cash)
                    TIME_DEBUG = 0
                    #input('Press enter to continue: ')

                if portfolio.cash < 0:
                    raise Exception('wtf, you really messed up')

                if MAX_ITER_DEBUG < 0:
                    CONTROL_END = tick_data['date']
                    raise IndexError('normal')

                CONTROL_SALE = tick_data['close']

    except IndexError:
        # terrible hack to know when we reach end of file
        print 'BOUGHT AT {}, SOLD AT {}'.format(CONTROL_BOUGHT, CONTROL_SALE)
        print 'from {} to {}'.format(CONTROL_BEGIN, CONTROL_END)

if __name__ == "__main__":
    main(sys.argv[1])
