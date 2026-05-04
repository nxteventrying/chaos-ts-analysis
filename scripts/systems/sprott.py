def sprott(a, b, t,state):
    x, y, z = state
    dx = y + a * x * y + x * z
    dy = 1 - b * x **2 + y * z
    dz = x - x ** 2 - y ** 2
    return [dx,dy,dz]