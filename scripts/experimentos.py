# import json
# import numpy as np
# from utils.helpers import sys_params_gen as params_gen
# from utils.helpers import initial_conditions_gen as ic_gen
# from data_generation.binder import Binder  
# from data_generation.tsdg import Sistema  
# import os

# file_path = '/home/think/Desktop/TESIS/test_runs/templates/global_test.json'
# destination_path = "/home/think/Desktop/TESIS/test_runs"

# def genesis_bulk_global(file_path, destination_path):

#     with open(file_path, 'r') as file:
#         config = json.load(file)
#     # Control variables
#     config['run_mode']
#     warden = config['warden']
#     shared_parameters = config['shared_parameters']
#     models = config['models']

#     # Extract the variables we need from the shared_parameters
#     test_number = shared_parameters["test_number"]
#     number_of_child_systems = shared_parameters["number_of_child_systems"]  
#     #t_span = shared_parameters["t_span"]  
#     #t_span = (t_span[0], t_span[1]) 
#     t_span = tuple(shared_parameters["t_span"])
#     num_points = shared_parameters["num_points"]  
#     initial_conditions = shared_parameters["initial_conditions"]  
#     t_eval = np.linspace(t_span[0], t_span[1], num_points)

#     # Initial conditions for each system
#     systems_initial_dict = ic_gen(initial_conditions, number_of_child_systems)
#     # Here we decide which model is allowed to be muahahaha
#     for key, value in warden.items():
#         if value == True:
#             parent_model = key
#             # Extracting parameters (and them ranges)
#             params = {
#                 key: {"min": value[0], "max": value[1]} 
#                 for key, value in models[key]["params"].items()
#                 }
#             # Parameters for each system
#             systems_params_dict = params_gen(params, number_of_child_systems)
#             for i, ((_, v1), (_, v2)) in enumerate(zip(systems_params_dict.items(), systems_initial_dict.items())):

#                 # Initialize the Binder object for dynamic function import
#                 binder = Binder(module_name=f"systems.{parent_model}", 
#                                 function_name=parent_model, 
#                                 params=v1)
                
#                 # Import the module
#                 binder.import_module()
                
#                 # Prepare the function
#                 fixed_function = binder.fixer()
                
#                 if fixed_function:  
#                     # Now we have the fixed function ready, so we can pass it to Sistema
#                     sistema = Sistema(f=fixed_function, 
#                                         y0=v2, 
#                                         t=t_eval, 
#                                         metodo='RK45')
                    
#                     # Solve the system
#                     sistema.resolver()
#                     # Display a nice plot
#                     #sistema.graficar(tipo='3d', guardar=False, show_plot=True)
#                     # Get the DataFrame for the solution
#                     ruta = os.path.join(f"{destination_path}",f"test_{test_number}",f"{parent_model}" ,f"{parent_model}_{i}.csv")
#                     #sistema.csv_or_dataframe(ruta)
#                     print(f'{parent_model}_{i} has been generated \n at {ruta}')

#         else:
#             pass    


# from rich.progress import Progress
# import time

# with Progress() as progress:
#     task = progress.add_task("[cyan]Procesando...", total=100)
#     while not progress.finished:
#         progress.update(task, advance=1)
#         time.sleep(0.1)


# import json
# import numpy as np
# from utils.helpers import sys_params_gen as params_gen
# from utils.helpers import initial_conditions_gen as ic_gen
# from data_generation.binder import Binder  
# from data_generation.tsdg import Sistema  
# import os
# import time
# from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn

# file_path = '/home/think/Desktop/TESIS/test_runs/templates/global_test.json'
# destination_path = "/home/think/Desktop/TESIS/test_runs"

# def genesis_bulk_global(file_path, destination_path, user_choice="both"):
#     # Cargar configuración desde JSON
#     with open(file_path, 'r') as file:
#         config = json.load(file)
#     # Variables de control
#     config['run_mode']
#     warden = config['warden']
#     shared_parameters = config['shared_parameters']
#     models = config['models']

#     # Extraer variables necesarias de shared_parameters
#     test_number = shared_parameters["test_number"]
#     number_of_child_systems = shared_parameters["number_of_child_systems"]  
#     t_span = tuple(shared_parameters["t_span"])
#     num_points = shared_parameters["num_points"]  
#     initial_conditions = shared_parameters["initial_conditions"]  
#     t_eval = np.linspace(t_span[0], t_span[1], num_points)

#     # Condiciones iniciales para cada sistema
#     systems_initial_dict = ic_gen(initial_conditions, number_of_child_systems)

#     # Calcular total de iteraciones (modelos activos * sistemas por modelo)
#     total_iterations = sum(1 for key, value in warden.items() if value) * number_of_child_systems

#     # Barra de progreso de Rich, que muestra descripción, barra y ETA
#     progress = Progress(
#         TextColumn("[progress.description]{task.description}"),
#         BarColumn(),
#         TextColumn("{task.completed} of {task.total}"),
#         TimeRemainingColumn(),
#     )
#     progress.start()
#     task = progress.add_task("[cyan]Generando Sistemas...",total=total_iterations)

#     # Aquí decidimos qué modelo está permitido
#     for key, value in warden.items():
#         if value == True:
#             parent_model = key
#             # Extraer parámetros (transforma lista [min, max] en diccionario)
#             params = {
#                 param_key: {"min": param_value[0], "max": param_value[1]} 
#                 for param_key, param_value in models[key]["params"].items()
#             }
#             # Parámetros para cada sistema
#             systems_params_dict = params_gen(params, number_of_child_systems)
#             for i, ((_, v1), (_, v2)) in enumerate(zip(systems_params_dict.items(), systems_initial_dict.items())):
#                 start_time = time.time()  # Tiempo inicial de cada iteración

#                 # Inicializar el Binder para importación dinámica
#                 binder = Binder(module_name=f"systems.{parent_model}", 
#                                 function_name=parent_model, 
#                                 params=v1)
                
#                 # Importar el módulo
#                 binder.import_module()
                
#                 # Preparar la función
#                 fixed_function = binder.fixer()
                
#                 if fixed_function:  
#                     # Ahora tenemos la función fija, se la pasamos a Sistema
#                     sistema = Sistema(f=fixed_function, 
#                                       y0=v2, 
#                                       t=t_eval, 
#                                       metodo='RK45')
                    
#                     # Resolver el sistema
#                     sistema.resolver()

#                     # Dependiendo de la elección del usuario
#                     if user_choice in ["plot", "both"]:
#                         sistema.graficar(tipo='3d', guardar=False, show_plot=True)
                    
#                     if user_choice in ["save", "both"]:
#                         ruta = os.path.join(destination_path, f"test_{test_number}", f"{parent_model}", f"{parent_model}_{i}.csv")
#                         #sistema.csv_or_dataframe(ruta)
#                     else:
#                         ruta = "No se guardó archivo"  # Para actualización en el progress
#                 elapsed_time = time.time() - start_time
#                 progress.update(task,advance=1, description=f"[cyan]{parent_model}_{i}: {elapsed_time:.2f}s")

#     progress.stop()

# # Ejemplo de uso:
# genesis_bulk_global(file_path, destination_path, user_choice="save")


# import numpy as np
# import matplotlib.pyplot as plt
# import scipy.integrate as integrate
# import matplotlib.animation as animation

# # Double pendulum equations of motion
# def f(t, state, g=9.81, l=0.4):
#     theta_1, theta_2, omega_1, omega_2 = state
#     ftheta1 = omega_1
#     ftheta2 = omega_2
#     denom = (3 - np.cos(2*theta_1 - 2*theta_2)) + 1e-6  # Avoid singularity
#     fomega1 = -((omega_1**2)*np.sin(2*theta_1 - 2*theta_2) + 2*(omega_2**2)*np.sin(theta_1 - theta_2) + (g/l)*(np.sin(theta_1 - 2*theta_2) + 3*np.sin(theta_1))) / denom
#     fomega2 = (4*(omega_1**2)*np.sin(theta_1 - theta_2) + (omega_2**2)*np.sin(2*theta_1 - 2*theta_2) + 2*(g/l)*(np.sin(2*theta_1 - theta_2) - np.sin(theta_2))) / denom
#     return [ftheta1, ftheta2, fomega1, fomega2]

# # Initial conditions: (theta1, theta2, omega1, omega2)
# y0 = [np.pi/2, np.pi/2, 0.0, 0.0]
# t_span = (0, 200)
# t_eval = np.linspace(t_span[0], t_span[1], 10000)

# # Solve the ODE
# sol = integrate.solve_ivp(f, t_span, y0, method='DOP853', t_eval=t_eval)

# # Convert to Cartesian coordinates
# l = 0.4  # Length of rods
# x1 = l * np.sin(sol.y[0])  # First pendulum bob (x)
# y1 = -l * np.cos(sol.y[0])  # First pendulum bob (y)
# x2 = x1 + l * np.sin(sol.y[1])  # Second pendulum bob (x)
# y2 = y1 - l * np.cos(sol.y[1])  # Second pendulum bob (y)

# # Animation setup
# fig, ax = plt.subplots(figsize=(5, 5))
# ax.set_xlim(-2*l, 2*l)
# ax.set_ylim(-2*l, 2*l)
# ax.set_aspect('equal')
# ax.set_title("Double Pendulum Simulation")

# # Elements to animate
# line, = ax.plot([], [], 'o-', lw=2)  # Pendulum rods
# trace, = ax.plot([], [], 'r-', alpha=0.5)  # Trail of second bob
# trace_x, trace_y = [], []

# # # Animation function
# # def update(i):
# #     line.set_data([0, x1[i], x2[i]], [0, y1[i], y2[i]])  # Pendulum arms
# #     trace_x.append(x2[i])  # Store trace positions
# #     trace_y.append(y2[i])
# #     trace.set_data(trace_x, trace_y)  # Update trace
# #     return line, trace

# # Animation function
# def update(i):
#     if i >= len(t_eval):  # Stop updating when out of data
#         ani.event_source.stop()  # Stop animation loop
#         return line, trace  # Return current frame

#     line.set_data([0, x1[i], x2[i]], [0, y1[i], y2[i]])  # Pendulum arms
#     trace_x.append(x2[i])  # Store trace positions
#     trace_y.append(y2[i])
#     trace.set_data(trace_x, trace_y)  # Update trace
#     return line, trace


# # Run animation
# ani = animation.FuncAnimation(fig, update, frames=len(t_eval), interval=20, blit=True)
# plt.show()



# import numpy as np
# import matplotlib.pyplot as plt
# import scipy.integrate as integrate
# import matplotlib.animation as animation

# # Double pendulum equations of motion
# def f(t, state, g=9.81, l=0.4):
#     theta_1, theta_2, omega_1, omega_2 = state
#     ftheta1 = omega_1
#     ftheta2 = omega_2
#     denom = (3 - np.cos(2*theta_1 - 2*theta_2)) + 1e-6  # Avoid singularity
#     fomega1 = -((omega_1**2)*np.sin(2*theta_1 - 2*theta_2) + 2*(omega_2**2)*np.sin(theta_1 - theta_2) + (g/l)*(np.sin(theta_1 - 2*theta_2) + 3*np.sin(theta_1))) / denom
#     fomega2 = (4*(omega_1**2)*np.sin(theta_1 - theta_2) + (omega_2**2)*np.sin(2*theta_1 - 2*theta_2) + 2*(g/l)*(np.sin(2*theta_1 - theta_2) - np.sin(theta_2))) / denom
#     return [ftheta1, ftheta2, fomega1, fomega2]

# # Initial conditions
# y0 = [np.pi/2, np.pi/2, 0.0, 0.0]
# t_span = (190, 250)
# t_eval = np.linspace(t_span[0], t_span[1], 1000)  # Increase to 1000 frames

# # Solve ODE
# sol = integrate.solve_ivp(f, t_span, y0, method='DOP853', t_eval=t_eval)

# # Convert to Cartesian coordinates
# l = 0.4  # Length of rods
# x1 = l * np.sin(sol.y[0])  
# y1 = -l * np.cos(sol.y[0])  
# x2 = x1 + l * np.sin(sol.y[1])  
# y2 = y1 - l * np.cos(sol.y[1])  

# # Animation setup
# fig, ax = plt.subplots(figsize=(5, 5))
# ax.set_xlim(-2*l, 2*l)
# ax.set_ylim(-2*l, 2*l)
# ax.set_aspect('equal')
# ax.set_title("Double Pendulum Simulation")

# # Elements to animate
# line, = ax.plot([], [], 'o-', lw=2)  # Pendulum arms
# trace, = ax.plot([], [], 'r-', alpha=0.5)  # Trail of second bob
# trace_x, trace_y = [], []

# # Add counter text
# counter_text = ax.text(0.05, 0.9, '', transform=ax.transAxes, fontsize=12, color='blue')

# # Animation function
# def update(i):
#     if i >= len(t_eval):  # Stop updating when out of data
#         ani.event_source.stop()  # Stop animation loop
#         return line, trace, counter_text  

#     # Update pendulum arms
#     line.set_data([0, x1[i], x2[i]], [0, y1[i], y2[i]])  
    
#     # Store trace positions
#     trace_x.append(x2[i])  
#     trace_y.append(y2[i])
#     trace.set_data(trace_x, trace_y)  

#     # Update frame counter
#     remaining_frames = len(t_eval) - i
#     counter_text.set_text(f"Frames Left: {remaining_frames}")

#     return line, trace, counter_text  

# # Run animation
# ani = animation.FuncAnimation(fig, update, frames=len(t_eval), interval=20, blit=True)
# plt.show()


# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# from mpl_toolkits.mplot3d import Axes3D
# from scipy.integrate import solve_ivp

# # 💡 Lorenz system equations
# def lorenz(t, state, sigma=10, beta=8/3, rho=28):
#     x, y, z = state
#     dx = sigma * (y - x)
#     dy = x * (rho - z) - y
#     dz = x * y - beta * z
#     return [dx, dy, dz]

# # 🌟 Solve the system
# t_span = (0, 40)  # Time interval
# t_eval = np.linspace(t_span[0], t_span[1], 4000)  # More frames for smoothness
# y0 = [1, 1, 1]  # Initial conditions

# sol = solve_ivp(lorenz, t_span, y0, t_eval=t_eval)
# x, y, z = sol.y  # Extract solutions

# # 🎨 Set up figure & 3D axis
# fig = plt.figure(figsize=(8, 6))
# ax = fig.add_subplot(111, projection='3d')
# ax.set_xlim((np.min(x), np.max(x)))
# ax.set_ylim((np.min(y), np.max(y)))
# ax.set_zlim((np.min(z), np.max(z)))
# ax.set_title("Lorenz Attractor Animation")

# # ✨ Initialize plot elements
# trail_length = 200  # Length of fading trace
# line, = ax.plot([], [], [], 'r-', lw=1)  # Full trajectory
# trace, = ax.plot([], [], [], 'g-', lw=2, alpha=0.7)  # Fading trace
# point, = ax.plot([], [], [], 'bo', markersize=6)  # Moving point
# frame_counter = ax.text2D(0.05, 0.9, '', transform=ax.transAxes, fontsize=12, color='black')

# def update(i):
#     if i < trail_length:
#         trace_x = x[:i]
#         trace_y = y[:i]
#         trace_z = z[:i]
#     else:
#         trace_x = x[i - trail_length:i]
#         trace_y = y[i - trail_length:i]
#         trace_z = z[i - trail_length:i]

#     # 🛠 Fix: Only apply fading if the trace has points
#     if len(trace_x) > 0:
#         fade_alpha = np.linspace(0.1, 1.0, len(trace_x))  # Gradient fade
#         trace.set_alpha(fade_alpha[0])  # Apply fading effect

#     # Update the trace
#     trace.set_data(trace_x, trace_y)
#     trace.set_3d_properties(trace_z)

#     # Update main trajectory and moving point
#     line.set_data(x[:i], y[:i])
#     line.set_3d_properties(z[:i])
#     point.set_data(x[i], y[i])
#     point.set_3d_properties(z[i])

#     return line, trace, point


# # 🎬 Run animation
# ani = animation.FuncAnimation(fig, update, frames=len(t_eval), interval=10, blit=False)

# plt.show()







from data_generation.tsdg import Sistema as sys
from data_generation.binder import Binder

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D


def wachi(system_name, parameters):
    # Use Binder to fix parameters
    binder = Binder(f"systems.{system_name}", f"{system_name}", parameters)
    binder.import_module()
    lorenz_fixed = binder.fixer()  # Partially applied function
    
    # Time range
    t = np.linspace(0, 105, 3000)  # More frames for a smoother animation

    # Initial conditions
    y0 = [0.1, 1, 0.1]

    # Solve the system
    edo = sys(lorenz_fixed, y0=y0, t=t, metodo="RK45")
    edo.resolver()
    sol = edo.solucion  # Solution (assuming it's stored as `sol` in your `Sistema` class)

    x, y, z = sol.y  # Extract trajectory data

    # Set up the figure and 3D axis
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim((np.min(x), np.max(x)))
    ax.set_ylim((np.min(y), np.max(y)))
    ax.set_zlim((np.min(z), np.max(z)))
    ax.set_title("Lorenz Attractor Animation")

    # Initialize the plot elements
    trail_length = 150  # Number of points in fading trace
    line, = ax.plot([], [], [], 'r-', lw=1)  # Main trajectory
    trace, = ax.plot([], [], [], 'g-', lw=2, alpha=0.7)  # Fading trace
    point, = ax.plot([], [], [], 'bo', markersize=6)  # Moving point

    def update(i):
        if i < trail_length:
            trace_x = x[:i]
            trace_y = y[:i]
            trace_z = z[:i]
        else:
            trace_x = x[i - trail_length:i]
            trace_y = y[i - trail_length:i]
            trace_z = z[i - trail_length:i]

        # 🛠 Fix: Only apply fading if the trace has points
        if len(trace_x) > 0:
            fade_alpha = np.linspace(0.1, 1.0, len(trace_x))  # Gradient fade
            trace.set_alpha(fade_alpha[0])  # Apply fading effect

        # Update the trace
        trace.set_data(trace_x, trace_y)
        trace.set_3d_properties(trace_z)

        # Update main trajectory and moving point
        line.set_data(x[:i], y[:i])
        line.set_3d_properties(z[:i])
        point.set_data(x[i], y[i])
        point.set_3d_properties(z[i])

        return line, trace, point
    # Run animation
    ani = animation.FuncAnimation(fig, update, frames=len(t), interval=10, blit=False)

    plt.show()



system_name = 'halvorsen'
params_rossler = (0.2,0.2,5.7)
params_aizawa = tuple(x + 0.9 for x in (0.95, 0.7, 0.6, 3.5, 0.25, 0.1))
params_lorenz63 = (1,2)
params_sprott = (2.07,1.79)
params_halvorsen = (1.89,)
wachi(system_name, parameters = params_halvorsen)