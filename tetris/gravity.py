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


def apply_gravity(grid, tetrominos: list[Tetromino], cell_owners: list[list[Tetromino | None]], focused_tetromino: Tetromino = None):
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
    
    if focused_tetromino and input_handling.just_hard_dropped:
        focused_tetromino.can_move = False


def focused_gravity(
        grid: list[list[bool]],
        cell_owners: list[list[Tetromino | None]],
        focused_tet: Tetromino
    ):
    """Attemps to move the focused tetromino downwards in the grid."""
    cur_cells = focused_tet.cells

    can_move_down: bool = True
    for cell in cur_cells:
        x, y = cell
        # Checks if the cell is at the bottom of the grid.
        if y == height - 1:
            can_move_down = False
            focused_tet.can_move = False
            break
        
        # Next, checks if it is blocked by other cells in focused_tet.
        if [x, y+1] in cur_cells:
            continue
        
        # Finally, checks if the cell is blocked by another piece.
        if grid[y+1][x]:
            can_move_down = False
            focused_tet.can_move = False
            break
    
    # If nothing is blocking the focused_tetromino, moves it down.
    if can_move_down:
        focused_tet.move_down(1, grid, cell_owners)

def line_clearing_gravity(
        rows_cleared: list[int],
        grid: list[list[bool]],
        cell_owners: list[list[Tetromino | None]],
        all_tetrominos: list[Tetromino]
    ) -> None:
    # Finds the highest row that was cleared.
    highest_row = min(rows_cleared)
    number_of_rows = len(rows_cleared)

    # For every tetromino, checks if it is above the cleared rows,
    # in which case it moves it down by the number of cleared rows.
    for tet in all_tetrominos:
        if tet.should_move(highest_row):
            tet.move_down(number_of_rows, grid, cell_owners)