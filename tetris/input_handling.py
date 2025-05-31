from tetromino import Tetromino
import rotation
from json_parser import get_file_data
from draw_buttons import Button
import debug_console
import pygame
import movement

pygame.init()

###################################################################################################
#------------------------------------------ Global vars ------------------------------------------#
###################################################################################################
SETTINGS_PROFILE: str = 'Profile1'

# Maps pygame inputs to strings
input_map: dict = {}
# Used to prevent move_left and move_right both being pressed.
left_key: int
right_key: int

# Actually initialises the input map from the settings file.
inputs = get_file_data('settings.json', SETTINGS_PROFILE, 'controls')
for action, key in inputs.items():
    if action == "move_left":
        left_key = key
    elif action == "move_right":
        right_key = key
    
    input_map[action] = key

# Gets a seperate map of what to display for each action, such as
# 'left' and 'right' to represent actions bound to arrow keys.
input_display: dict = get_file_data('settings.json', SETTINGS_PROFILE, 'displayed_controls')
for key, value in input_map.items():
    print(f"Key: {key}, action: {value}, symbol: {input_display[key]}")


# Maps each action in the input map to its relevant function.
action_map: dict = {
    "move_left": movement.move_tet,
    "move_right": movement.move_tet,
    "hard_drop": movement.hard_drop,
    "soft_drop": movement.hard_drop,
    "rotate_right": rotation.rotate_tet,
    "rotate_left": rotation.rotate_tet,
    "hold_piece": movement.hold_piece
}

# List of what inputs the user is allowed to bind to actions.
# For the most part, allows all numbers, keys, symbols and arrow keys.
valid_events: list = get_file_data('settings.json', 'pygame_events_details', 'valid_events')

soft_dropping: bool = False
just_hard_dropped: bool = False

# Seperates all the actions into 'singular' and 'repeatable', which represents
# whether an action should be repeated if the key is held down.
singular_inputs: list = ["rotate_left", "rotate_right", "hold_piece", "hard_drop"]
repeatable_inputs: list = ["move_left", "move_right", "soft_drop"]

# Stores whether each 'singular' can be used. These values are set to true
# when an action is pressed, then set to false when they are released.
singular_key_cooldowns: dict[str, bool] = {
    "rotate_left": False, 
    "rotate_right": False, 
    "hold_piece": False, 
    "hard_drop": False,
}

# For each repeatable action, stores how long of a
# cooldown it has left before it can be used again.
repeatable_key_cooldowns: dict[str, float] = {
    "move_left": 0.0,
    "move_right": 0.0,
    "soft_drop": 0.0,
}
# How long, in seconds, of a cooldown there should be before repeating actions.
repeatable_key_cooldown: float = 0.12

###################################################################################################
#---------------------------------------- Setup functions ----------------------------------------#
###################################################################################################

def reset_input_map(file_path: str, profile: str, data_path: str):
    pass

###################################################################################################
#--------------------------------------- Utility functions ---------------------------------------#
###################################################################################################

def event_is_valid_control(event: pygame.event.Event):
    """Returns whether an inputted key is valid and available
    to be mapped to an input."""
    # Checks if the given event is already bound to something.
    for input in input_map.keys():
        if input == event.key:
                return False
    
    if event.unicode:
        if event.unicode.lower() in valid_events:
            return True
    else:
        if event.key in valid_events:
            return True
    return False


def update_input_map(new_input, action: str):
    global left_key, right_key
    for key, value in input_map.items():
        if key == action:
            input_map.pop(key)
            input_map[action] = new_input
            if action == "move_left":
                left_key = new_input
            elif action == "move_right":
                right_key = new_input
            return True
    
    return False

###################################################################################################
#---------------------------------------- Main functions -----------------------------------------#
###################################################################################################

def update_cooldowns(delta_time: float):
    for key, cooldown in repeatable_key_cooldowns.items():
        if cooldown > 0:
            repeatable_key_cooldowns[key] -= delta_time
            if repeatable_key_cooldowns[key] < 0:
                repeatable_key_cooldowns[key] = 0


def get_inputs(
        grid: list[list[bool]], 
        cell_owners: list[list[Tetromino | None]],
        focused_tet: Tetromino, 
        piece_sequence: list[int], 
        all_tets: list[Tetromino]
    ):

    global just_hard_dropped, repeatable_key_cooldown

    action_args: dict = {
        "hard_drop": [grid, focused_tet, cell_owners, True],
        "rotate_right": [grid, focused_tet, cell_owners, True],
        "rotate_left": [grid, focused_tet, cell_owners, False],
        "hold_piece": [grid, cell_owners, all_tets, focused_tet, piece_sequence],
        "move_left": [grid, focused_tet, cell_owners, -1],
        "move_right": [grid, focused_tet, cell_owners, 1],
        "soft_drop": [grid, focused_tet, cell_owners, False],
    }

    # Checks the tetromino should be able to move.
    if focused_tet.locking_frame == focused_tet.MAX_LOCKING_FRAME:
        return
    
    pressed_keys = pygame.key.get_pressed()

    # If any key in the input map is pressed, gets set to True
    # so that the ghost piece gets updated.
    action_happened: bool = False

    for action_name, key in input_map.items():
        # Repeatable and non-repeatable events work differently
        # and are therefore handled seperately.
        if action_name in repeatable_inputs:
            if pressed_keys[key] and repeatable_key_cooldowns[action_name] == 0:
                # Prevents left and right being pressed.
                if action_name == "move_left" and pressed_keys[right_key]:
                    continue
                elif action_name == "move_right" and pressed_keys[left_key]:
                    continue
                
                action = action_map[action_name]
                args = action_args[action_name]
                action(*args)
                action_happened = True
                # Note: Takes the cooldown from the debug console because
                # it is easier to change it there than it is to fix the
                # import issues when I try to import this module from the console.
                repeatable_key_cooldowns[action_name] = debug_console.input_cooldown_time
            
        else:
            if pressed_keys[key]:
                if not singular_key_cooldowns[action_name]:
                    action = action_map[action_name]
                    args: list = action_args[action_name]
                    action(*args)
                    if action_name == "hard_drop":
                        just_hard_dropped = True
                        singular_key_cooldowns[action_name] = debug_console.single_input_cooldowns
                        # Breaks out of the input handling loop to avoid issues
                        # with hard drop and hold piece being bound to the same key.
                        break
                    
                    singular_key_cooldowns[action_name] = debug_console.single_input_cooldowns
            
            # If the key isn't pressed, resets its 'cooldown'.
            else:
                singular_key_cooldowns[action_name] = False

    return action_happened


def attractor_input_processor(
        event,
        grid: list[list[bool]],
        cell_owners: list[list[Tetromino | None]],
        focused_tet: Tetromino
    ):

    global just_hard_dropped

    match event:
        case "a": # Move left
            movement.move_tet(grid, focused_tet, cell_owners, -1)
        case "d": # Move right
            movement.move_tet(grid, focused_tet, cell_owners, 1)

        case "w": # Hard drop
            movement.hard_drop(grid, focused_tet, cell_owners, True)
            just_hard_dropped = True
        case "s": # Soft drop
            soft_dropping = True

        case "e": # Rotate right
            rotation.rotate_tet(grid, focused_tet, cell_owners, True)
        case "q": # Rotate left
            rotation.rotate_tet(grid, focused_tet, cell_owners, False)

        case "h": # Hold piece
            print("Sorry, holding not implemented yet.")
        case _:
            # Allows the attractor to have delays between steps.
            # Returns to prevent update_ghost_piece() being called.
            print("Stalling for a tick.")
            return False
    return True


def reset_controls(controls_buttons: list[Button]):
    global input_map, input_display, left_key, right_key

    # Resets the input map to the defaults
    input_map = {}
    inputs = get_file_data('settings.json', SETTINGS_PROFILE, 'controls')
    for action, key in inputs.items():
        if action == "move_left":
            left_key = key
        elif action == "move_right":
            right_key = key
        input_map[action] = key

    # Updates all the controls buttons to display the default symbols.
    for button in controls_buttons:
        # Disregards the last 4 characters, since they are always '_btn'
        name = button.button_name[0:-4]
        button.button_symbol = input_display[name]