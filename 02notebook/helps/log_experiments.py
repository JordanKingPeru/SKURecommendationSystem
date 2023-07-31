# Import necessary libraries
import pandas as pd
from datetime import datetime
from IPython import get_ipython
import sys
import re
import os


def generate_experiment_id():
    now = datetime.now()
    return now.strftime('%Y%m%d%H%M%S')


def get_dataframes_in_memory():
    # Get the IPython instance
    ipython = get_ipython()

    # Get all interactive variables
    all_vars = ipython.user_ns

    # Filter out everything that is not a DataFrame
    dataframes = {name: var for name, var in all_vars.items()
                  if isinstance(var, pd.DataFrame)}

    # Create a list of dictionaries, each containing information about one DataFrame
    df_info = [{'name': name, 'rows': df.shape[0], 'cols': df.shape[1], 
                'size': sys.getsizeof(df), 'columns': list(df.columns),
                'first_record': df.iloc[0].to_dict() if not df.empty else None}
               for name, df in dataframes.items() if not re.match(r'^_\d+$', name)]

    return str(df_info)


def get_other_objects_in_memory():
    # Get the IPython instance
    ipython = get_ipython()

    # Get all interactive variables
    all_vars = ipython.user_ns

    # Filter out everything that is not a DataFrame and does not start with an underscore
    other_objects = {name: var for name, var in all_vars.items()
                     if not isinstance(var, pd.DataFrame) and not re.match(r'^_', name)
                     and type(var).__name__ not in ['module', 'ZMQExitAutocall']}

    # Create a list of dictionaries, each containing information about one object
    obj_info = [{'name': name, 'type': type(obj).__name__, 
                 'size': sys.getsizeof(obj),
                 'value': str(obj)[:100] + '...' if isinstance(obj, (str, list, dict, tuple, set)) else obj}
                for name, obj in other_objects.items()]

    return str(obj_info)


def log_experiment(recall_experimento, algoritmos, additional_info=None):
    # Generate experiment ID
    id_experimento = generate_experiment_id()

    # Get DataFrames in memory
    tablas_en_memoria = get_dataframes_in_memory()

    # Get objets in memory
    objetos_en_memoria = get_other_objects_in_memory()

    # Get current date and time
    fecha = datetime.now()

    # Create a DataFrame with the log details
    log_details = pd.DataFrame({
        'id_experimento': [id_experimento],
        'recall_experimento': [recall_experimento],
        'algoritmos': [algoritmos],
        'fecha': [fecha],
        'tablas_en_memoria': [tablas_en_memoria],
        'objetos_en_memoria': [objetos_en_memoria],
        'additional_info': [additional_info]
    })

    # Create a path to the general folder
    cwd = os.getcwd()
    root_dir = os.path.dirname(cwd)
    os.chdir(root_dir)

    # Define the log directory and file
    log_dir = '01data/04log_experiments'
    log_file = 'experiment_log.parquet'

    # Check if the log directory exists, if not create it
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Check if the log file exists
    log_path = os.path.join(log_dir, log_file)
    if os.path.exists(log_path):
        # If it exists, read the existing log file
        existing_log = pd.read_parquet(log_path)

        # Append the new log details to the existing log
        log = pd.concat([existing_log, log_details], ignore_index=True)
    else:
        # If it doesn't exist, create a new log
        log = log_details

    # Write the log to a parquet file
    print(log_path)
    log.to_parquet(log_path)
    os.chdir(cwd)

    return log

# Use the function to log an experiment
# log = log_experiment(0.5, ['SVD'], 'This is a test experiment.')
