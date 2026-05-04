import os
import time
import json
import numpy as np

def read_config(file_path):
    with open(file_path, 'r') as file:
        config = json.load(file)

    test_number = config["test_number"]
    parent_model = config["parent_model"]
    number_of_child_systems = config["number_of_child_systems"]
    kind_step = config["kind_step"]
    
    # Extracting parameters (sigma, rho, beta ranges)
    params = {
        key: {"min": value[0], "max": value[1]} 
        for key, value in config["params"].items()
    }

    # Extracting initial conditions with min/max values
    initial_conditions = {
        key: {"min": value["min"], "max": value["max"]}
        for key, value in config["initial_conditions"].items()
    }

    t_span = {"start": config["t_span"][0], "end": config["t_span"][1]}
    num_points = config["num_points"]

    return {
        "test_number": test_number,
        "parent_model": parent_model,
        "number_of_child_systems": number_of_child_systems,
        "kind_step": kind_step,
        "params": params,
        "initial_conditions": initial_conditions,
        "t_span": t_span,
        "num_points": num_points
    }

def load_config():

    answer = input("Do you have a configuration file? (Y/N): ").strip().lower()

    if answer == "y":
        file_path = input("Where is your configuration file for this test?\n").strip()
        
        # /home/think/Desktop/TESIS/test_runs/test_1/test1.json

        # Check if file exists
        if not os.path.isfile(file_path):
            print("File not found. Make sure you typed the correct path.")
            exit(1)  # Exit script

        print("\nLoading configuration...")
        time.sleep(1)  # <- Delay for 2 seconds
        config_data = read_config(file_path)  # Read JSON
        print("Configuration loaded")

        return config_data

    else:
        print("Go and make one with architect.py you dumbass")
        exit(1)


def frange(start, stop, step):
    while start <= stop:
        yield round(start, 10)  # Avoid floating-point errors
        start += step

def sys_params_gen(params, number_of_child_systems):

  child_parameters_bag = {}

  for key, value in params.items():
      min_value = value["min"]
      max_value = value["max"]
      step = (max_value - min_value) / number_of_child_systems
      child_parameters_bag[key] = list(frange(min_value, max_value, step))

  systems_params_dict = {}

  y = []
  for value in child_parameters_bag.values():
    y.append(len(value))
  for i in range(min(y)):
    y = []
    for key,value in child_parameters_bag.items():
      y.append(value[i])
    systems_params_dict[f"system_{i}_params"] = tuple(y) 
  
  return systems_params_dict  


def initial_conditions_gen(initial_conditions, number_of_child_systems):

  child_initial_conditions_bag = {}

  for key, value in initial_conditions.items():
    # Retrieve the dynamically created min and max values from the global namespace
    min_value = value["min"]
    max_value = value["max"]
    step = (max_value - min_value) / number_of_child_systems
    gen = frange(min_value, max_value, step)
    child_initial_conditions_bag.update({f"{key}": np.fromiter(gen, dtype=float)})

  systems_initial_dict = {}
  w = []
  for value in child_initial_conditions_bag.values():
    w.append(len(value))
  for i in range(min(w)):
    y = []
    for key,value in child_initial_conditions_bag.items():
      y.append(value[i])
    systems_initial_dict[f"initial_condition_{i}"] = y
  
  return systems_initial_dict