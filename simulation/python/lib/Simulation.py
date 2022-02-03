
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


    def next_step(self, p):
        potential_new_steps = neighbor(p)


    
    def neighbor(self, p, arr):
        x, y = p.x, p.y
        pot = []
        
        if x > 0 and y > 0:
            return [[p.x-1, p.y-1],
                    [p.x, p.y-1],
                    [p.x+1, p.y-1],
                    [p.x-1,p.y],
                    [p.x+1,p.y],
                    [p.x-1,p.y+1],
                    [p.x,p.y+1],
                    [p.x,p.y+1]
                    ]
        elif x > 0:
            pass
        elif y > 0:
                pass
