from lib.Point import *
from lib.Utility import *
from lib.Ant import *
from lib.Calculation import *
from lib.Simulation import *

def main():
    ant_amt = 1
    u = Utility()
    s = Simulation(ant_amt)
    c = Calculation(0.5, 1)
    x = u.fill_cost(3, 3)
    ants = [Ant(Point(0, 1)) for i in range(ant_amt)] 
    i = 0
    while i < 10:
        ants = s.generate_solution(x, ants)
        c.pheremone_update(x, ants)
        i += 1

if __name__ == "__main__":
    main()
