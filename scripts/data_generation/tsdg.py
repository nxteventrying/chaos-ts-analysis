# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# from scipy.integrate import solve_ivp
# import pandas as pd
# import os
# import matplotlib.animation as animation


# class Sistema:

#     """
#     Clase para resolver ecuaciones diferenciales ordinarias (EDOs).

#     Parámetros:
#       - f: función que define el sistema de ecuaciones diferenciales (dy/dt = f(t, y)).
#       - y0: condición inicial (puede ser un número o un array para sistemas).
#       - t: array de tiempos donde se evaluará la solución.
#       - metodo: método numérico para la integración (por defecto "RK45").
#     """


#     def __init__(self, f, y0, t, metodo = "RK45"):
#         self.f = f
#         self.y0 = np.atleast_1d(y0)
#         self.t = t
#         self.metodo = metodo
#         self.solucion = None

#     def set_metodo(self, nuevo_metodo):

#         """
#         Permite cambiar el método de integración numérica.
#         """

#         self.metodo = nuevo_metodo
#         print(f"Método cambiado a {self.metodo}")

#     def resolver(self):

#         """Resuelve la EDO utilizando el método numérico definido."""

#         self.solucion = solve_ivp(self.f, [self.t[0], self.t[-1]], self.y0,
#                                     t_eval=self.t, method=self.metodo)
#         return self.solucion
    
#     def atractor_animation(self):
        
#         sol = self.solucion  
#         x, y, z = sol.y  # Extract trajectory data

#         # Set up the figure and 3D axis
#         fig = plt.figure(figsize=(8, 6))
#         ax = fig.add_subplot(111, projection='3d')
#         ax.set_xlim((np.min(x), np.max(x)))
#         ax.set_ylim((np.min(y), np.max(y)))
#         ax.set_zlim((np.min(z), np.max(z)))
#         ax.set_title("Attractor Animation")

#         # Initialize the plot elements
#         trail_length = 150  # Number of points in fading trace
#         line, = ax.plot([], [], [], 'r-', lw=1)  # Main trajectory
#         trace, = ax.plot([], [], [], 'g-', lw=2, alpha=0.7)  # Fading trace
#         point, = ax.plot([], [], [], 'bo', markersize=6)  # Moving point

#         def update(i):
#             if i < trail_length:
#                 trace_x = x[:i]
#                 trace_y = y[:i]
#                 trace_z = z[:i]
#             else:
#                 trace_x = x[i - trail_length:i]
#                 trace_y = y[i - trail_length:i]
#                 trace_z = z[i - trail_length:i]

#             # 🛠 Fix: Only apply fading if the trace has points
#             if len(trace_x) > 0:
#                 fade_alpha = np.linspace(0.1, 1.0, len(trace_x))  # Gradient fade
#                 trace.set_alpha(fade_alpha[0])  # Apply fading effect

#             # Update the trace
#             trace.set_data(trace_x, trace_y)
#             trace.set_3d_properties(trace_z)

#             # Update main trajectory and moving point
#             line.set_data(x[:i], y[:i])
#             line.set_3d_properties(z[:i])
#             point.set_data(x[i], y[i])
#             point.set_3d_properties(z[i])

#             return line, trace, point
#         # Run animation
#         ani = animation.FuncAnimation(fig, update, frames=len(self.t), interval=10, blit=False)

#         plt.show()


#         return
#     def graficar(self, tipo='3d', guardar=False, show_plot=True, filename='plot.png'):
#         """
#         Genera la gráfica de la solución de la EDO.
        
#         Parámetros:
#         - tipo: '3d' para la trayectoria en 3D o 'series' para la serie de tiempo.
#         - guardar: si True, guarda la gráfica en un archivo.
#         - show_plot: si True, muestra la gráfica en pantalla.
#         - filename: nombre del archivo donde se guardará la gráfica.
        
#         Retorna el objeto figura (fig).
#         """
#         if self.solucion is None:
#             raise ValueError("Primero debes resolver la ecuación.")

#         if tipo == '3d':
#             fig = plt.figure(figsize=(10, 8))
#             ax = fig.add_subplot(111, projection='3d')
#             ax.plot(self.solucion.y[0], self.solucion.y[1], self.solucion.y[2],
#                     color='purple', lw=0.5)
#             ax.set_xlabel('x')
#             ax.set_ylabel('y')
#             ax.set_zlabel('z')
#             ax.set_title(f'Attractor (3D)')  # {self.f.func.__name__}
#             ax.view_init(elev=30, azim=60)

#         elif tipo == 'series':
#             fig, axs = plt.subplots(self.solucion.y.shape[0], 1, figsize=(10, 8), sharex=True)
#             labels = ['x', 'y', 'z']
#             colors = ['r', 'g', 'b']

#             for i in range(self.solucion.y.shape[0]):
#                 axs[i].plot(self.solucion.t, self.solucion.y[i], color=colors[i])
#                 axs[i].set_ylabel(labels[i])
#                 axs[i].grid()

#             axs[-1].set_xlabel("Time")
#             fig.suptitle(f"Series de Tiempo de {getattr(self.f, 'func', self.f).__name__}")

#         else:
#             raise ValueError("Tipo de gráfica no reconocido. Usa '3d' o 'series'.")

#         plt.tight_layout()

#         if guardar:
#             directory = "/path/to/save/directory" 
#             os.makedirs(directory, exist_ok=True)  
#             full_path = os.path.join(directory, filename)
#             fig.savefig(full_path)
#             print(f"Gráfica guardada en {full_path}")

#         if show_plot:
#             plt.show()

#         return fig
       
#     def csv_or_dataframe(self, filename = None):

#         """Devuelve el dataframe de la series de tiempo, o un csv
#          si es que le damos un nombre """
        
#         if self.solucion is None:
#             raise ValueError("Primero debes resolver la ecuación.")
        
#         X = self.solucion.y[0]
#         Y = self.solucion.y[1]
#         Z = self.solucion.y[2]
     
#         df = pd.DataFrame({'x':X,'y':Y,'z':Z })

#         if filename:
#             df.to_csv(filename, index=False)

#         return df
    

# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# from scipy.integrate import solve_ivp
# import pandas as pd
# import matplotlib.animation as animation
# import os

# class DynamicalSystem:
#     """
#     Class to solve and visualize dynamical systems defined by ODEs.
#     """

#     def __init__(self, f, y0, t, method="RK45"):
#         self.f = f
#         self.y0 = np.atleast_1d(y0)
#         self.t = t
#         self.method = method
#         self.solution = None

#     def set_method(self, new_method):
#         """Change the integration method."""
#         self.method = new_method
#         print(f"Integration method changed to {self.method}")

#     def solve(self):
#         """Solve the ODE system with the selected method."""
#         self.solution = solve_ivp(
#             self.f,
#             [self.t[0], self.t[-1]],
#             self.y0,
#             t_eval=self.t,
#             method=self.method
#         )
#         return self.solution

#     def animate(self, trail_length=150, interval=10):
#         """Generate a 3D animation of the trajectory."""
#         if self.solution is None:
#             raise ValueError("You must solve the system first.")

#         x, y, z = self.solution.y
#         fig = plt.figure(figsize=(8, 6))
#         ax = fig.add_subplot(111, projection='3d')
#         ax.set_xlim((np.min(x), np.max(x)))
#         ax.set_ylim((np.min(y), np.max(y)))
#         ax.set_zlim((np.min(z), np.max(z)))
#         ax.set_title("Attractor Animation")

#         line, = ax.plot([], [], [], 'r-', lw=1)
#         trace, = ax.plot([], [], [], 'g-', lw=2, alpha=0.7)
#         point, = ax.plot([], [], [], 'bo', markersize=6)

#         def update(i):
#             i = i % len(self.t)
#             if i < trail_length:
#                 trace_x, trace_y, trace_z = x[:i], y[:i], z[:i]
#             else:
#                 trace_x, trace_y, trace_z = x[i - trail_length:i], y[i - trail_length:i], z[i - trail_length:i]

#             trace.set_data(trace_x, trace_y)
#             trace.set_3d_properties(trace_z)

#             line.set_data(x[:i], y[:i])
#             line.set_3d_properties(z[:i])
#             point.set_data(x[i], y[i])
#             point.set_3d_properties(z[i])
#             return line, trace, point

#         ani = animation.FuncAnimation(fig, update, frames=len(self.t), interval=interval, blit=False)
#         plt.show()

#     def plot(self, kind="3d", variable=None, save=False, show=True, filename="plot.png"):
#         """
#         Plot the solution.

#         kind: 
#           - '3d': full 3D trajectory
#           - 'projections': xy, yz, zx (or a single one if variable is set)
#           - 'series': time series (all or one)

#         variable:
#           - For kind='series': 'x', 'y', 'z', or None
#           - For kind='projections': 'xy', 'yz', 'xz', or None
#         """
#         if self.solution is None:
#             raise ValueError("You must solve the system first.")

#         labels = ["x", "y", "z"]
#         colors = ["r", "g", "b"]

#         if kind == "3d":
#             fig = plt.figure(figsize=(10, 8))
#             ax = fig.add_subplot(111, projection="3d")
#             ax.plot(*self.solution.y, color="purple", lw=0.5)
#             ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
#             ax.set_title("Attractor (3D)")

#         elif kind == "projections":
#             if variable is None:
#                 fig, axs = plt.subplots(1, 3, figsize=(15, 5))
#                 axs[0].plot(self.solution.y[0], self.solution.y[1], lw=0.5)
#                 axs[0].set_xlabel("x"); axs[0].set_ylabel("y"); axs[0].set_title("XY")

#                 axs[1].plot(self.solution.y[1], self.solution.y[2], lw=0.5)
#                 axs[1].set_xlabel("y"); axs[1].set_ylabel("z"); axs[1].set_title("YZ")

#                 axs[2].plot(self.solution.y[0], self.solution.y[2], lw=0.5)
#                 axs[2].set_xlabel("x"); axs[2].set_ylabel("z"); axs[2].set_title("XZ")
#                 fig.suptitle("2D Projections")
#             else:
#                 fig, ax = plt.subplots(figsize=(6, 6))
#                 if variable == "xy":
#                     ax.plot(self.solution.y[0], self.solution.y[1], lw=0.5)
#                     ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_title("XY Projection")
#                 elif variable == "yz":
#                     ax.plot(self.solution.y[1], self.solution.y[2], lw=0.5)
#                     ax.set_xlabel("y"); ax.set_ylabel("z"); ax.set_title("YZ Projection")
#                 elif variable == "xz":
#                     ax.plot(self.solution.y[0], self.solution.y[2], lw=0.5)
#                     ax.set_xlabel("x"); ax.set_ylabel("z"); ax.set_title("XZ Projection")
#                 else:
#                     raise ValueError("Variable must be 'xy', 'yz', 'xz' or None.")

#         elif kind == "series":
#             if variable is None:
#                 n_vars = self.solution.y.shape[0]
#                 fig, axs = plt.subplots(n_vars, 1, figsize=(10, 8), sharex=True)
#                 for i in range(n_vars):
#                     axs[i].plot(self.solution.t, self.solution.y[i], color=colors[i])
#                     axs[i].set_ylabel(labels[i]); axs[i].grid()
#                 axs[-1].set_xlabel("Time")
#                 fig.suptitle("Time Series")
#             else:
#                 var_map = {"x": 0, "y": 1, "z": 2}
#                 if variable not in var_map:
#                     raise ValueError("Variable must be 'x', 'y' or 'z'")
#                 idx = var_map[variable]
#                 fig, ax = plt.subplots(figsize=(10, 4))
#                 ax.plot(self.solution.t, self.solution.y[idx], color=colors[idx])
#                 ax.set_ylabel(variable); ax.set_xlabel("Time"); ax.grid()
#                 fig.suptitle(f"Time Series - {variable}")

#         else:
#             raise ValueError("Unknown plot kind.")

#         plt.tight_layout()
#         if save:
#             full_path = os.path.join(os.getcwd(), filename)
#             fig.savefig(full_path)
#             print(f"Plot saved to {full_path}")
#         if show:
#             plt.show()
#         return fig

#     def to_dataframe(self, path=None):
#         """
#         Return a DataFrame with the time series.
#         If path is specified, save as CSV.
#         """
#         if self.solution is None:
#             raise ValueError("You must solve the system first.")

#         df = pd.DataFrame({"x": self.solution.y[0],
#                            "y": self.solution.y[1],
#                            "z": self.solution.y[2]},
#                           index=self.solution.t)

#         if path is not None:
#             df.to_csv(path, index=True)
#             print(f"Data saved to {path}")
#         return df


# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# from scipy.integrate import solve_ivp
# import pandas as pd
# import matplotlib.animation as animation
# import os

# class DynamicalSystem:
#     """
#     Class to solve and visualize dynamical systems defined by ODEs.
#     """

#     def __init__(self, f, y0, t, method="RK45", notebook=False):
#         self.f = f
#         self.y0 = np.atleast_1d(y0)
#         self.t = t
#         self.method = method
#         self.solution = None
#         self.notebook = notebook  # <- switch for Jupyter

#     def set_method(self, new_method):
#         """Change the integration method."""
#         self.method = new_method
#         print(f"Integration method changed to {self.method}")

#     def solve(self):
#         """Solve the ODE system with the selected method."""
#         self.solution = solve_ivp(
#             self.f,
#             [self.t[0], self.t[-1]],
#             self.y0,
#             t_eval=self.t,
#             method=self.method
#         )
#         return self.solution

#     def solve_rk4(self, dt):
#         """Fixed-step RK4 integration."""
#         y = [self.y0]
#         for i in range(1, len(self.t)):
#             u = y[-1]
#             h = dt
#             f = self.f
#             k1 = f(u)
#             k2 = f(u + 0.5*h*k1)
#             k3 = f(u + 0.5*h*k2)
#             k4 = f(u + h*k3)
#             y_next = u + (h/6)*(k1 + 2*k2 + 2*k3 + k4)
#             y.append(y_next)
#         y = np.array(y).T
#         self.solution = type('Solution', (), {})()  # simple object to mimic solve_ivp
#         self.solution.t = self.t
#         self.solution.y = y
#         return self.solution





# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# from scipy.integrate import solve_ivp
# import pandas as pd
# import matplotlib.animation as animation
# import os

# class DynamicalSystem:
#     """
#     Class to solve and visualize dynamical systems defined by ODEs.
#     """

#     def __init__(self, f, y0, t, method="RK45", notebook=False):
#         self.f = f
#         self.y0 = np.atleast_1d(y0)
#         self.t = t
#         self.method = method
#         self.solution = None
#         self.notebook = notebook

#     def set_method(self, new_method):
#         """Change the integration method."""
#         self.method = new_method
#         print(f"Integration method changed to {self.method}")

#     def solve(self):
#         """Solve the ODE system with the selected method."""
#         if self.method == "RK4":
#             # Use custom RK4 implementation
#             dt = self.t[1] - self.t[0]  # Assumes uniform time spacing
#             return self.solve_rk4(dt)
#         else:
#             # Use scipy's solve_ivp
#             self.solution = solve_ivp(
#                 self.f,
#                 [self.t[0], self.t[-1]],
#                 self.y0,
#                 t_eval=self.t,
#                 method=self.method
#             )
#             return self.solution

#     def solve_rk4(self, dt):
#         """Fixed-step RK4 integration."""
#         y = [self.y0]
#         t_current = self.t[0]
        
#         for i in range(1, len(self.t)):
#             u = y[-1]
#             h = dt
            
#             # RK4 steps - note that f expects (t, y) signature
#             k1 = self.f(t_current, u)
#             k2 = self.f(t_current + 0.5*h, u + 0.5*h*k1)
#             k3 = self.f(t_current + 0.5*h, u + 0.5*h*k2)
#             k4 = self.f(t_current + h, u + h*k3)
            
#             y_next = u + (h/6)*(k1 + 2*k2 + 2*k3 + k4)
#             y.append(y_next)
#             t_current += h
            
#         y = np.array(y).T
        
#         # Mimic solve_ivp's output structure
#         self.solution = type('Solution', (), {})()
#         self.solution.t = self.t
#         self.solution.y = y
#         self.solution.success = True
        
#         return self.solution


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.integrate import solve_ivp
import pandas as pd
import matplotlib.animation as animation
import os

class DynamicalSystem:
    """
    Class to solve and visualize dynamical systems defined by ODEs.
    """

    def __init__(self, f, y0, t, method="RK45", notebook=False):
        self.f = f
        self.y0 = np.atleast_1d(y0)
        self.t = t
        self.method = method
        self.solution = None
        self.notebook = notebook

    def set_method(self, new_method):
        """Change the integration method."""
        self.method = new_method
        print(f"Integration method changed to {self.method}")

    def solve(self):
        """Solve the ODE system with the selected method."""
        if self.method == "RK4":
            # Use custom RK4 implementation
            dt = self.t[1] - self.t[0]  # Assumes uniform time spacing
            return self.solve_rk4(dt)
        else:
            # Use scipy's solve_ivp
            self.solution = solve_ivp(
                self.f,
                [self.t[0], self.t[-1]],
                self.y0,
                t_eval=self.t,
                method=self.method
            )
            return self.solution

    def solve_rk4(self, dt):
        """Fixed-step RK4 integration."""
        y = [self.y0]
        
        for i in range(1, len(self.t)):
            u = y[-1]
            h = dt
            
            # RK4 steps - handle both f(t, y) and f(y) signatures
            try:
                # Try f(t, y) signature first (solve_ivp standard)
                k1 = self.f(self.t[i-1], u)
                k2 = self.f(self.t[i-1] + 0.5*h, u + 0.5*h*k1)
                k3 = self.f(self.t[i-1] + 0.5*h, u + 0.5*h*k2)
                k4 = self.f(self.t[i-1] + h, u + h*k3)
            except TypeError:
                # Fall back to f(y) signature (fixed parameters)
                k1 = self.f(u)
                k2 = self.f(u + 0.5*h*k1)
                k3 = self.f(u + 0.5*h*k2)
                k4 = self.f(u + h*k3)
            
            y_next = u + (h/6)*(k1 + 2*k2 + 2*k3 + k4)
            y.append(y_next)
            
        y = np.array(y).T
        
        # Mimic solve_ivp's output structure
        self.solution = type('Solution', (), {})()
        self.solution.t = self.t
        self.solution.y = y
        self.solution.success = True
        
        return self.solution



    def animate(self, trail_length=150, interval=10, show=True):
        """Generate a 3D animation of the trajectory."""
        if self.solution is None:
            raise ValueError("You must solve the system first.")

        x, y, z = self.solution.y
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlim((np.min(x), np.max(x)))
        ax.set_ylim((np.min(y), np.max(y)))
        ax.set_zlim((np.min(z), np.max(z)))
        ax.set_title("Attractor Animation")

        line, = ax.plot([], [], [], 'r-', lw=1)
        trace, = ax.plot([], [], [], 'g-', lw=2, alpha=0.7)
        point, = ax.plot([], [], [], 'bo', markersize=6)

        def update(i):
            i = i % len(self.t)
            if i < trail_length:
                trace_x, trace_y, trace_z = x[:i], y[:i], z[:i]
            else:
                trace_x, trace_y, trace_z = x[i - trail_length:i], y[i - trail_length:i], z[i - trail_length:i]

            trace.set_data(trace_x, trace_y)
            trace.set_3d_properties(trace_z)

            line.set_data(x[:i], y[:i])
            line.set_3d_properties(z[:i])
            point.set_data(x[i], y[i])
            point.set_3d_properties(z[i])
            return line, trace, point

        ani = animation.FuncAnimation(fig, update, frames=len(self.t), interval=interval, blit=False)
        if show and not self.notebook:
            plt.show()
        return ani

    def plot(self, kind="3d", variable=None, save=False, show=True, filename="plot.png"):
        """
        Plot the solution.

        kind: 
          - '3d': full 3D trajectory
          - 'projections': xy, yz, zx (or a single one if variable is set)
          - 'series': time series (all or one)

        variable:
          - For kind='series': 'x', 'y', 'z', or None
          - For kind='projections': 'xy', 'yz', 'xz', or None
        """
        if self.solution is None:
            raise ValueError("You must solve the system first.")

        labels = ["x", "y", "z"]
        colors = ["r", "g", "b"]

        if kind == "3d":
            fig = plt.figure(figsize=(10, 8))
            ax = fig.add_subplot(111, projection="3d")
            ax.plot(*self.solution.y, color="purple", lw=0.5)
            ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
            ax.set_title("Atractor de Lorenz63")

        elif kind == "projections":
            if variable is None:
                fig, axs = plt.subplots(1, 3, figsize=(15, 5))
                axs[0].plot(self.solution.y[0], self.solution.y[1], lw=0.5)
                axs[0].set_xlabel("x"); axs[0].set_ylabel("y"); axs[0].set_title("XY")

                axs[1].plot(self.solution.y[1], self.solution.y[2], lw=0.5)
                axs[1].set_xlabel("y"); axs[1].set_ylabel("z"); axs[1].set_title("YZ")

                axs[2].plot(self.solution.y[0], self.solution.y[2], lw=0.5)
                axs[2].set_xlabel("x"); axs[2].set_ylabel("z"); axs[2].set_title("XZ")
                fig.suptitle("2D Projections")
            else:
                fig, ax = plt.subplots(figsize=(6, 6))
                if variable == "xy":
                    ax.plot(self.solution.y[0], self.solution.y[1], lw=0.5)
                    ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_title("XY Projection")
                elif variable == "yz":
                    ax.plot(self.solution.y[1], self.solution.y[2], lw=0.5)
                    ax.set_xlabel("y"); ax.set_ylabel("z"); ax.set_title("YZ Projection")
                elif variable == "xz":
                    ax.plot(self.solution.y[0], self.solution.y[2], lw=0.5)
                    ax.set_xlabel("x"); ax.set_ylabel("z"); ax.set_title("XZ Projection")
                else:
                    raise ValueError("Variable must be 'xy', 'yz', 'xz' or None.")

        elif kind == "series":
            if variable is None:
                n_vars = self.solution.y.shape[0]
                fig, axs = plt.subplots(n_vars, 1, figsize=(10, 8), sharex=True)
                for i in range(n_vars):
                    axs[i].plot(self.solution.t, self.solution.y[i], color=colors[i])
                    axs[i].set_ylabel(labels[i]); axs[i].grid()
                axs[-1].set_xlabel("Time")
                fig.suptitle("Series de Tiempo de Lorenz63")
            else:
                var_map = {"x": 0, "y": 1, "z": 2}
                if variable not in var_map:
                    raise ValueError("Variable must be 'x', 'y' or 'z'")
                idx = var_map[variable]
                fig, ax = plt.subplots(figsize=(10, 4))
                ax.plot(self.solution.t, self.solution.y[idx], color=colors[idx])
                ax.set_ylabel(variable); ax.set_xlabel("Time"); ax.grid()
                fig.suptitle(f"Time Series - {variable}")

        else:
            raise ValueError("Unknown plot kind.")

        plt.tight_layout()
        if save:
            full_path = os.path.join(os.getcwd(), filename)
            fig.savefig(full_path)
            print(f"Plot saved to {full_path}")

        # only show if not in notebook or show explicitly requested
        if show and not self.notebook:
            plt.show()
        return fig

    def to_dataframe(self, path=None):
        """
        Return a DataFrame with the time series using numeric index.
        If path is specified, save as CSV.
        """
        if self.solution is None:
            raise ValueError("You must solve the system first.")

        # Create DataFrame with numeric index
        df = pd.DataFrame({
            "x": self.solution.y[0],
            "y": self.solution.y[1],
            "z": self.solution.y[2]
        })
        # Reset index to start at 1
        df.index = np.arange(1, len(df) + 1)

        if path is not None:
            df.to_csv(path, index=True)  # index will now be 1, 2, 3, ...
            print(f"Data saved to {path}")
        return df
