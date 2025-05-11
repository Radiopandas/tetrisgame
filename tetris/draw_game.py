"""
Filename: draw_game.py
Last updated: 5/05/2025
Description: Python script containing various functions to draw the game
in a seperate window using pygame.
"""
import utility_funcs
import pygame
from tetromino import Tetromino
import json_parser
import draw_start_menu
import draw_main_game
import draw_buttons
import draw_settings_menu

import movement

width: int = 0
height: int = 0


def set_grid_size(_width: int, _height: int):
    """Called from 'main.py' to tell 'draw_game.py' the play_area size."""
    global height, width
    height = _height
    width = _width


# Some setup stuff for pygame.
pygame.init()

# Sets up the screen.
screen_info = pygame.display.Info()
screen_w = screen_info.current_w
screen_h = screen_info.current_h

#screen = pygame.display.set_mode((1920, 1080))
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption("SIRTET")

cell_width: int = 0

# Sets up the fonts.
base_font = None
base_font_size: int = 0

title_font = None
title_font_size: int = 100

piece_display_font = None
piece_display_font_size: int = 50

controls_font = None
controls_font_size: int = 50

controls_title_font = None
controls_title_font_size: int = 70



background_colour = pygame.Color(0, 0, 0)

var_defaults = [0, 0, 0, 0, None]

game_controls: dict = {}

start_menu_initialised = False
main_game_initialised = False
settings_initialised = False

###################################################################################################
#--------------------------------------- Utility Functions ---------------------------------------#
###################################################################################################

game_controls = json_parser.get_file_data('settings.json', "Profile1", "displayed_controls")

def reset():
    """Resets all necessary local global variables."""
    global width, height, cell_width, base_font_size, base_font, var_defaults

    width, height, cell_width, base_font_size, base_font = var_defaults


def print_grid(
        grid: list[list[bool]], 
        ghost_tiles: list[list[bool]]
    ):
    """Prints the Tetris game in the terminal using box drawing characters."""
    print("\033c")
    print("┏" + "━━" * len(grid[0]) + "┓")
    for y, row in enumerate(grid):
        print('┃', end="")
        for x, cell in enumerate(row):
            if cell:
                print("██", end="")
            else:
                if ghost_tiles[y][x]:
                    print("██", end="")
                else:
                    print("  ", end="")
        print('┃')
    
    print("┗" + "━━" * len(grid[0]) + "┛")

###################################################################################################
#---------------------------------- Main Game Drawing Functions ----------------------------------#
###################################################################################################

def buttons():
    global settings_initialised
    
    if not settings_initialised:
        settings_initialised = True
        draw_settings_menu.initialise_settings_buttons()
    
    if draw_settings_menu.settings_menu_open:
        draw_settings_menu.draw_settings_menu(screen)

    draw_buttons.draw_buttons(screen)


def main_game(
        grid: list[list[bool]],
        cell_owners: list[list[Tetromino | None]], 
        board_offset: int, 
        ghost_tiles: list[list[bool]], 
        score: int, 
        lines_cleared: int, 
        piece_sequence: list[int],
        all_tets: list[Tetromino],
        held_piece: int = None,
        draw_ghost_piece: bool = True
    ) -> None:
    """Calls several other functions to draw everything onto the screen."""

    global game_controls, main_game_initialised

    #draw_grid(grid, cell_owners, board_offset, ghost_tiles, 5)
    if not main_game_initialised:
        main_game_initialised = True
        draw_main_game.set_grid_size(10, 22)
        draw_main_game.initialise_base_font(16)
        draw_main_game.initialise_controls_font(16)
        draw_main_game.initialise_piece_display_font(16)
        draw_main_game.initialise_controls_title_font(24)
    
    draw_main_game.draw_grid(screen, all_tets, movement.ghost_piece, 5, draw_ghost_piece)

    draw_main_game.draw_stats(screen, score, lines_cleared, lines_cleared // 10)

    draw_main_game.draw_next_pieces(screen, piece_sequence[0:3])

    draw_main_game.draw_held_piece(screen, held_piece)

    #draw_main_game.draw_controls(screen, game_controls)

    buttons()
    


def start_menu() -> bool:
    """Draws a start menu consisting of the title and basic instructions."""
    
    global start_menu_initialised
    if not start_menu_initialised:
        start_menu_initialised = True
        draw_start_menu.initialise_title_font(33)
        draw_start_menu.initialise_instructions_font(33)

    draw_start_menu.draw_start_menu(screen)

    #draw_grid_lines(20)

    # Checks for the user pressing <key> to exit the start screen.
    # Returns True if <key> is pressed, else False. 

    buttons()

"""    keys = pygame.key.get_pressed()
    if keys[pygame.K_0]:
        return True
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                return True
"""
    


def draw_grid_lines(h_lines: int):
    """Draws a grid on the screen in solid black lines for the sake
    of more easily aligning visual elements."""
    spacing = screen_w // h_lines

    v_lines = screen_h // spacing

    # Draws all the horizontal lines.
    for x in range(h_lines):
        pygame.draw.line(screen, (0, 0, 0), (spacing * x, 0), (spacing * x, screen_h), width = 5)
    
    # Draws all the vertical lines.
    for y in range(v_lines):
        pygame.draw.line(screen, (0, 0, 0), (0, spacing * y), (screen_w, spacing * y), width = 5)
    
    # Prints the position of a mouse click to allow for easier calculations.
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())
            print()
            pass



###################################################################################################
#------------------------------------------- TODO LIST -------------------------------------------#
###################################################################################################

"""
Left edge: 100
Right edge 461

Top: 133
Bottom 525
Bottom of text: 485

Add 50 to the horizontal ones
871
904

"""