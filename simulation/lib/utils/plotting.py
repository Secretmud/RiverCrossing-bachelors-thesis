import matplotlib.pyplot as plt

def plot_single(x, y, x1=None, y1=None):
    plt.plot(x, y)
    if (x1 != None or y1 != None):
        plt.plot(x1, y1, "r+")
    plt.plot([0,20], [0, 0], "r--")
    plt.xlabel("X-akse")
    plt.ylabel("Y-akse")
    plt.show()