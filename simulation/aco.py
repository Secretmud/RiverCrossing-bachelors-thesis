import lib.aco.Ant as ant
import lib.aco.Point as p
import lib.utils.plotting as plotter
import numpy as np
import random
import threading

g = lambda x, theta: np.tan(theta) - S(x)/(v*np.cos(theta))

n = 50
m = 50
D = 20
S = lambda x: 0.9*np.exp(-np.power(x-D/2, 4)/5000)
v = 1

surface = []
for i in range(m):
    tmp = [0]*n
    surface.append(tmp)
dx = D/n
dy = D/m
theta = [np.arctan(dy/dx),2*np.pi - np.arctan(dy/dx)]
j = 1

for y in range(m):
    i = 1
    for x in range(n):
        surface[y][x] = p.Point(x, y, i*dx, j*dy, v=S(i*dx), pheremone=1)
        i += 1
    j += 1


def neighbor(surface, x, y):
    neigh = {#0: surface[y-1][x] if y-1 >= 0 else None,
             1: surface[y-1][x+1] if y+1 < m and x+1 < n else None,
             #2: surface[y][x+1] if x+1 < n else None,
             3: surface[y+1][x+1] if y+1 < m and x+1 < n else None,
             #4: surface[y+1][x] if y+1 < m else None
            }
    return neigh

plot = plotter.Plotter()
plot.set_projection("2d")

a_start_x = 0
a_start_y = int(np.floor(m/2))
amount_of_ants = 80

coordinates = ['N', 'NE', 'E', 'SE', 'S']

ants = [ant.Ant(surface[a_start_y][a_start_x]) for i in range(amount_of_ants)]
f = 0
def generate_solution(ant):
    ant.new_path()
    curr = ant.get_current()
    while curr.x + 1 != n:
        neigh = neighbor(surface, curr.x, curr.y)
        next_step = []
        for key, val in neigh.items():
            if val is not None:
                if v > val.v:
                    next_step.append(val)
        pheremone = 0
        if (len(next_step) > 0):
            for ph in next_step:
                pheremone += ph.p
            nxt = random.random()
            potential_nodes = {}
            for k, v in x.items():
            if v is not None:
                potential_nodes[k] = v/pheremone

            potential_nodes = {k: v for k, v in sorted(potential_nodes.items(), key=lambda item: item[1])}

            prev_v = 0
            next_node = 0
            last_key = list(potential_nodes.keys())[-1]
            for k, v in potential_nodes.items():
                if prev_v <= nxt < v:
                    next_node = k
                    break
                if k == last_key:
                    next_node = k

                prev_v = v

            ant.add_path(next_step[next_node])
        else:
            break
        curr = ant.get_current()
    while curr.y != a_start_y:
        if curr.y < a_start_y:
            ant.add_path(surface[curr.y+1][curr.x])
        else:
            ant.add_path(surface[curr.y-1][curr.x])
        curr = ant.get_current()
        
        import random



rho = 0.9

def update_pheremones():
        for y in range(m):
            for x in range(n):
                tot_p = 0
                for ant in ants:
                    ant_path = ant.get()
                    for p in ant_path:
                        if y == p.y and x == p.x:
                            tot_p += p.p
                          
                surface[y][x].p = (1-rho)*surface[y][x].p + tot_p

while f < 1:
    threads = [threading.Thread(target=generate_solution, args=(ant,)) for ant in ants]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    update_pheremones()
    f += 1
    print(f"{f}/10")


for a in ants:
    a = a.get()
    X = []
    Y = []
    for i in a:
        X.append(i.dx)
        Y.append(i.dy)
    plot.plot_ant(X, Y)

plot.plot_show()
