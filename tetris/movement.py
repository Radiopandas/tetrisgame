from tetromino import Tetromino
import utility_funcs
import rotation
from time import sleep
import main
import pygame

pygame.init()

ghost_piece: Tetromino = None

width: int = 0
height: int = 0

var_defaults = None, 0, 0

def reset():
    global ghost_piece, width, height, var_defaults

    ghost_piece, width, height = var_defaults

def set_grid_size(_width: int, _height: int):
    global height, width
    height = _height
    width = _width


def move_tet(grid, tetromino: Tetromino, cell_owners, direction: int):
    # Checks if the cells in 'direction' are clear
    cur_cells = tetromino.cells
    can_move: bool = True
    for cell in cur_cells:
        x, y = cell[0], cell[1]
        if not (0 <= (x + direction) < width):
            can_move = False
            break
        if [x + direction, y] in cur_cells:
            continue
        if grid[y][x + direction]:
            can_move = False
            break
    
    if can_move:
        new_cells: list = []
        for cell in cur_cells:
            x, y = cell[0], cell[1]
            grid[y][x] = False
            cell_owners[y][x] = None
            new_cells.append([x + direction, y])
        
        tetromino.cells = new_cells
        for cell in new_cells:
            x, y = cell[0], cell[1]
            grid[y][x] = True
            cell_owners[y][x] = tetromino


def quick_drop(grid, focused_tet: Tetromino, cell_owners, hard_drop: bool = True):
    cur_cells = focused_tet.cells

    focused_tet.can_move = True
    focused_tet.has_moved = False

    can_drop: bool = True
    while can_drop:
        # This means it can update the cells after every time it moves down
        # Thus allowing it to 'hard drop'
        if hard_drop:
            cur_cells = focused_tet.cells
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
    if hard_drop:
        focused_tet.can_move = False


def update_ghost_piece(grid, focused_tet: Tetromino, ghost_tiles: list):
    global ghost_piece
    # Initialises a ghost piece if there isn't one
    if not ghost_piece:
        ghost_piece = Tetromino([])
    
    # Deletes its cells
    #for cell in ghost_piece.cells:
    #    x, y = cell[0], cell[1]
    #    ghost_tiles[y][x] = False
    for y, row in enumerate(ghost_tiles):
        for x, cell in enumerate(row):
            if cell:
                ghost_tiles[y][x] = False

    ghost_piece.cells = focused_tet.cells
    
    # Attempts to drop it down
    can_drop: bool = True
    while can_drop:
        cur_cells = ghost_piece.cells
    
        can_move: bool = True
        for cell in cur_cells:
            x, y = cell[0], cell[1]
            if y == height - 1:
                can_move = False
                break
            if [x, y + 1] in cur_cells:
                continue
            if grid[y + 1][x]:
                can_move = False
                break
        
        if can_move:
            new_cells = []
            for cell in cur_cells:
                x, y = cell[0], cell[1]
                new_cells.append([x, y+1])
            
            ghost_piece.cells = new_cells
            for cell in new_cells:
                x, y = cell[0], cell[1]
        else:
            can_drop = False
    
    # Finally, sets its cells so it is visible
    for cell in ghost_piece.cells:
        x, y = cell[0], cell[1]
        ghost_tiles[y][x] = True

def get_movement_2(grid, focused_tet: Tetromino, cell_owners):
    """
    Used to get keyboard inputs that can be repeated by being held down.
    Similar to 'get_movement' except this uses 'pygame' instead of 'keyboard'
    to handle inputs
    """
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        move_tet(grid, focused_tet, cell_owners, -1)
        return True
    elif keys[pygame.K_d]:
        move_tet(grid, focused_tet, cell_owners, 1)
        return True
    elif keys[pygame.K_s]:
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
    elif event.key == pygame.K_w:
        quick_drop(grid, focused_tet, cell_owners, True)
        return True
    elif event.key == pygame.K_h:
        # Tries to hold the piece
        hold_successful = utility_funcs.hold_piece(piece_sequence, focused_tet)
        if hold_successful:
            print("Grid before calling \'clear_tetromino\'", end="")
            print(*grid, sep="\n")

            utility_funcs.clear_tetromino(focused_tet, grid, all_tets, cell_owners)

            print("Grid after calling \'clear_tetromino\'", end="")
            print(*grid, sep="\n")

            #sleep(10)

            can_spawn, new_tet_cells, new_tet_type = utility_funcs.generate_tetromino(grid, piece_sequence)
            focused_tet.cells = new_tet_cells
            focused_tet.tet_type = new_tet_type
            focused_tet.times_rotated = 0

            utility_funcs.add_tetromino(focused_tet, grid, cell_owners)
        return True

    return False

def update_ghost_piece_2(grid, focused_tet: Tetromino, ghost_tiles: list):
    global ghost_piece
    # Initialises a ghost piece if there isn't one
    if not ghost_piece:
        ghost_piece = Tetromino([])
    
    # Deletes its cells
    for y, row in enumerate(ghost_tiles):
        for x, cell in enumerate(row):
            if cell:
                ghost_tiles[y][x] = False
    
    ghost_piece.cells = focused_tet.cells

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
        height_diffs.append(ghost_column_heights[column] - lowest_ghost_cells[column])
    
    distance_to_move = min(height_diffs)
    new_cells: list = []
    for cell in ghost_piece.cells:
        x, y = cell[0], cell[1]
        new_cells.append([x, y + distance_to_move])
    
    ghost_piece.cells = new_cells
    for cell in new_cells:
        x, y = cell[0], cell[1]
        ghost_tiles[y][x] = True

    #print(f"Ghost columns: {ghost_columns}")
    #print(f"Lowest ghost cells: {lowest_ghost_cells}")
    #print(f"Ghost column heights: {ghost_column_heights}")
    #print(f"Ghost column height diffs: {height_diffs}")
    #sleep(10)




"""
New update_ghost_piece

For every column that has a ghost_tile, find the highest blocked cell
Find the distance between the lowest ghost tile in each column and this blocked cell
Find the minimum of these values, then move everything down by that amount

"""