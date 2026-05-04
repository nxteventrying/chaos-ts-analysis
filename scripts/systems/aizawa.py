def aizawa(a, b, c, d, e, f, t,state):
    x, y, z = state
    dx = (z - b) * x - d * y
    dy = d * x + (z - b) * y
    dz = c + a * z - (z**3)/3 - (x ** 2 + y ** 2) * (1 + e *z) + f * z * x **3
    return [dx,dy,dz]