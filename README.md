# The-Ridiculously-Abnormally-Dumb-Enrichment-Refrigerator

### Installation

```sh
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

### How to run the program
1) Select an algorithm. i.e ```from signals.noobtheory import NoobTheory as AlgoSignals```
2) Select data source. ```market_data_client = MarketDataClient('data/stooq_hourly/wmt.us.txt', ticker)```
3) Ensure ```MarketDataClient``` is correctly loaded with source ```from market_data_client.stooq_client import MarketDataClient```
2) In project home directory, run ```python main.py $TICKER```,
    - in this example, it would be ```python main.py WMT```

### Version
0.0.1

### Authors
Winfield Tian
