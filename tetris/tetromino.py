
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

    # What type of piece it is (1: I, 2: J, 3: L, 4: O, 5: S, 6: T or 7: Z).
    tet_type: int = 0

    # Determines the layout of the piece for rotation
    times_rotated: int = 0

    # Allows gravity to work based on a clock specific to the focused tetromino
    # instead of a global clock.
    gravity_frame: int = 0

    
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

    def should_move(self, row: int) -> bool:
        """Given a row, checks if the current tetromino contains cells
        above that row. Called after line clearing to move all cells above
        the cleared line(s) downwards."""
        for cell in self.cells:
            if cell[1] < row:
                return True
        
        return False
    
    def move_down(
            self,
            num_of_rows: int,
            grid: list[list[bool]],
            cell_owners: list[list]
        ) -> None:
        """
        Moves all cells in the Tetromino down 1 cell.
        It should be noted that this function does not check if movement
        is blocked or not, so should only be called when you are certain
        there is nothing blocking the current Tetromino.
        """
        cur_cells = self.cells
        new_cells = []
        for cell in cur_cells:
            x, y = cell
            # Removes the current cell from the grids.
            grid[y][x] = False
            cell_owners[y][x] = None

            new_cells.append([x, y + num_of_rows])
        
        # Adds the new cells back to the grids.
        self.cells = new_cells
        for cell in new_cells:
            x, y = cell
            grid[y][x] = True
            cell_owners[y][x] = self
        