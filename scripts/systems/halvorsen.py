def halvorsen(a, t, state):
    x, y, z = state
    dx = - a * x - 4 * y - 4 * z - y ** 2
    dy = - a * y - 4 * z - 4 * x - z ** 2 
    dz = - a * z - 4 * x - 4 * y - x ** 2
    return [dx,dy,dz]
