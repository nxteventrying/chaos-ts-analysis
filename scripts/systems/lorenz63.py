def lorenz63(sigma, beta, rho, t, state):
    x, y, z = state
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x *  y - beta *z
    return [dx,dy,dz]

