import numpy as np


class DaqQueue:
    def __init__(self, size):
        self.dim = tuple(size)
        self.length = self.dim[0]
        self.data = np.empty(size)
        self.count = 0

    def add_data(self, data):
        if not self.check_data(data):
            print("Check data dimension!")
            return 0
        n = data.shape[0]
        if n >= self.length:
            self.data = data[-self.length:, ...]
        else:
            ram = self.length - n
            self.data[0:ram, ...] = self.data[-ram:, ...]
            self.data[ram:, ...] = data
        self.count += n
        return 1

    def check_data(self, data):
        data_shape = data.shape
        # print(data_shape, self.dim)
        return data_shape[1:] == self.dim[1:]

    def get_data(self):
        if self.count < self.length:
            return self.data[-self.count:, ...]
        else:
            return self.data

    def get_count(self):
        return self.count

    def get_length(self):
        if self.count < self.length:
            return self.count
        else:
            return self.length
