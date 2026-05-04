def lorenz83(a, b, f, g, t,state):
    x, y, z = state
    dx = - a * x - y ** 2 - z ** 2 + a * f
    dy = - y  + x * y - b * x * z + g
    dz =  - z + b * x * y + x * z 
    return [dx,dy,dz]