import json
from time import sleep

read_files: dict = {}

SCOREBOARD_MAX_LENGTH: int = 20

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


def get_file_data(file_path: str, profile: str="", data_path: str="") -> dict:
    if file_path not in read_files.keys():
        read_files[file_path] = read_json_file(file_path)
    
    data = read_files[file_path]
    
    if profile:
        data = data[profile]
    if data_path:
        data = data[data_path]
    
    return data


def write_to_scoreboard(name: str, info: dict, filename='scoreboard.json', path='Scores', position=None):
    try:
        with open(filename, 'r+') as scoreboard:
            # Loads data from the scoreboard file.
            scoreboard_data = json.load(scoreboard)

            # Writes to this data.
            #scoreboard_data[path][name] = info
            new_entry = {"Name": name}
            new_entry.update(info)
            if position:
                scoreboard_data[path].insert(position, new_entry)
            else:
                scoreboard_data[path].append(new_entry)

            # Sorts the scoreboard by score in descending order.c
            scoreboard_data[path].sort(key=lambda x: x["Score"], reverse=True)
            
            # Trims the scoreboard if necessary
            if len(scoreboard_data[path]) > SCOREBOARD_MAX_LENGTH and SCOREBOARD_MAX_LENGTH > 0:
                scoreboard_data[path].pop(-1)

            # Adds it back to the scoreboard file.
            scoreboard.seek(0)
            json.dump(scoreboard_data, scoreboard, indent=3)

    except FileNotFoundError:
        print("ERROR: File path doesn't exist")
        return
    except json.JSONDecodeError:
        print(f"ERROR: Invalid JSON format in file: {filename}")
        return