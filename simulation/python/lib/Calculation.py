import math

class Calculation:

    def __init__(self, rho, c):
        self.rho = rho
        self.c = c

        
    def tau_k(self, p, i):
        pos = i.get_prev()
        pheremone = abs(math.sqrt((p.x - pos.x)**2 + (p.y - pos.y)**2))
        if pheremone == 0:
            return 0
        return self.c/abs(math.sqrt((p.x - pos.x)**2 + (p.y - pos.y)**2))

    
    def pheremone_update(self, arr, ants):
        for j in arr:
            for y in j:
                tot_p = 0
                ant_x = 0
                for i in ants:
                    tmp = i.get()
                    tot_p += self.tau_k(arr[y.x][y.y], i)
                    print (f"Ant: {ant_x}, tot_p: {tot_p}, x: {y.x}, y: {y.y}", end=" ")
                    ant_x += 1
                arr[y.x][y.y].p = (1-self.rho)*arr[y.x][y.y].p + tot_p
                print(arr[y.x][y.y].p)



