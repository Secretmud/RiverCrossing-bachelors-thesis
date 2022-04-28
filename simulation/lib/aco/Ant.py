class Ant:

    def __init__(self, p):
        self.pa = 0.2
        self.path = []
        self.l = 0
        self.add_path(p)
        self.time = 0
        self.edged = False
        self.last_dy = 0
        self.node = 0

    def add_path(self, p):
        self.path.append(p)

    def get(self):
        return self.path

    def get_current(self):
        return self.path[-1]

    def add_time(self, t):
        self.time += t

    def new_path(self):
        first = self.path[0]
        self.path.clear()
        self.path.append(first)