import random
class Ant:

    def __init__(self, x, y, start_x, start_y):
        u = Utility()
        self.path = u.zeroes(x, y)
        self.add_path(start_x, start_y)

    def add_path(self, x, y):
        self.path[x][y] = Point(x, y)

    def get(self, x, y):
        return self.path[x][y]


class Point:

    def __init__(self, x, y, v=0, pheremone=0):
        self.x = x
        self.y = y
        self.v = v
        self.p = pheremone

    def __str__(self):
        return "[" + str(self.x) + "," + str(self.y) + "@" + str(self.v) + " " + str(self.p) + "]"

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
        x = self.zeroes(row, col)
        for i in range(row):
            for j in range(col):
                x[i][j] = Point(i, j, random.randrange(0, 5), 1)

        return x

class Simulation:
    
    def __init__(self, ant_amt):
        self.ant_amt = ant_amt

    def generate_solution(self, arr, ants):
        for ant in ants:
            for i in arr:
                for j in i:
                    ant.add_path(1, j.y)
                    print(ant.path[j.x][j.y], end=" ")

                print()

        return ants


class Calculation:

    def __init__(self, rho, c):
        self.rho = rho
        self.c = c

    def tau_k(self, p):
        return self.c/p.v

    def pheremone_update(self, arr, ants):
        tot_p = 0
        for i in ants:
            for j in arr:
                for y in j:
                    tmp = i.get(y.x, y.y)
                    #print(tmp)
                    #tot_p +=  self.tau_k(arr[tmp.x][tmp.y].v)


def main():
    c = Calculation(0.5, 1)
    u = Utility()
    s = Simulation(100)
    x = u.fill_cost(5, 5)
    ants = [Ant(5,5, 0, 1) for i in range(1)] 
    ants = s.generate_solution(x, ants)
    c.pheremone_update(x, ants)

main()
