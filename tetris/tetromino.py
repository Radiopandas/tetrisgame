
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

    # What type of piece it is (1: I, 2: J, 3: L, 4: O, 5: S, 6: T or 7: Z)
    # a 'tet_type' of 0 represents miscellaneous pieces such as lone cells.
    tet_type: int = 0

    # Determines the layout of the piece for rotation
    times_rotated: int = 0

    
    def __init__(self, _cells):
        self.cells = _cells

    def __str__(self):
        return f"Tet with cells: {self.cells}"

    # Checks if the cells in the tetromino are split up
    def get_split_cell(self):
        if len(self.cells) == 1:
            return []
        
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