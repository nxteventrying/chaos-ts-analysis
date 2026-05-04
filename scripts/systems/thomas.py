import numpy as np
def thomas(b, t,state):
    x, y, z = state
    dx = np.sin(y) - b * x 
    dy = np.sin(z) - b * y
    dz = np.sin(x) - b * z
    return [dx,dy,dz]
