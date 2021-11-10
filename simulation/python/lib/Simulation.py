
class Simulation:
    
    def __init__(self, ant_amt):
        self.ant_amt = ant_amt

        
    def generate_solution(self, arr, ants):
        current: int = 0
        while current != self.ant_amt:
            for i in arr:
                for j in i:
                    pass

            current += 1

        return ants

    
    def neighbor(self, arr, x, y):
        if x == 0:
            pass
