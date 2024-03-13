import importlib
import inspect
import os
from myutils.type_library import ClassObject

def get_classes_from_folder(folder_path) -> dict[str, type]:
    # Get the absolute path of the folder
    abs_folder_path = os.path.abspath(folder_path)

    # Initialize a dictionary to store the classes
    classes_dict = {}

    # Iterate through all files in the folder
    for file_name in os.listdir(abs_folder_path):
        # Check if the file is a Python file
        if file_name.endswith(".py"):
            # Import the module dynamically
            module_name = file_name[:-3]  # Remove the ".py" extension
            module_path = f"models.{module_name}"

            try:
                module = importlib.import_module(module_path)
            except ImportError as e:
                print(f"Error importing module {module_path}: {e}")
                continue

            # Iterate through members of the module
            for _, member in inspect.getmembers(module):
                # Check if the member is a class and not an imported module
                if inspect.isclass(member) and member.__module__ == module.__name__:
                    classes_dict[module_name] = member
    return classes_dict

import models.anniversary