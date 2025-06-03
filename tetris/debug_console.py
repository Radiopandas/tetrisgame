"""
Name: debug_console.py
Created on: 28/05/2025
Description: Stores a list of booleans representing debug modes/special modes. Also contains a console for entering commands.
"""
# Imports required for changing certain variables.
#import input_handling

# Imports required for the actual input part of the console.
from input_box import InputBox
#from input_handling import repeatable_key_cooldown
import pygame
pygame.init()

###################################################################################################
#------------------------------------------ Global vars ------------------------------------------#
###################################################################################################

# Screen info.
display_info = pygame.display.Info()
screen_w = 640
screen_h = 360
screen_scale = display_info.current_w // screen_w

console_visible: bool = False

# Grid info
grid_width: int = 0
grid_height: int = 0
cell_width: int = 0

# Console modes and stuff
# ----------------------------------------------------------
debug_mode: bool = False
""" Debug mode:
0: Disabled.
1: Enabled, only spawns line pieces. Does not replace current queued pieces.
"""

colour_mode: int = 0
""" Colour modes:
0: Default tetris colour scheme.
1: Gradient colours.
2: DodgerBlue everything.
3: Everything flashes the same, random colour.
4: Every cell flashes its own, random colour.
5: Every piece flashes its own, random colour.
"""

draw_mode: int = 0
""" Draw modes:
0: Default draw mode.
1: Draws a background image.
2: Default, except circles.
"""

background_image: pygame.Surface = pygame.image.load(".\images\purple_monkey_dishwasher.jpg")

input_cooldown_time: float = 0.12
single_input_cooldowns: bool = True
# ----------------------------------------------------------

# Stuff for the actual console.
command_input_box = InputBox(
    screen_w * screen_scale // 2, 
    screen_h * screen_scale // 2, 
    64 * screen_scale, 
    prompt = "", 
    font_size = 32*screen_scale
)
command_input_box.centred_text = True
#command_input_box.rect.width += 250 * screen_scale
command_input_box.rect.width = screen_w * screen_scale
command_input_box.rect.centery = 16 * screen_scale
command_input_box.rect.centerx = screen_w * screen_scale // 2

###################################################################################################
#--------------------------------------- Utility functions ---------------------------------------#
###################################################################################################

def change_debug_mode(command_value: str):
    # Tries to convert the passed value to an int.
    try:
        command_value = int(command_value)
    except ValueError:
        print("Invalid command value")
        return

    global debug_mode
    debug_mode = True if command_value == 1 else False

def set_colour_mode(command: str):
    # Tries to convert the passed value to an int.
    command_value: int
    try:
        command_value = int(command)
    except ValueError:
        print("Invalid command value")
        return
    
    global colour_mode
    if 0 <= command_value <= 5:
        colour_mode = command_value


def set_drawing_mode(command: str):
    command_value: int
    try:
        command_value = int(command)
    except ValueError:
        print("Invalid command value")
        return
    
    global draw_mode
    if 0 <= command_value < 3:
        draw_mode = command_value

def set_background_image(command: str):
    image: pygame.Surface

    try:
        image = pygame.image.load(command)
        image = pygame.transform.scale(image, (grid_width * cell_width, grid_height * cell_width))
        global background_image
        background_image = image

    except FileNotFoundError:
        print("File not found")
        return

def set_repeatable_input_cooldowns(command: str):
    command_value: float
    try:
        command_value = float(command)
    except ValueError:
        print("Invalid command value")
        return
    global input_cooldown_time
    if 0 <= command_value:
        input_cooldown_time = command_value

def set_singular_input_cooldowns(command: str):
    command_value: int
    try:
        command_value = int(command)
    except ValueError:
        print("Invalid command value")
        return
    
    global single_input_cooldowns
    if command_value in [0, 1]:
        single_input_cooldowns = True if command_value == 1 else False


###################################################################################################
#---------------------------------------- Setup functions ----------------------------------------#
###################################################################################################

def set_grid_size(_grid_width: int, _grid_height: int, _cell_width: int):
    global grid_width, grid_height, cell_width, background_image
    grid_width = _grid_width
    grid_height = _grid_height
    cell_width = _cell_width

    if background_image:
        background_image = pygame.transform.scale(background_image, (grid_width * cell_width, grid_height * cell_width))

###################################################################################################
#---------------------------------------- Main functions -----------------------------------------#
###################################################################################################

def handle_command(input: str):

    split_command = input.split()

    if len(split_command) > 1:
        command, command_value = split_command
    else:
        return
    match command:
        case "setdebugmode":
            change_debug_mode(command_value)
        case "setcolourmode":
            set_colour_mode(command_value)
        case "setdrawmode":
            set_drawing_mode(command_value)
        case "setbackgroundimage":
            set_background_image(command_value)
        case "setrepeatablecooldown":
            set_repeatable_input_cooldowns(command_value)
        case "setsingularcooldown":
            set_singular_input_cooldowns(command_value)

def draw_console(screen: pygame.Surface):
    command_input_box.visible = True
    command_input_box.draw(screen)
