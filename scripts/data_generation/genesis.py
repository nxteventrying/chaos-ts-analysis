# import numpy as np
# from data_generation.tsdg import Sistema as sys
# from data_generation.binder import Binder 

# # Parameters
# sigma_val = 10.0
# beta_val = 8.0 / 3.0
# rho_val = 28.0
# params = (sigma_val, beta_val, rho_val)
# # Use Binder to fix parameters
# binder = Binder("systems.lorenz63", "lorenz63", params)
# binder.import_module()
# lorenz_fixed = binder.fixer()  # Now this is a partially applied function

# # Time range
# t = np.linspace(0, 105, 735)

# # Initial conditions
# y0 = [1.0, 1.0, 1.0]

# # Solve the system
# edo = sys(lorenz_fixed, y0=y0, t=t, metodo="RK45")
# edo.resolver()
# edo.graficar(tipo='series', guardar=False, show_plot=True)


# import numpy as np
# from utils.helpers import load_config
# from utils.helpers import sys_params_gen as params_gen
# from utils.helpers import initial_conditions_gen as ic_gen
# from data_generation.binder import Binder  
# from data_generation.tsdg import Sistema  
# from tqdm import tqdm

# # Ask for configuration file, or make one
# config_data = load_config()

# # Extract the variables we need from the config
# test_number = config_data["test_number"]
# parent_model = config_data["parent_model"]  
# number_of_child_systems = config_data["number_of_child_systems"]  
# params = config_data["params"]
# initial_conditions = config_data["initial_conditions"]  
# t_span = config_data["t_span"]  
# num_points = config_data["num_points"]  

# # Parameters for each system
# systems_params_dict = params_gen(params, number_of_child_systems)
# # Initial conditions for each system
# systems_initial_dict = ic_gen(initial_conditions, number_of_child_systems)

# # Set time span for solving
# t_span = (t_span["start"], t_span["end"])
# t_eval = np.linspace(t_span[0], t_span[1], num_points)

# # Create a tqdm progress bar
# total_systems = len(systems_params_dict)  # Total iterations
# with tqdm(total=total_systems, desc="Processing systems", unit="system") as pbar:
#     for i, ((_, v1), (_, v2)) in enumerate(zip(systems_params_dict.items(), systems_initial_dict.items())):
#     #for (k1, v1), (k2, v2) in zip(systems_params_dict.items(), systems_initial_dict.items()):
        
#         # Initialize the Binder object for dynamic function import
#         binder = Binder(module_name=f"systems.{parent_model}", 
#                         function_name=parent_model, 
#                         params=v1)
        
#         # Import the module
#         binder.import_module()
        
#         # Prepare the function
#         fixed_function = binder.fixer()
        
#         if fixed_function:  
#             # Now we have the fixed function ready, so we can pass it to Sistema
#             sistema = Sistema(f=fixed_function, 
#                               y0=v2, 
#                               t=t_eval, 
#                               metodo='RK45')
            
#             # Solve the system
#             sistema.resolver()
#             sistema.graficar(tipo='series', guardar=False, show_plot=True)
#             # Get the DataFrame for the solution
#             #sistema.csv_or_dataframe(f"/home/think/Desktop/TESIS/test_runs/test_{str(test_number)}/{i}.csv")
                
#         pbar.update(1)  # Increment progress bar


import json
import numpy as np
from utils.helpers import sys_params_gen as params_gen
from utils.helpers import initial_conditions_gen as ic_gen
from data_generation.binder import Binder  
from data_generation.tsdg import Sistema  
import os
import time
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn

file_path = '/home/think/Desktop/TESIS/test_runs/templates/global_test.json'
destination_path = "/home/think/Desktop/TESIS/test_runs"

def genesis_bulk_global(file_path, destination_path):

    with open(file_path, 'r') as file:
        config = json.load(file)
    # Control variables
    config['run_mode']
    warden = config['warden']
    shared_parameters = config['shared_parameters']
    models = config['models']

    # Extract the variables we need from the shared_parameters
    test_number = shared_parameters["test_number"]
    number_of_child_systems = shared_parameters["number_of_child_systems"]  
    #t_span = shared_parameters["t_span"]  
    #t_span = (t_span[0], t_span[1]) 
    t_span = tuple(shared_parameters["t_span"])
    num_points = shared_parameters["num_points"]  
    initial_conditions = shared_parameters["initial_conditions"]  
    t_eval = np.linspace(t_span[0], t_span[1], num_points)

    # Initial conditions for each system
    systems_initial_dict = ic_gen(initial_conditions, number_of_child_systems)

    # Calcular total de iteraciones (modelos activos * sistemas por modelo)
    total_iterations = sum(1 for key, value in warden.items() if value) * number_of_child_systems

    # Barra de progreso de Rich, que muestra descripción, barra y ETA
    progress = Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("{task.completed} of {task.total}"),
        TimeRemainingColumn(),
    )
    progress.start()
    task = progress.add_task("[cyan]Generando Sistemas...",total=total_iterations)

    # Here we decide which model is allowed to be muahahaha
    for key, value in warden.items():
        if value == True:
            parent_model = key
            # Extracting parameters (and them ranges)
            params = {
                key: {"min": value[0], "max": value[1]} 
                for key, value in models[key]["params"].items()
                }
            # Parameters for each system
            systems_params_dict = params_gen(params, number_of_child_systems)
            for i, ((_, v1), (_, v2)) in enumerate(zip(systems_params_dict.items(), systems_initial_dict.items())):
                
                start_time = time.time()  # Tiempo inicial de cada iteración
                # Initialize the Binder object for dynamic function import
                binder = Binder(module_name=f"systems.{parent_model}", 
                                function_name=parent_model, 
                                params=v1)
                
                # Import the module
                binder.import_module()
                
                # Prepare the function
                fixed_function = binder.fixer()
                
                if fixed_function:  
                    # Now we have the fixed function ready, so we can pass it to Sistema
                    sistema = Sistema(f=fixed_function, 
                                        y0=v2, 
                                        t=t_eval, 
                                        metodo='RK45')
                    
                    # Solve the system
                    sistema.resolver()
                    # Display a cutie plot
                    #sistema.graficar(tipo='series', guardar=False, show_plot=True)
                    # Get the DataFrame for the solution
                    ruta = os.path.join(f"{destination_path}",f"test_{test_number}",f"{parent_model}" ,f"{parent_model}_{i}.csv")
                    sistema.csv_or_dataframe(ruta)
                    #sistema.atractor_animation()
                    print(f'{parent_model}_{i} has been generated \n at {ruta}')
                elapsed_time = time.time() - start_time
                progress.update(task,advance=1, description=f"[cyan]{parent_model}_{i}: {elapsed_time:.2f}s")
   
    progress.stop()