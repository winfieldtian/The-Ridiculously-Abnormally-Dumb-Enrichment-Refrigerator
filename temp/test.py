#pylint: skip-file

"""primary script to run to test algorithmic program
to run, do `python main.py` in this directory
"""

from __future__ import absolute_import

from indicators.simple_moving_average import SimpleMovingAverage
from models.stream_array import StreamArray

a = SimpleMovingAverage(3)
b = [100,0,50,100,0,33]
a.calc(b)
print a
print a[0]
c = StreamArray(5)
c.push(1)
c.push(2)
c.push(3)
c.push(4)
print max(c)
