from lib.utils.plotting import Plotter
import numpy as np
from pathlib import Path

p = Path("sd/")
i = 0
files = {}
for file in p.iterdir():
    if file.is_file():
        files[i] = file
        i += 1
files[i] = "q"
p = Plotter()

sd = []
mean = []
print(f"Select a file:")
for k, v in files.items():
    print(f"\t{k}:\t{v}")

file = files[int(input())]
if file != "q":
    with open(file, "r") as f:
        sd = f.readline().split(",")
        mean = f.readline().split(",")

    print(f"{len(sd)}")
    p.set_projection("2d")
    x = []
    for i in range(len(sd)):
        x.append(i)

    import matplotlib.pyplot as plt

    x.reverse()

    plt.scatter(x, sd)
    #plt.errorbar(x, mean, sd, linestyle='None', marker='^')
    #plt.scatter(x, mean)
    plt.yscale("log")
    #plt.xscale("log")
    plt.xlabel("Generations")
    plt.ylabel("std")
    plt.show()
else:
    print(f"See you later o/!")