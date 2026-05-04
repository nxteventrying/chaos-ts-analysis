def dadras(a, b, c, d, e, t,state):
    x, y, z = state
    dx = y - a * x  + b * y * z
    dy = c * y - x * z + z
    dz = d * x * y - e * z
    return [dx,dy,dz]