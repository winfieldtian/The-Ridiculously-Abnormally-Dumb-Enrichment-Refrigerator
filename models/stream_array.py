"""fixed array size that is optimized for O(1) pushes to the array
    while removing the oldest value. Most recent value is stored in
    0th index
"""

from __future__ import absolute_import

class StreamArray(object):
    """rotating array class"""

    def __init__(self, length):
        self.length = length
        self.head = length
        self.data = [None] * length

    def __getitem__(self, index):
        if index >= self.length:
            raise IndexError('index out of bounds, dumbass')

        real_index = (self.head + index) % self.length
        res = self.data[real_index]
        if res is None:
            raise ValueError('why are you so eager, this isnt initailized yet')
        return res

    def __len__(self):
        return self.length

    def __str__(self):
        return str(self.get())

    def __max__(self):
        return max(self.data)

    def __min__(self):
        return min(self.data)

    def push(self, value):
        """appends a new value to the list"""
        self.head = (self.head - 1) % self.length
        self.data[self.head] = value

    def get(self):
        """prints entire data to console"""
        length = self.length
        readable_array = [None] * length
        index = self.head

        for i in range(length):
            val = self.data[index]
            readable_array[i] = val
            index = (index + 1) % length

        return readable_array

    def curr(self):
        """returns the most recent stream data (like a peak)"""
        return self.data[self.head]

    def saturated(self):
        """validates whether the array is fully populated"""
        if None in self.data:
            return False
        else:
            return True
