from pathlib import Path

'''  
Before starting a generation we need to know: 

- **Date:** 2025-09-06  
- **Experiment:** Chaos Features Extraction 
- **Location:** `/home/think/Desktop/MOCK/`  
- **Description:**  
  Testing genesis.py and consolidating its purpose.

We use logger to create such destination, as well as the MANIFESTO.txt
'''

def logger(logger_params):
    # Extract parameters
    main_folder = Path(logger_params["main_folder"])
    exp_name = logger_params["experiment_name"]
    date = logger_params["date"]
    iteration = logger_params["iteration"]
    description = logger_params["description"]

    # Build experiment folder name
    folder_name = f"{exp_name}_{date}_iter{iteration}"
    exp_folder = main_folder / folder_name

    # Create folder (including parents if missing)
    exp_folder.mkdir(parents=True, exist_ok=True)

    # Write manifesto.txt
    manifesto_path = exp_folder / "manifesto.txt"
    with open(manifesto_path, "w", encoding="utf-8") as f:
        f.write(description)

    return exp_folder, manifesto_path