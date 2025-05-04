from tetromino import Tetromino
import utility_funcs
import rotation
from copy import deepcopy
import pygame

pygame.init()

ghost_piece: Tetromino

width: int = 0
height: int = 0

var_defaults = [None, 0, 0]

def reset():
    """Resets all necessary local variables."""
    global ghost_piece, width, height, var_defaults

    ghost_piece, width, height = var_defaults

def set_grid_size(_width: int, _height: int):
    """Called from 'main.py' to tell 'movement.py' the play area size."""
    global height, width
    height = _height
    width = _width


def move_tet(
        grid: list[list[bool]], 
        tetromino: Tetromino, 
        cell_owners: list[list[Tetromino | None]], 
        direction: int
    ) -> None:
    """Attempts to move a tetromino left or right, based on 'direction'."""
    
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


def quick_drop(
        grid: list[list[bool]], 
        focused_tet: Tetromino, 
        cell_owners: list[list[Tetromino | None]], 
        hard_drop: bool = True
    ):
    """Drops the focused piece downwards, either by one cell or fully."""
    cur_cells = focused_tet.cells

    focused_tet.can_move = True
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


def get_movement(grid, focused_tet: Tetromino, cell_owners):
    """Used to get keyboard inputs that can be repeated by being held down."""
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        move_tet(grid, focused_tet, cell_owners, -1)
        return True
    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        move_tet(grid, focused_tet, cell_owners, 1)
        return True
    elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
        quick_drop(grid, focused_tet, cell_owners, False)
        return True


def pygame_event_handler(event, grid, focused_tet: Tetromino, cell_owners, piece_sequence: list[int], all_tets: list[Tetromino]) -> bool:
    """Used to get keyboard inputs that can't be repeated by being held down"""
    if event.key == pygame.K_e:
        rotation.rotate_tet(grid, focused_tet, cell_owners, True)
        return True
    elif event.key == pygame.K_q:
        rotation.rotate_tet(grid, focused_tet, cell_owners, False)
        return True
    elif event.key == pygame.K_w or event.key == pygame.K_UP:
        quick_drop(grid, focused_tet, cell_owners, True)
        return True
    elif event.key == pygame.K_h:
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
        return True

    return False

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


# Function used for the attractor.
def process_given_input(
        event: str, 
        grid: list[list[bool]],
        focused_tet: Tetromino, 
        cell_owners: list[list[Tetromino | None]], 
        piece_sequence: list[int], 
        all_tets: list[Tetromino],
        ghost_tiles: list[list[bool]]
    ):
    """Simulates playing the game by being fed a series of inputs."""
    match event:
        case "a":
            move_tet(grid, focused_tet, cell_owners, -1)
        case "d":
            move_tet(grid, focused_tet, cell_owners, 1)

        case "w":
            quick_drop(grid, focused_tet, cell_owners, True)
        case "s":
            quick_drop(grid, focused_tet, cell_owners, False)
        
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
            return

    # Updates the ghost piece after every change.
    update_ghost_piece(grid, focused_tet, ghost_tiles)


