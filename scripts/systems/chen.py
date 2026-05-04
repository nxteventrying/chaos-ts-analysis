def chen(alpha, beta, delta, t,state):
    x, y, z = state
    dx = alpha * x - y * z
    dy = beta * y + x * z
    dz = delta * z + (x * y)/3
    return [dx,dy,dz]