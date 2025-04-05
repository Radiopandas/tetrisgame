from tetromino import Tetromino
from time import sleep   # Delete once done

width: int = 0
height: int = 0

def set_grid_size(_width: int, _height: int):
    global height, width
    height = _height
    width = _width

    print(f"Height: {height}")
    #sleep(2)

def try_move_down(grid, tetromino: Tetromino, cell_owners):
    can_move_down: bool = True
    cur_cells = tetromino.cells

    for cell in cur_cells:
        x, y = cell[0], cell[1]
        # Checks if the current cell is at the very bottom of the grid
        if y == height - 1:
            can_move_down = False
            break
        
        # Checks the cell below isn't part of the same tetromino
        #if Coord(x, y + 1) in cur_cells:
        if [x, y + 1] in cur_cells:
            continue

        # Finally checks if the cell below is blocked
        if grid[y + 1][x]:
            blocking_tet: Tetromino = cell_owners[y + 1][x]
            # Attempts to apply the gravity to the blocking tetromino
            if blocking_tet.can_move:
                try_move_down(grid, blocking_tet, cell_owners)
                # Checks again to see if the cell is still occupied
                if grid[y + 1][x]:
                    can_move_down = False
                    break
            else:
                can_move_down = False
                break
    
    
    if can_move_down:
        # Resets all the cells currently part of the tetromino
        tetromino.has_moved = True
        new_cells: list[list[int]] = []
        for cell in cur_cells:
            x, y = cell[0], cell[1]
            grid[y][x] = False
            cell_owners[y][x] = None
            new_cells.append([x, y + 1])
        
        # Adds the new cells and updates the grids
        tetromino.cells = new_cells
        for cell in new_cells:
            x, y = cell[0], cell[1]
            grid[y][x] = True
            cell_owners[y][x] = tetromino
    else:
        tetromino.can_move = False
        tetromino.has_moved = True


def apply_gravity(grid, tetrominos: list[Tetromino], cell_owners: list[Tetromino]):
    for tetromino in tetrominos:
        tetromino.can_move = True
        tetromino.has_moved = False
    
    for tetromino in tetrominos:
        if tetromino.has_moved:
            continue
        try_move_down(grid, tetromino, cell_owners)