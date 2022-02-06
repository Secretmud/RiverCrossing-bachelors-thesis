class Ant:

    def __init__(self, p):
        self.pa = 0.2
        self.path = []
        self.add_path(p)

    def add_path(self, p):
        self.path.append(p)

    def get(self):
        return self.path

    def get_prev(self):
        return self.path[-1]
