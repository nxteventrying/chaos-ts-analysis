def ravinoch_fabrikant(alpha, gamma, t,state):
    x, y, z = state
    dx = y * (z - 1 + x **  2) + gamma * x
    dy = x * (3 * z + 1 - x ** 2)
    dz = - 2 * z * (alpha + x * y )
    return [dx,dy,dz]