from tetromino import Tetromino
from utility_funcs import get_range
from copy import deepcopy

# Wall kicks stuff
jlstz_wall_kicks: dict = {
    "01": [[0, 0], [-1, 0], [-1, -1], [0, 2], [-1, 2]],
    "10": [[0, 0], [1, 0], [1, 1], [0, -2], [1, -2]],
    "12": [[0, 0], [1, 0], [1, 1], [0, -2], [1, -2]],
    "21": [[0, 0], [-1, 0], [-1, -1], [0, 2], [-1, 2]],
    "23": [[0, 0], [1, 0], [1, -1], [0, 2], [1, 2]],
    "32": [[0, 0], [-1, 0], [-1, 1], [0, -2], [-1, -2]],
    "30": [[0, 0], [-1, 0], [-1, 1], [0, -2], [-1, -2]],
    "03": [[0, 0], [1, 0], [1, -1], [0, 2], [1, 2]]
}
i_wall_kicks: dict = {
    "01": [[0, 0], [-2, 0], [1, 0], [-2, 1], [1, -2]],
    "10": [[0, 0], [2, 0], [-1, 0], [2, -1], [-1, 2]],
    "12": [[0, 0], [-1, 0], [2, 0], [-1, -2], [2, 1]],
    "21": [[0, 0], [1, 0], [-2, 0], [1, 2], [-2, -1]],
    "23": [[0, 0], [2, 0], [-1, 0], [2, -1], [-1, 2]],
    "32": [[0, 0], [-2, 0], [1, 0], [-2, 1], [1, -2]],
    "30": [[0, 0], [1, 0], [-2, 0], [1, 2], [-2, -1]],
    "03": [[0, 0], [-1, 0], [2, 0], [-1, -2], [2, 1]]
}

width: int = 0
height: int = 0

var_defaults = [0, 0]

def reset():
    global width, height, var_defaults
    width, height = var_defaults

def set_grid_size(_width: int, _height: int):
    global height, width
    height = _height
    width = _width

def rotate_grid(grid, clockwise: bool = True):
    """'Rotate' a grid by 90 degrees and return the result"""
    if clockwise:
        # Performs a matrix transpose
        rotated_grid = [[grid[j][i] for j in range(len(grid))] for i in range(len(grid[0]))]
        # Reverses every row
        for row in rotated_grid:
            row.reverse()
        return rotated_grid
    else:
        # For clockwise rotation, we just have to reverse
        # the list and then do a matrix transpose
        for row in grid:
            row.reverse()
        rotated_grid = [[grid[j][i] for j in range(len(grid))] for i in range(len(grid[0]))]
        # Undoes the previous reversal so the intial 'grid' doesn't change.
        for row in grid:
            row.reverse()
        return rotated_grid


def get_wall_kicks(cur_rotation: int, direction: int, piece_type: int):
    key = str(cur_rotation) + str((cur_rotation + direction) % 4)
    if piece_type == 1:
        return i_wall_kicks[key]
    else:
        return jlstz_wall_kicks[key]

def check_rotation_validity(grid, rotated_grid, coord_grid, tetromino: Tetromino, offset: list = [0, 0]):
    print("rotated_grid: ")
    print(*rotated_grid, sep="\n")

    # Increments grid_coords by the offset
    grid_width: int = len(coord_grid)
    print("Coord grid: ")
    print(*coord_grid, sep="\n")

    _coord_grid = deepcopy(coord_grid)

    for y in range(grid_width):
        for x in range(grid_width):
            _coord_grid[y][x][0] += offset[0]
            _coord_grid[y][x][1] += offset[1]
    print("New Coord grid: ")
    print(*_coord_grid, sep="\n")
    print("Oldish coord grid")
    print(*coord_grid, sep="\n")

    #sleep(3)
    rotation_valid: bool = True
    for row_y, row in enumerate(_coord_grid):
        for row_x, cell in enumerate(row):
            x, y = cell[0], cell[1]
            # Checks the new cells are actually in the grid
            if not 0 <= x < width or not 0 <= y < height:
                rotation_valid = False
                break

            # Checks the new location is empty
            if rotated_grid[row_y][row_x] and not [x, y] in tetromino.cells:
                if grid[y][x]:
                    print(f"{x}, {y} is invalid: Grid at {x}, {y}: {grid[y][x]}")
                    rotation_valid = False
                    break
        if not rotation_valid:
            break
    
    return rotation_valid

def rotate_tet(grid, focused_tet: Tetromino, cell_owners, clockwise: bool = True):
    # Since the 'o' piece can't be rotated, exits early
    if focused_tet.tet_type == 4:
        return
    
    cur_cells = focused_tet.cells
    
    x_coords: list[int] = []
    y_coords: list[int] = []
    for cell in cur_cells:
        x_coords.append(cell[0])
        y_coords.append(cell[1])
    
    min_x = min(x_coords)
    min_y = min(y_coords)

    x_offset: int = 0
    y_offset: int = 0

    # Calculates how much offset is required to have each piece be
    # Centred in the grids
    base_offset = 2 if focused_tet.tet_type == 1 else 1
    match focused_tet.times_rotated:
        case 0:
            y_offset = base_offset - 1
        case 1:
            x_offset = base_offset
        case 2:
            y_offset = base_offset
        case 3:
            x_offset = base_offset - 1
    
    shape_width = max(get_range(x_coords), get_range(y_coords))

    coord_grid: list = [[[x+min_x - x_offset, y+min_y - y_offset] for x in range(shape_width)] for y in range(shape_width)]

    # Converts the inputted shape to a grid of bools
    bool_grid = [[False for i in range(shape_width)] for j in range(shape_width)]

    for cell in cur_cells:
        x, y = cell[0] + x_offset, cell[1] + y_offset
        bool_grid[y - min_y][x - min_x] = True
    
    rotated_grid = rotate_grid(bool_grid, clockwise)

    rotation_x_offset: int = 0
    rotation_y_offset: int = 0
    can_rotate: bool = True

    direction: int = 1 if clockwise else -1
    wall_kicks = get_wall_kicks(focused_tet.times_rotated, direction, focused_tet.tet_type)
    for offset in wall_kicks:
        rotation_x_offset = offset[0]
        rotation_y_offset = offset[1]
        can_rotate = check_rotation_validity(grid, rotated_grid, coord_grid, focused_tet, offset)
        if can_rotate:
            break
    

    if can_rotate:
        for y, row in enumerate(bool_grid):
            for x, cell in enumerate(row):
                if cell:
                    cur_x, cur_y = coord_grid[y][x][0], coord_grid[y][x][1]
                    grid[cur_y][cur_x] = False
                    cell_owners[cur_y][cur_x] = None

        new_cells = []
        for y, row in enumerate(rotated_grid):
            for x, cell in enumerate(row):
                if cell:
                    cur_x = coord_grid[y][x][0] + rotation_x_offset
                    cur_y = coord_grid[y][x][1] + rotation_y_offset
                    new_cells.append([cur_x, cur_y])
        
        focused_tet.cells = new_cells
        for cell in new_cells:
            x, y = cell[0], cell[1]
            grid[y][x] = True
            cell_owners[y][x] = focused_tet
                

        if clockwise:
            focused_tet.times_rotated += 1
            if focused_tet.times_rotated > 3:
                focused_tet.times_rotated = 0
        else:
            focused_tet.times_rotated -= 1
            if focused_tet.times_rotated < 0:
                focused_tet.times_rotated = 3