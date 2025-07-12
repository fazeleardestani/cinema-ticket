import json

def data_dump(file_path:str , data:list):
    """Saves a dictionary to a JSON file."""
    with open(file_path,'w') as file:
        json.dump(data, file, indent=4)

def data_load(file_path:str):
    """Loads a dictionary from a JSON file."""
    with open(file_path) as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {}

