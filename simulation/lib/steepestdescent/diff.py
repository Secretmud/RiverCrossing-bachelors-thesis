import numpy as np

def lr(x, xp, gx, gxp):
    return np.abs((x - xp) * (gx - gxp))/ np.abs(np.power(gx - gxp), 2)

def next_step(x, lr, gx):
    return x - lr*gx

