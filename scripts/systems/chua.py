

def chua(alpha, beta,f,t,state):
    x, y, z = state
    dxdt = alpha * (y - x - f(x))
    dydt = x - y + z
    dzdt = -beta * y
    return [dxdt, dydt, dzdt]
