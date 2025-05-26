from tetromino import Tetromino
import input_handling

width: int = 0
height: int = 0

var_defaults = [0, 0]

def reset():
    """Resets necessary local global variables."""
    global width, height, var_defaults

    width, height = var_defaults

def set_grid_size(_width: int, _height: int):
    """Called from 'main.py' to tell 'gravity.py' the play area size."""
    global height, width
    height = _height
    width = _width

    print(f"Height: {height}")


def try_move_down(
        grid: list[list[bool]], 
        tetromino: Tetromino, 
        cell_owners: list[list[Tetromino | None]]
        ):
    """Gravity function that is called (somewhat) recursively to try
    and move all tetrominos downwards."""
    can_move_down: bool = True
    cur_cells = tetromino.cells

    # Iterates through each cell in the current piece, checking if it
    # is obstructed / is at the bottom of the play area.
    for cell in cur_cells:
        x, y = cell[0], cell[1]
        # Checks if the current cell is at the very bottom of the grid
        if y == height - 1:
            can_move_down = False
            break
        
        # Checks the cell below isn't part of the same tetromino
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
    
    # Moves the cells of 'tetromino' down and marks that it has moved.
    if can_move_down:
        # Resets all the cells currently part of the tetromino
        # Also adds cells to new_cells.
        tetromino.has_moved = True
        tetromino.gravity_frame = 0
        tetromino.is_on_ground = False
        new_cells: list[list[int]] = []
        for cell in cur_cells:
            x, y = cell[0], cell[1]
            grid[y][x] = False
            cell_owners[y][x] = None
            new_cells.append([x, y + 1])
        
        # Applies these changes to 'tetromino' and updates the grids.
        tetromino.cells = new_cells
        for cell in new_cells:
            x, y = cell[0], cell[1]
            grid[y][x] = True
            cell_owners[y][x] = tetromino
    else:
        # Marks that 'tetromino' is blocked and has already tried to move.
        tetromino.can_move = False
        tetromino.has_moved = True


def apply_gravity(grid, tetrominos: list[Tetromino], cell_owners: list[list[Tetromino | None]], focused_tetromino: Tetromino):
    """Attempts to call a recursive gravity function on every tetromino on the board."""
    # Resets the movement booleans for every tetromino.
    for tetromino in tetrominos:
        if tetromino.cells != []: # Hopefully fixes issue no. 1
            tetromino.can_move = True
            tetromino.has_moved = False
    # Tries to call 'try_move_down'.
    for tetromino in tetrominos:
        if tetromino.has_moved:
            continue
        try_move_down(grid, tetromino, cell_owners)

    # Checks if the focused tetromino is now sitting on top of something:
    for cell in focused_tetromino.cells:
        x, y = cell
        if y == height - 1:
            focused_tetromino.is_on_ground = True
            break
        
        if [x, y+1] in focused_tetromino.cells:
            continue
        
        if grid[y+1][x]:
            focused_tetromino.is_on_ground = True
            break
    
    # Makes it so that the focused tetromino is only locked down after its locking_delay.
    if not focused_tetromino.can_move and \
    focused_tetromino.locking_frame < focused_tetromino.MAX_LOCKING_FRAME and \
    not focused_tetromino.is_locked:
        focused_tetromino.can_move = True
        focused_tetromino.is_on_ground = True
    
    if focused_tetromino and input_handling.just_hard_dropped:
        focused_tetromino.can_move = False


def focused_gravity(
        grid: list[list[bool]], 
        cell_owners: list[list[Tetromino | None]], 
        focused_tet: Tetromino
    ):
    cur_cells = focused_tet.cells
    can_move: bool = True
    for cell in cur_cells:
        x, y = cell
        # Checks if the cell is grounded
        if y == height - 1:
            can_move = False
            focused_tet.can_move = False
            break

        # Checks if the cell is blocked by another part of the same tetromino.
        if [x, y + 1] in cur_cells:
            continue

        # Checks if it is blocked by another tetromino
        if grid[y + 1][x]:
            can_move = False
            focused_tet.can_move = False
            break
    
    if can_move:
        for cell in cur_cells:
            x, y = cell
            grid[y][x] = False
            cell_owners[y][x] = None
            cell[1] += 1
        
        for cell in cur_cells:
            x, y = cell
            grid[y][x] = True
            cell_owners[y][x] = focused_tet
        
        focused_tet.cells = True

"""
Attempt to move everything downwards.
If a piece is able to move downwards, reset its locking delay.

After applying gravity, check if the focused tetromino is marked as unable to move.
    Check if its locking delay is less than 20(arbitrary number).
        If it is, make it able to move again.
"""