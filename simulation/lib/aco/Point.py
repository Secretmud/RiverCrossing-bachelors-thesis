
class Point:

    def __init__(self, x, y, v=0, pheremone=1):
        self.x = x
        self.y = y
        self.v = v
        self.p = pheremone

        
    def __str__(self):
        return "[" + str(self.x) + "," + str(self.y) + "@" + str(self.v) + " " + str(self.p) + "]"
