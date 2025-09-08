import numpy as np
import importlib
from functools import partial
import sys

class Binder:
    def __init__(self, module_name, function_name, params):
    
        self.module_name = module_name
        self.function_name = function_name
        self.params = params
        self.module = None
        self.prepared_function = None

    def import_module(self):
        """Imports the module and assigns it to self.module."""
        self.module = importlib.import_module(self.module_name)
        #print(f"Module {self.module_name} imported successfully.")
     
    def fixer(self):
        """Fixes parameters to the function and returns a partially applied function."""
        if self.module is None:
            print("You have to import_module first :)")
            return None
        
        func = getattr(self.module, self.function_name, None)
        if func is None:
            print(f"Function {self.function_name} not found in module {self.module_name}.")
            return None

        self.prepared_function = partial(func, *self.params)
        return self.prepared_function
