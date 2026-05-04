# def summon(parent_model):
#     module = importlib.import_module(parent_model)
#     func = getattr(module, parent_model)
#     return func
# def fixed_function(params):
#     func = summon(parent_model)
#     fixed_function = partial(func, *params)
#     return fixed_function
# def solve_ivp(fixed_function, t_span, y0, method='RK45', t_eval=None):
#     sol = solve_ivp(fixed_function, t_span, y0, method=method, t_eval=t_eval)
# def csv_saver(filename):
#     df = pd.DataFrame({'x': sol.y[0], 'y': sol.y[1], 'z': sol.y[2]})
#     df.to_csv(filename, index=False)




from scipy.integrate import solve_ivp
import importlib
from functools import partial
import pandas as pd



def df_in_one(module_name, function_name, params, t_span, y0, method='RK45', t_eval=None):
    # Import module dynamically
    module = importlib.import_module(module_name)

    # Get function dynamically
    func = getattr(module, function_name)

    # Apply parameters using functools.partial
    fixed_function = partial(func, *params)

    # Solve the differential equation
    sol = solve_ivp(fixed_function, t_span, y0, method=method, t_eval=t_eval)

    # Save results to CSV
    df = pd.DataFrame({'x': sol.y[0], 'y': sol.y[1], 'z': sol.y[2]})
    #df.to_csv(filename, index=False)

    return df  # Return solution in case further analysis is needed