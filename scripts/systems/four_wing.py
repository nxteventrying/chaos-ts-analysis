def four_wing(a, b, c, t,state):
    x, y, z = state
    dx = a * x + y * z
    dy = b * x + c * y - x * z
    dz = -z - x * y
    return [dx,dy,dz]