import json

read_files: dict = {}

def read_json_file(file_path: str) -> dict:
    try:
        with open (file_path, 'r') as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        print("ERROR: File path doesn't exist")
        return {}
    except json.JSONDecodeError:
        print(f"ERROR: Invalid JSON format in file: {file_path}")
        return {}

def get_file_data(file_path: str, data_path: str) -> dict:
    if file_path not in read_files.keys():
        read_files[file_path] = read_json_file(file_path)
    
    data = read_files[file_path]
    return data[data_path]

