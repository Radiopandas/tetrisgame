from tetromino import Tetromino
from utility_funcs import get_range
import rotation
from keyboard import is_pressed
from time import sleep

ghost_piece: Tetromino = None

width: int = 0
height: int = 0

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


def update_ghost_piece(grid, focused_tet: Tetromino, ghost_tiles: list):
    global ghost_piece
    # Initialises a ghost piece if there isn't one
    if not ghost_piece:
        ghost_piece = Tetromino([])
    
    # Deletes its cells
    for cell in ghost_piece.cells:
        x, y = cell[0], cell[1]
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

def get_movement(grid: list[list[bool]], focused_tet: Tetromino, cell_owners):
    if is_pressed("a"):
        move_tet(grid, focused_tet, cell_owners, -1)
        return True
    if is_pressed("d"):
        move_tet(grid, focused_tet, cell_owners, 1)
        return True
    if is_pressed("e"):
        rotation.rotate_tet(grid, focused_tet, cell_owners, True)
        return True
    if is_pressed("q"):
        rotation.rotate_tet(grid, focused_tet, cell_owners, False)
        return True
    if is_pressed("w"):
        quick_drop(grid, focused_tet, cell_owners, True)
        return True
    if is_pressed("s"):
        quick_drop(grid, focused_tet, cell_owners, False)