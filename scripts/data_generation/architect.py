import numpy as np

# The main job is to make easier the scripting
# but also to control the chaotic behaviour
# like, it allows them to be a certain way

class Architect:
    """
    Here we'll decide like the global configuration
    for that we need the following:
    
    - parent model: f,(e.g lorenz63.py)
    - params wich come from blueprints (e.g lorenz63.jsom)
    - initial conditions: y0 = [x0,y0,z0]
    - t_span = (ti,tf)
    - t_eval = np.linspace(t_span[0],t_span[1],number of points in between)


    """
    def __init__(self, f,params, y0, t_span, t_eval):
    
        self.f = f
        self.params = params
        self.module = None
    
    def designer():

        pass