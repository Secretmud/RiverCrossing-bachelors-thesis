import random
from lib.Point import *

class Utility:

    def __init__(self):
        self.i = 0

        
    def ones(self, row, col):
        x: double = [[1 for i in range(col)] for x in range(row)]  
        return x

    
    def zeroes(self, row, col):
        x: double = [[0 for i in range(col)] for x in range(row)]  
        return x

    
    def fill_cost(self, row, col):
        tmp = self.zeroes(row, col)
        for y in range(len(tmp)):
            c = random.uniform(0, random.uniform(0.01, 0.1))
            for x in range(len(tmp[y])):
                if x < len(tmp[y])/2:
                    tmp[y][x] = Point(y, x, c, 1)
                    tmp[y][len(tmp[y])-x-1] = Point(y, len(tmp[y])-x-1, c, 1)
                c = random.uniform(c, c+random.uniform(0, 2))

        return tmp
