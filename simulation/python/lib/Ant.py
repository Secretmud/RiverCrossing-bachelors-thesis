
class Ant:

    def __init__(self, p):
        self.path = []
        self.add_path(p)

    def add_path(self, p):
        self.path.append(p)

    def get(self):
        return self.path
