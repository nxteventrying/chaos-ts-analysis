def rossler(a,b,c, t,state):
    x, y, z = state
    dx = - y - z
    dy = x + a * y
    dz = b + z * (x - c)
    return [dx,dy,dz]