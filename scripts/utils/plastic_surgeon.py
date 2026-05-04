import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import importlib
from functools import partial
import pandas as pd


def plot_3_ts(system, sol):
    fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    jejes = ['x', 'y', 'z']
    colors = ['red', 'green', 'blue']

    for i, j in enumerate(jejes):
        axs[i].plot(sol.t, sol.y[i], color=colors[i])
        axs[i].set_ylabel(j)
        axs[i].set_title(f'{system} System: {j} vs Time (RK45)')

    plt.tight_layout()
    plt.show()




def from_sol_to_df(sol,sol_dim,freq):
  if sol_dim == 2:
    df = pd.DataFrame({'x':sol.y[0],'y':sol.y[1] })
    df = df.copy()
    df['date'] = pd.date_range(start='1970-01-01', periods=len(df), freq=freq)
    df = df.set_index('date')
    df = df.asfreq(freq)
    # Rename the 'Demand' column to 'y' in the DataFrame
    df = df.rename(columns = {'y': 'exo_1'})
    df = df.rename(columns = {'x': 'y'})
    df_transitioned = df
    return df_transitioned
  elif sol_dim == 3:
    df = pd.DataFrame({'x':sol.y[0],'y':sol.y[1],'z':sol.y[2] })
    df = df.copy()
    df['date'] = pd.date_range(start='1970-01-01', periods=len(df), freq=freq)
    df = df.set_index('date')
    df = df.asfreq(freq)
    # Rename the 'Demand' column to 'y' in the DataFrame
    df = df.rename(columns = {'y': 'exo_1', 'z' : 'exo_2'})
    df = df.rename(columns = {'x': 'y'})
    df_transitioned = df
    return df_transitioned


def plot_3d(sol):
  fig = plt.figure(figsize=(10, 8))
  ax = fig.add_subplot(111, projection='3d')
  ax.plot(sol.y[0], sol.y[1], sol.y[2],
          color='purple', lw=0.5)
  ax.set_xlabel('x')
  ax.set_ylabel('y')
  ax.set_zlabel('z')
  ax.set_title(f'Attractor (3D)')  # {self.f.func.__name__}
  ax.view_init(elev=30, azim=60)


def tesefresco(df):
  df_prep = df.copy().reset_index()
  df_prep_new = df_prep[["date", "y"]]
  df_prep_new['date'] = 1
  return df_prep_new



def transition(df,freq):
  df = df.copy()
  df['date'] = pd.date_range(start='1970-01-01', periods=len(df), freq=freq)
  df = df.set_index('date')
  df = df.asfreq(freq)
  # Rename the 'Demand' column to 'y' in the DataFrame
  df = df.rename(columns = {'y': 'exo_1', 'z' : 'exo_2'})
  df = df.rename(columns = {'x': 'y'})
  df_transitioned = df

  return df_transitioned