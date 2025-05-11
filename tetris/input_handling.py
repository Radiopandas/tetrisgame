from tetromino import Tetromino
import rotation
from json_parser import get_file_data
import pygame
import movement


pygame.init()

###################################################################################################
#------------------------------------------ Global vars ------------------------------------------#
###################################################################################################
# Maps pygame inputs to strings
input_map: dict = {
    pygame.K_a: "move_left",
    pygame.K_d: "move_right",
    pygame.K_w: "hard_drop",
    pygame.K_s: "soft_drop",
    pygame.K_e: "rotate_right",
    pygame.K_q: "rotate_left",
    pygame.K_h: "hold_piece"
}
# Maps strings to functions to be called
action_map: dict = {
    "move_left": movement.move_tet,
    "move_right": movement.move_tet,
    "hard_drop": movement.quick_drop,
    "soft_drop": movement.quick_drop,
    "rotate_right": rotation.rotate_tet,
    "rotate_left": rotation.rotate_tet,
    "hold_piece": movement.hold_piece
}

valid_events: list = get_file_data('settings.json', 'pygame_events_details', 'valid_events')

repeatable_inputs: list = ["move_left", "move_right", "soft_drop"]

###################################################################################################
#---------------------------------------- Setup functions ----------------------------------------#
###################################################################################################

def initialise_input_map(file_path: str, profile: str, data_path: str):
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
    for key, value in input_map.items():
        if value == action:
            input_map.pop(key)
            input_map[new_input] = action
            return True
    
    return False

###################################################################################################
#---------------------------------------- Main functions -----------------------------------------#
###################################################################################################

def get_repeatable_inputs(
        grid: list[list[bool]],
        cell_owners: list[list[Tetromino | None]],
        focused_tet: Tetromino
    ) -> bool:

    # Maps strings to function arguments to be used with 'action_map'.
    action_args: dict[str, list] = {
        "move_left": [grid, focused_tet, cell_owners, -1],
        "move_right": [grid, focused_tet, cell_owners, 1],
        "soft_drop": [grid, focused_tet, cell_owners, False]
    }

    movement_occured = False
    pressed_keys = pygame.key.get_pressed()
    for key in input_map.keys():
        if pressed_keys[key]:
            if input_map[key] in repeatable_inputs:
                action_name = input_map[key]
                action = action_map[action_name]
                args: list = action_args[action_name]
                action(*args)
                movement_occured = True
    
    return movement_occured


def handle_pygame_events(
        event, 
        grid: list[list[bool]], 
        cell_owners: list[list[Tetromino | None]],
        focused_tet: Tetromino, 
        piece_sequence: list[int], 
        all_tets: list[Tetromino]
    ) -> bool:
    # Maps strings to function arguments to be used with 'action_map'.
    action_args: dict = {
        "hard_drop": [grid, focused_tet, cell_owners, True],
        "rotate_right": [grid, focused_tet, cell_owners, True],
        "rotate_left": [grid, focused_tet, cell_owners, False],
        "hold_piece": [grid, cell_owners, all_tets, focused_tet, piece_sequence]
    }

    # Iterates through the entire input map, checking if each input has been pressed.
    if event.key in input_map.keys():
        if input_map[event.key] not in repeatable_inputs:
            action_name = input_map[event.key]
            action = action_map[action_name]
            args: list = action_args[action_name]
            action(*args)
            return True
    
    return False


def attractor_input_processor(
        event,
        grid: list[list[bool]],
        cell_owners: list[list[Tetromino | None]],
        focused_tet: Tetromino
    ):
    match event:
        case "a":
            movement.move_tet(grid, focused_tet, cell_owners, -1)
        case "d":
            movement.move_tet(grid, focused_tet, cell_owners, 1)

        case "w":
            movement.quick_drop(grid, focused_tet, cell_owners, True)
        case "s":
            movement.quick_drop(grid, focused_tet, cell_owners, False)

        case "e":
            rotation.rotate_tet(grid, focused_tet, cell_owners, True)
        case "q":
            rotation.rotate_tet(grid, focused_tet, cell_owners, False)

        case "h":
            print("Sorry, holding not implemented yet.")
        case _:
            # Allows the attractor to have delays between steps.
            # Returns to prevent update_ghost_piece() being called.
            print("Stalling for a tick.")
            return False
    return True


def handle_button_presses(button):
    pass