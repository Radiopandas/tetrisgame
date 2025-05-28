
# Constants used to represent moving in cardinal directions
N, S, E, W = 1, 2, 4, 8
DX = {N: 0, S: 0, E: 1, W: -1}
DY = {N: -1, S: 1, E: 0, W: 0}


class Tetromino:
    # Stores the coordinates of every cell that 
    # is a part of the current piece.
    cells: list[list[int]] = [] 

    # Can move determines whether the pieces of a tetromino
    # should be considered when checking for full rows.
    can_move: bool = True

    # Prevents gravity being applied multiple times
    has_moved: bool = False

    is_locked: bool = False

    # What type of piece it is (1: I, 2: J, 3: L, 4: O, 5: S, 6: T or 7: Z).
    tet_type: int = 0

    # Determines the layout of the piece for rotation
    times_rotated: int = 0

    # Allows gravity to be tied to each piece instead of a global clock,
    # thus reducing inconsistencies when pieces spawn.
    gravity_frame: int = 0

    is_on_ground: bool = False
    locking_frame: int = 0
    MAX_LOCKING_FRAME: int = 30

    
    def __init__(self, _cells):
        self.cells = _cells

    def __str__(self):
        return f"Tet with cells: {self.cells}"

    # Checks if the cells in the tetromino are split up
    def get_split_cell(self) -> list[int]:
        """Returns the cell that is split up from the main Tetromino
        if it exists."""
        # If there is only one cell total, it can't possibly be split up.
        if len(self.cells) == 1:
            return []
        
        # Every cell checks for another cell in each of the 4 directions.
        # If it doesn't find another cell, it must be the split off cell.
        # If every cell is connected to another, returns an empty cell.
        for cell in self.cells:
            is_connected: bool = False
            x, y = cell[0], cell[1]

            directions = [N, S, E, W]
            for direction in directions:
                new_x, new_y = x + DX[direction], y + DY[direction]
                if [new_x, new_y] in self.cells:
                    is_connected = True
                    break
            
            if not is_connected:
                return cell
        return []
    
    def get_top_left(self) -> tuple[int, int]:
        top = self.cells[0][0]
        left = self.cells[0][0]

        for cell in self.cells:
            x, y = cell
            if y < top:
                top = y
            if x < left:
                left = x
        
        return (left, top)

    def check_is_grounded(self, grid: list[list[bool]]) -> bool:
        height = len(grid)
        for cell in self.cells:
            x, y = cell
            # Checks if the cell is at the bottom of the grid.
            if y == height - 1:
                return True
            
            if [x, y + 1] in self.cells:
                continue

            if grid[y+1][x]:
                return True
        
        return False