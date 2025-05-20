from tetromino import Tetromino
import utility_funcs
import rotation
import json_parser
from copy import deepcopy
import pygame

pygame.init()

ghost_piece: Tetromino

width: int = 0
height: int = 0

var_defaults = [None, 0, 0]

SETTINGS_PATH = 'settings.json'
CONTROLS_PATH = 'controls'
CONTROLS_PRESET = 'Profile1'

controls = json_parser.get_file_data(SETTINGS_PATH, CONTROLS_PRESET, CONTROLS_PATH)


def reset():
    """Resets all necessary local variables."""
    global ghost_piece, width, height, var_defaults

    ghost_piece, width, height = var_defaults

def set_grid_size(_width: int, _height: int):
    """Called from 'main.py' to tell 'movement.py' the play area size."""
    global height, width
    height = _height
    width = _width


def check_keys(pressed_keys, controls: list) -> bool:
    for control in controls:
        if pressed_keys[control]:
            return True
    
    return False


def move_tet(
        grid: list[list[bool]], 
        tetromino: Tetromino, 
        cell_owners: list[list[Tetromino | None]], 
        direction: int
    ) -> None:
    """Attempts to move a tetromino left or right, based on 'direction'."""
    
    if not tetromino.can_move:
        return
    cur_cells = tetromino.cells
    can_move: bool = True
    # Checks if the cells in 'direction' are clear.
    for cell in cur_cells:
        x, y = cell[0], cell[1]
        # Checks if moving in 'direction' would put 'tetromino' out of bounds.
        if not (0 <= (x + direction) < width):
            can_move = False
            break
        
        # Checks if a different cell in 'tetromino' is in 'direction'.
        if [x + direction, y] in cur_cells:
            continue

        # Checks if the cell in 'direction' is occupied.
        if grid[y][x + direction]:
            can_move = False
            break
    
    # Updates the cells of 'tetromino' to move it in 'direction'.
    if can_move:
        # Creates a list of the new cells and clears them out.
        new_cells: list = []
        for cell in cur_cells:
            x, y = cell[0], cell[1]
            grid[y][x] = False
            cell_owners[y][x] = None
            new_cells.append([x + direction, y])
        
        # Applies these changes and marks them on 'grid' and 'cell_owners'.
        tetromino.cells = new_cells
        for cell in new_cells:
            x, y = cell[0], cell[1]
            grid[y][x] = True
            cell_owners[y][x] = tetromino


def hard_drop(
        grid: list[list[bool]], 
        focused_tet: Tetromino, 
        cell_owners: list[list[Tetromino | None]], 
        hard_drop: bool = True
    ):
    """Drops the focused piece downwards, either by one cell or fully."""
    cur_cells = focused_tet.cells

    #focused_tet.can_move = True
    focused_tet.has_moved = False

    can_drop: bool = True
    # Attempts to move the piece downwards.
    while can_drop:
        # By setting cur_cells every iteration, the piece can hard drop.
        # Otherwise, the second iteration will get blocked by the new piece.
        if hard_drop:
            cur_cells = focused_tet.cells
        
        # Iterates through every cell, checking if it can move downwards.
        can_move: bool = True
        for cell in cur_cells:
            x, y = cell[0], cell[1]
            if y == height - 1:
                can_move = False
                focused_tet.can_move = False
                break

            if [x, y + 1] in cur_cells:
                continue
            if grid[y + 1][x]:
                can_move = False
                break
        
        # If it can, updates the cells of 'focused_tet' to
        # reflect these changes.
        if can_move:
            new_cells = []
            for cell in cur_cells:
                x, y = cell[0], cell[1]
                grid[y][x] = False
                cell_owners[y][x] = None
                new_cells.append([x, y+1])
            
            focused_tet.cells = new_cells
            for cell in new_cells:
                x, y = cell[0], cell[1]
                grid[y][x] = True
                cell_owners[y][x] = focused_tet
        else:
            can_drop = False
    # Makes it so that after hard dropping, the piece can't continue moving.
    if hard_drop:
        focused_tet.can_move = False


def hold_piece(
        grid: list[list[bool]], 
        cell_owners: list[list[Tetromino | None]], 
        all_tets: list[Tetromino], 
        focused_tet: Tetromino, 
        piece_sequence: list[int]
    ) -> None:
    # Tries to hold the piece
    hold_successful = utility_funcs.hold_piece(piece_sequence, focused_tet)
    if hold_successful:
        # Clears it from the grid so it can be replaced by a new piece.
        utility_funcs.clear_tetromino(focused_tet, grid, all_tets, cell_owners)

        # Gets that new piece. Note: 'can_spawn' isn't currently used.
        can_spawn, new_tet_cells, new_tet_type = utility_funcs.generate_tetromino(grid, piece_sequence)
        focused_tet.cells = new_tet_cells
        focused_tet.tet_type = new_tet_type
        focused_tet.times_rotated = 0

        # Spawns the new piece in.
        utility_funcs.add_tetromino(focused_tet, grid, cell_owners)
    

def update_ghost_piece(grid, focused_tet: Tetromino, ghost_tiles: list):
    """Updates the position of the 'ghost piece' to show where the 
    current tile would land if hard dropped."""
    global ghost_piece

    # If the current piece can't move, it must be sitting on something.
    # Thus we don't need to draw the ghost piece.
    if not focused_tet.can_move:
        return
    if len(focused_tet.cells) == 0:
        return

    # Initialises a ghost piece if there isn't one
    if not ghost_piece:
        ghost_piece = Tetromino([])
    
    # Deletes its cells
    for y, row in enumerate(ghost_tiles):
        for x, cell in enumerate(row):
            if cell:
                ghost_tiles[y][x] = False
    
    # Creates a deepcopy so that modifying the ghost piece has no effect on
    # the actual tetromino.
    ghost_piece.cells = deepcopy(focused_tet.cells)

    # Gets the columns that the ghost piece is in.
    ghost_columns: list = []
    for cell in ghost_piece.cells:
        x = cell[0]
        if x not in ghost_columns:
            ghost_columns.append(x)
    
    # Gets the lowest ghost piece cell in each column.
    lowest_ghost_cells: dict = {}
    for cell in ghost_piece.cells:
        x, y = cell[0], cell[1]
        if x not in lowest_ghost_cells.keys():
            lowest_ghost_cells[x] = y
        else:
            if lowest_ghost_cells[x] < y:
                lowest_ghost_cells[x] = y
    
    # Gets the highest blocked cell in each column.
    ghost_column_heights: dict = {}
    for column in ghost_columns:
        y = lowest_ghost_cells[column]
        while y != height - 1 and not grid[y + 1][column]:
            if y == height - 2:
                y += 1
                break
            y += 1
        ghost_column_heights[column] = y
    
    # Calculates the height differences in each column.
    height_diffs: list = []
    for column in ghost_columns:
        height_diffs.append(
            ghost_column_heights[column] - 
            lowest_ghost_cells[column]
        )
    
    # Finds the minimum of these height differences, then moves
    # every cell down by that amount
    distance_to_move = min(height_diffs)
    new_cells: list = []
    for cell in ghost_piece.cells:
        x, y = cell[0], cell[1]
        new_cells.append([x, y + distance_to_move])
    
    # Updates the ghost piece with these changes.
    ghost_piece.cells = new_cells
    for cell in new_cells:
        x, y = cell[0], cell[1]
        ghost_tiles[y][x] = True