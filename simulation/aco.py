import lib.aco.Ant as ant
import lib.aco.Point as p
import lib.utils.plotting as plotter
import numpy as np
import random
import threading
import numba
import cProfile
g = lambda x, theta: np.tan(theta) - S(x)/(v*np.cos(theta))

n = 1280 
m = 720
D = 20
W = 20
smax = 1
S = lambda x: smax*np.exp(-np.power(x-D/2, 4)/5000)
v = 1

surface = []
for i in range(m):
    tmp = [0]*n
    surface.append(tmp)
dx = D/n
dy = W/m
theta = [
    np.arctan(dy/dx),
    2*np.pi - np.arctan(dy/dx)
]
j = 1

for y in range(m):
    i = 1
    for x in range(n):
        surface[y][x] = p.Point(x, y, i*dx, j*dy, pheremone=1)
        i += 1
    j += 1
# Pre recreation
"""
time = [
    lambda x: dy/(v-S(x)),
    lambda x: (1+(dy/dx)**2)*dx/(np.sqrt((1+(dy/dx)**2)*v**2-S(x+dx/2)**2)-dy/dx*S(x+dx/2)), # np.sqrt()
    lambda x: dx/np.sqrt(v**2-S(x+dx/2)**2), 
    lambda x: (1-(dy/dx)**2)*dx/(np.sqrt((1+(dy/dx)**2)*v**2-S(x+dx/2)**2)+(dy/dx)*S(x+dx/2)),
    lambda x: dy/(v+S(x))
]
"""

# New SE and NE functions
time = [
    lambda x, y: dy/(v-S(x)),
    lambda x, y: dx/v*(np.sqrt(1-(S(x+dx/2)/v)**2+(y/x)**2) - dy/dx*(S(x+dx/2)/v))/(1-(S(x+dx/2)/v)**2),
    lambda x, y: dx/np.sqrt(v**2-S(x+dx/2)**2), 
    lambda x, y: dx/v*(np.sqrt(1-(S(x+dx/2)/v)**2+(y/x)**2) + dy/dx*(S(x+dx/2)/v))/(1-(S(x+dx/2)/v)**2),
    lambda x, y: dy/(v+S(x))
]

def neighbor(surface, x, y):
    if v > S((x+1)*dx):
        neigh = {
                #0: surface[y + 1][x] if y + 1 < m else None,                       # North
                1: surface[y + 1][x + 1] if y + 1 < m and x + 1 < n else None,     # North East
                2: surface[y][x + 1] if x + 1 < n else None,                       # East
                3: surface[y - 1][x + 1] if y > 0 and x + 1 < n else None,         # South East
                #4: surface[y - 1][x] if y > 0 else None                            # South
        }
    else:
        neigh = {
                3: surface[y - 1][x + 1] if y > 0 and x + 1 < n else None,         # South East
                #4: surface[y - 1][x] if y > 0 else None                            # South
        }

    return neigh

plot = plotter.Plotter()
plot.set_projection("2d")

a_start_x = 0
a_start_y = int(np.floor(m/2)) 
amount_of_ants = 60

ants = [ant.Ant(surface[a_start_y][a_start_x]) for i in range(amount_of_ants)]
f = 0
def generate_solution(ant):
    ant.new_path()
    ant.time = 0
    curr = ant.get_current()
    while curr.x + 1 != n:
        neigh = neighbor(surface, curr.x, curr.y)
        pheremone = 0
        if (len(neigh) > 0):
            for k, val in neigh.items():
                if val is not None:
                    if neigh[k] not in ant.get():
                        pheremone += val.p
            nxt = random.random()
            potential_nodes = {}
            for k, val in neigh.items():
                if val is not None:
                    if neigh[k] not in ant.get():
                        potential_nodes[k] = val.p/pheremone
            

            potential_nodes = {k: val for k, val in sorted(potential_nodes.items(), key=lambda item: item[1])}

            #print(f"{potential_nodes}")

            prev_val = 0
            for k, val in potential_nodes.items():
                potential_nodes[k] = val + prev_val
                prev_val += val
            
            #print(f"{potential_nodes}")

            prev_v = 0
            next_node = 0
            last_key = list(potential_nodes.keys())[-1]
            for k, val in potential_nodes.items():
                if k == last_key:
                    next_node = k
                    break
                if prev_v <= nxt <= val:
                    next_node = k
                    break

                prev_v = val

            #print(f"{neigh} {next_node}")
            ant.add_path(neigh[next_node])
            neigh[next_node].visited = True
        else:
            break
        curr = ant.get_current()
        ant.time += time[next_node](curr.dx, curr.dy)
    edged = False
    k = 0
    while curr.y != a_start_y:
        if k == 0:
            edged = True
            ant.last_dy = curr.dy
            k += 1
        if curr.y < a_start_y:
            ant.add_path(surface[curr.y+1][curr.x])
            curr = ant.get_current()
            ant.time += time[0](curr.dx, curr.dy)
        else:
            ant.add_path(surface[curr.y-1][curr.x])
            curr = ant.get_current()
            ant.time += time[-1](curr.dx, curr.dy)
    
    ant.edged = edged


rho = 0.5
alpha = 0.1

"""
Update the pheremones for each point that has been hit by an ant. 
"""


def update_pheremones():
    pheremone = []
    for y in range(m):
        tmp = []
        for x in range(n):
            tmp.append(surface[y][x].p)
        pheremone.append(tmp)

    for ant in ants:
        for p in ant.get():
            pheremone[p.y][p.x] += 1/ant.time
    
    for y in range(m):
        for x in range(n):
            diff = neighbor(surface, surface[y][x].x, surface[y][x].y)
            tot_diff = 0
            for k, val in diff.items():
                if val is not None:
                    tot_diff += val.p
            surface[y][x].p = (rho)*(pheremone[y][x] + alpha*tot_diff)
iterations = 400
plotting = False
if plotting:
    plot.plot_ant_surface([0, D], [8, 12])
    plot.plot_ant([0, D], [a_start_y, a_start_y], clean=True)
from alive_progress import alive_bar

with alive_bar(iterations) as bar:
    for i in range(iterations):
        if i > 0 and plotting:
            plot.plot_ant_clear()
            plot.plot_ant_surface([0, D], [8, 12])

        p = [threading.Thread(target=generate_solution, args=(ant,)) for ant in ants]
        for t in p:
            t.start()
        for t in p:
            t.join()
        if plotting:
            for ant in ants:
                posx = []
                posy = []
                for a in ant.get():
                    posx.append(a.dx)
                    posy.append(a.dy)
                plot.plot_ant(posx, posy)
                plot.plot_pause(1/amount_of_ants)

        update_pheremones()
        bar()
"""
with alive_bar(iterations) as bar:
    for i in range(iterations):
        p = [threading.Thread(target=generate_solution, args=(ant,)) for ant in ants]
        for t in p:
            t.start()
        for t in p:
            t.join()
        update_pheremones()
        if i + 1 != iterations:
            for ant in ants:
                ant.time = 0
        bar()
        
"""


times = []

for a in ants:
    times.append(a.time)
    a = a.get()
    X = []
    Y = []
    for i in a:
        X.append(i.dx)
        Y.append(i.dy)
    plot.plot_ant_surface([0, D], [8, 12])
    plot.plot_ant(X, Y)

plot.plot_show()
print(sorted(times))