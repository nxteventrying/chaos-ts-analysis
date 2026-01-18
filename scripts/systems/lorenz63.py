def lorenz63(sigma, beta, rho, t, state):
    x, y, z = state
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x *  y - beta *z
    return [dx,dy,dz]

# def lorenz_rhs(u, *, sigma, rho, beta):
#     x, y, z = u
#     x_dot = sigma * (y - x)
#     y_dot = x * (rho - z) - y
#     z_dot = x * y - beta * z
#     u_dot = np.array([x_dot, y_dot, z_dot])
#     return u_dot