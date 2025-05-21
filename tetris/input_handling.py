from tetromino import Tetromino
import rotation
from json_parser import get_file_data
from draw_buttons import Button
import pygame
import movement




pygame.init()

###################################################################################################
#------------------------------------------ Global vars ------------------------------------------#
###################################################################################################
# Maps pygame inputs to strings
input_map: dict = {
    121: "move_left",
    pygame.K_d: "move_right",
    pygame.K_w: "hard_drop",
    pygame.K_s: "soft_drop",
    pygame.K_e: "rotate_right",
    pygame.K_q: "rotate_left",
    pygame.K_h: "hold_piece"
}
# Used to prevent move_left and move_right both being pressed.
left_key: int
right_key: int

input_map = {}
inputs = get_file_data('settings.json', 'Profile1', 'controls')
for action, key in inputs.items():
    if action == "move_left":
        left_key = key
    elif action == "move_right":
        right_key = key
    
    input_map[key] = action

## Maps 
input_display: dict = get_file_data('settings.json', 'Profile1', 'displayed_controls')
for key, value in input_map.items():
    print(f"Key: {key}, action: {value}, symbol: {input_display[value]}")

# Maps strings to functions to be called
action_map: dict = {
    "move_left": movement.move_tet,
    "move_right": movement.move_tet,
    "hard_drop": movement.hard_drop,
    "soft_drop": movement.hard_drop,
    "rotate_right": rotation.rotate_tet,
    "rotate_left": rotation.rotate_tet,
    "hold_piece": movement.hold_piece
}


valid_events: list = get_file_data('settings.json', 'pygame_events_details', 'valid_events')


singular_inputs_states: dict = {
    "rotate_left": False, 
    "rotate_right": False, 
    "hold_piece": False, 
    "hard_drop": False,
}

soft_dropping: bool = False

just_hard_dropped: bool = False

singular_inputs: list = ["rotate_left", "rotate_right", "hold_piece", "hard_drop"]
singular_key_cooldowns: dict[str, bool] = {
    "rotate_left": False, 
    "rotate_right": False, 
    "hold_piece": False, 
    "hard_drop": False,
}

repeatable_inputs: list = ["move_left", "move_right", "soft_drop"]
repeatable_key_cooldowns: dict[str, float] = {
    "move_left": 0.0,
    "move_right": 0.0,
    "soft_drop": 0.0,
}

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
        if event.unicode in valid_events:
            return True
    else:
        if event.key in valid_events:
            return True
    return False


def update_input_map(new_input, action: str):
    global left_key, right_key
    for key, value in input_map.items():
        if value == action:
            input_map.pop(key)
            input_map[new_input] = action
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

    global just_hard_dropped

    action_args: dict = {
        "hard_drop": [grid, focused_tet, cell_owners, True],
        "rotate_right": [grid, focused_tet, cell_owners, True],
        "rotate_left": [grid, focused_tet, cell_owners, False],
        "hold_piece": [grid, cell_owners, all_tets, focused_tet, piece_sequence],
        "move_left": [grid, focused_tet, cell_owners, -1],
        "move_right": [grid, focused_tet, cell_owners, 1],
        "soft_drop": [grid, focused_tet, cell_owners, False],
    }
    pressed_keys = pygame.key.get_pressed()

    # If any key in the input map is pressed, gets set to True
    # so that the ghost piece gets updated.
    action_happened: bool = False

    for key, action_name in input_map.items():
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
                repeatable_key_cooldowns[action_name] = 0.12
            
        else:
            if pressed_keys[key]:
                if not singular_key_cooldowns[action_name]:
                    action = action_map[action_name]
                    args: list = action_args[action_name]
                    action(*args)
                    if action_name == "hard_drop":
                        just_hard_dropped = True
                    
                    singular_key_cooldowns[action_name] = True
            
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
    global input_map, input_display

    # Resets the input map to the defaults
    input_map = {}
    inputs = get_file_data('settings.json', 'Profile1', 'controls')
    for key, value in inputs.items():
        input_map[value] = key

    # Updates all the controls buttons to display the default symbols.
    for button in controls_buttons:
        name = button.button_name[0:-4]
        button.button_symbol = input_display[name]