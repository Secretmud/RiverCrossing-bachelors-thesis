import lib.aco.Ant as ant
import lib.aco.Point as point
import lib.utils.plotting as plotter
import numpy as np
import random
import threading
from time import perf_counter
import operator
import statistics
from pathlib import Path
from subprocess import check_call

"""
This sections is made up of all the differenet variables this program use to run properly 
"""
folder = "fold"
version = 8
initialized_surface = False
iterations = 9000
plotting = True
std = False
"""
Below we have all the different variables that can be tweaked to change the potential outcome of the program
"""
n = 20
m = 10
amount_of_ants = n*m
rho = 0.6
alpha = 0
n_alpha = 1
n_beta = 0
elite = int(amount_of_ants/10)
D = 20
W = 5
v = 1
dx = D/(n-1)
dy = W/m
smax = 0.9
offset = 3
S = lambda x: smax*np.exp(-np.power(x-D/2, 4)/5000)

a_start_x = 0
a_start_y = 0


plot = plotter.Plotter()
plot.set_projection("2d")



time = [
    lambda x, y: dy/(v+S(x)),
    lambda x, y: dx/v*(np.sqrt(1-(S(x+dx/2)/v)**2+(dy/dx)**2) + dy/dx*(S(x+dx/2)/v))/(1-(S(x+dx/2)/v)**2),
    lambda x, y: dx/np.sqrt(v**2-S(x+dx/2)**2), 
    lambda x, y: dx/v*(np.sqrt(1-(S(x+dx/2)/v)**2+(dy/dx)**2) - dy/dx*(S(x+dx/2)/v))/(1-(S(x+dx/2)/v)**2),
    lambda x, y: dy/(v-S(x))
]

def neighbor(surface, x, y):
    if v > S((x+1)*dx):
        neigh = {
                #0: surface[y + 1][x] if y + 1 < m and surface[y + 1][x].p > 0 else None,                       # North
                1: surface[y + 1][x + 1] if y + 1 < m and x + 1 < n and surface[y + 1][x + 1].p > 0 else None,     # North East
                2: surface[y][x + 1] if x + 1 < n and surface[y][x + 1] .p > 0 else None,                       # East
                3: surface[y - 1][x + 1] if y > 0 and x + 1 < n and surface[y - 1][x + 1].p > 0  else None,         # South East
                #4: surface[y - 1][x] if y > 0 and surface[y - 1][x].p > 0 else None                            # South
        }
    else:
        neigh = {
                3: surface[y - 1][x + 1] if y > 0 and x + 1 < n and surface[y - 1][x + 1].p > 0 else None,         # South East
                #4: surface[y - 1][x] if y > 0 and surface[y - 1][x].p > 0 else None                            # South
        }

    return {key: val for key, val in neigh.items() if val is not None}
surface = []
for i in range(m):
    tmp = [0 for i in range(n)]
    surface.append(tmp)

def free_flow():
    global a_start_y
    j = 0
    for y in range(m):
        i = 0
        for x in range(n):
            c_dy = (-W/2)+j*dy
            surface[y][x] = point.Point(x, y, i*dx, c_dy, pheremone=1)
            if c_dy == 0:
                a_start_y = y

            i += 1
        j += 1
    

def force_flow(m,n,initialized_surface):
    global a_start_y
    j = 1
    if initialized_surface:
        for y in range(m):
            i = 0
            for x in range(n):
                c_dy = (-W/2)+j*dy
                c_dx = i*dx
                pheremone = 1
                if abs(c_dy) > D-c_dx:
                    pheremone = 0
                
                surface[y][x].p = pheremone
                if c_dy == 0:
                    a_start_y = y

                i += 1
            j += 1
    else:
        for y in range(m):
            i = 0
            for x in range(n):
                c_dy = (-W/2)+j*dy
                c_dx = i*dx
                pheremone = 1
                if abs(c_dy) > D-c_dx:
                    pheremone = 0
                
                surface[y][x] = point.Point(x, y, c_dx, c_dy, pheremone=pheremone)
                if c_dy == 0:
                    a_start_y = y

                i += 1
            j += 1

force_flow(m,n,initialized_surface)
#free_flow()

for s in surface:
    for p in s:
        print(f"{p.dx:.3f}", end=" ")
    print()
#exit()

for y in range(m):
    for x in range(n):
        if surface[y][x] is not None:
            surface[y][x].neigh = neighbor(surface, x, y)
ants = [ant.Ant(surface[a_start_y][a_start_x]) for i in range(amount_of_ants)]

initialized_surface = True

training_data = [amount_of_ants, rho, alpha, n_alpha, n_beta, elite, n, m, D, W, smax]
# New SE and NE functions

"""
generate_solution(ant) -> void
It saves the path the ant has taken inside of the ant object, using the point objects (These are the objects that hold infomation about a specific address in the 2d surface)

The first thing we need to do is set the ant time to 0, this is done for the simple reason that we need store the crossing time for each generation.

We need to know which possible neighboors we have aswell, this is stored inside the point objects, this is done to speed up the code. By doing it this way we only need to 
find the neighboors once. Which is done at the initialization of the surface matrix.

We then create a probability vector and a possible key vector (Used to get the next step using the neighbor dictionary).

We normalize the probability vector based on the sum of all the pheremones we test against.

Then you simply use numpy's random.choice function to get a properly tested discrete probability picker. 

If we dont hit the value of y that doesnt satisfy f(0) = f(D) = 0, we then force the ants to the correct location, this also goes for the x value, which can happen if we use a forced
flow. 
"""

def generate_solution(ant):
    ant.new_path()
    ant.time = 0
    curr = ant.get_current()
    while curr.x + 1 != n:
        neigh = curr.neigh
        pheremone = 0
        if (len(neigh) > 0):
            nxt = random.random()
            potential_nodes = []
            selection_probs = []
            for k, val in neigh.items():
                #dist = np.sqrt(np.power(val.dx - curr.dx, 2) + np.power(val.dy - curr.dy, 2))
                dist = time[k](val.dx, val.dy)
                selection_probs.append(np.power(val.p, n_alpha)*np.power(1/dist, n_beta))
                potential_nodes.append(k)
                pheremone += selection_probs[-1]
            
            next_node = 0
            for i in range(len(selection_probs)):
                selection_probs[i] /= pheremone
            next_node = potential_nodes[np.random.choice(len(potential_nodes), p=selection_probs)]
            ant.add_path(neigh[next_node])
            neigh[next_node].visited = True
        else:
            break
        curr = ant.get_current()
        ant.time += time[next_node](curr.dx, curr.dy)
        #τij=(1−φ)⋅τij+φ⋅τ0 local update
        #curr.p = (1-rho)*curr.p + rho*1
    while curr.y != a_start_y:
        key = 0
        if curr.y < a_start_y:
            if len(curr.neigh) == 1:
                key = 1
                ant.add_path(curr.neigh[1])
            else:
                key = 0
                ant.add_path(surface[curr.y+1][curr.x])
            curr = ant.get_current()
            ant.time += time[key](curr.dx, curr.dy)
        else:
            if len(curr.neigh) == 1:
                key = 3
                ant.add_path(curr.neigh[3])
            else:
                key = -1
                ant.add_path(surface[curr.y-1][curr.x])
            curr = ant.get_current()
            ant.time += time[key](curr.dx, curr.dy)


"""
Update the pheremones for each point that has been hit by an ant. 
"""


def update_pheremones(best_ants=ants):
    pheremone = []
    global alpha
    for i in range(m):
        tmp = [0 for i in range(n)]
        pheremone.append(tmp)

    for ant in best_ants:
        for p in ant.get():
            pheremone[p.y][p.x] += 1/ant.time
    
    for y in range(m):
        for x in range(n):
            if surface[y][x] is not None:
                diff = surface[y][x].neigh
                tot_diff = 0
                neighs = 1
                for k, val in diff.items():
                    tot_diff += val.p
                    neighs+=1
                surface[y][x].p = (1-rho)*surface[y][x].p+(pheremone[y][x] + alpha*tot_diff/neighs)
#if plotting:
#    plot.plot_ant_surface([0, D], [surface[a_start_y][a_start_x].dy-offset, surface[a_start_y][a_start_x].dy+offset])
i = 0
plot_save = 0
sd = []
mean = []

old_sum = 0
start = perf_counter()
while i < iterations:
    if plot_save >= 80:
        alpha = 0
    p = [threading.Thread(target=generate_solution, args=(ant,)) for ant in ants]
    for t in p:
        t.start()
    for t in p:
        t.join()
    times = {}
    for ant in ants:
        times[ant] = ant.time
    times = sorted(times.items(), key=operator.itemgetter(1))[:elite]
    best_ants = []
    times_ant = []
    f = 1
    for ant in ants:
        times_ant.append(ant.time)
    for k in times:
        k[0].time = f + k[0].time
        best_ants.append(k[0])
        f += 1
    
    times_ant.sort()
    diff = abs(old_sum - sum(times_ant))
    print(f"{times_ant[0]} {times_ant[-1]} {diff}", end="\r")
    sd.append(statistics.stdev(times_ant))
    mean.append(statistics.mean(times_ant))
    if diff < 10e-7:
        for val1, val2 in zip(ants, times_ant):
            val1.time = val2
        training_data.append(plot_save)
        break
    old_sum = sum(times_ant)
    update_pheremones(best_ants=best_ants)
    if plotting and i%1 == 0:
        if std:
            x = np.linspace(0, D, n)
            y = np.linspace(-offset, offset, m)
            z = np.zeros((m,n))
            for j in range(m):
                for i in range(n):
                    z[j][i] = surface[j][i].p
            plot.plot_scatter_std(x, y, z, plot_save)
        else:
            plot.plot_ant_clear()
            plot.plot_ant_surface([0, D], [surface[a_start_y][a_start_x].dy-offset, surface[a_start_y][a_start_x].dy+offset])
            for a in ants:
                times.append(a.time)
                a = a.get()
                X = []
                Y = []
                for path in a:
                    X.append(path.dx)
                    Y.append(path.dy)
                plot.plot_ant(X, Y)
                plot.plot_ant_surface([0, D], [surface[a_start_y][a_start_x].dy-offset, surface[a_start_y][a_start_x].dy+offset], plot_save)

        plot_save += 1
    i += 1

end = perf_counter() - start

times = []

for a in ants:
    times.append(a.time)
    a = a.get()
    X = []
    Y = []
    for i in a:
        X.append(i.dx)
        Y.append(i.dy)
    plot.plot_ant(X, Y)
    plot.plot_ant_surface([0, D], [surface[a_start_y][a_start_x].dy-offset, surface[a_start_y][a_start_x].dy+offset], f"part_3_crossing_{str(rho)}_{m}_{n}")

with open(f"sd/{rho}_{alpha}_{m}_{n}_size({len(sd)}).txt", "w+") as f:
    for s in sd:
        f.write(f"{s},")
    f.write("\n")
    for me in mean:
        f.write(f"{me},")

#plot.plot_show()
if plotting:
    path = Path(f"animation/")
    name = f"{times[0]}"

    if f"{name}.mp4" in path.iterdir():
        name += "(1)"
    np = Path(f"videos/{folder+str(version)}").mkdir(parents=True, exist_ok=True)
    check_call([f"./make_video.sh", f"{8}", f"{folder+str(version)}/{name}"])
    """
    for item in path.iterdir():
        if item.is_file():
            item.unlink()
    """

training_data.append(times[0])
training_data.append(end)

with open("training.csv", "a+") as f:
    f.write("\n")
    for data in training_data:
        f.write(f"{data},")
