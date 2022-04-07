import numpy as np

class Point:

    def __init__(self, x, y, dx, dy, pheremone=1):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.p = pheremone
        self.visited = False
        

    def __str__(self):
        return f"[{self.x=} {self.y=} {self.dx=} {self.dy=} {self.v=:.4f} {self.p=}]"