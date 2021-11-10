

class Calculation:

    def __init__(self, rho, c):
        self.rho = rho
        self.c = c

        
    def tau_k(self, p):
        if p.v == 0:
            return 0
        return self.c/p.v

    
    def pheremone_update(self, arr, ants):
        tot_p = 0
        for j in arr:
            for y in j:
                for i in ants:
                    tot_p +=  self.tau_k(arr[y.x][y.y])
                    print(tot_p, end=" ")
                print()
