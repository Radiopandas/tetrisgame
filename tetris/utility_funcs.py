from tetromino import Tetromino
from random import shuffle
from time import sleep # Delete after



def create_grid(width: int, height: int, value = False): return [[value for x in range(width)] for y in range(height)]

def get_range(nums: list): return max(nums) - min(nums) + 1


def add_tetromino(tetromino: Tetromino, grid, owners):
    for cell in tetromino.cells:
        grid[cell[1]][cell[0]] = True
        owners[cell[1]][cell[0]] = tetromino

def tet_to_pattern(tet_type: int) -> list[list[bool]]:
    """Returns an array containing the pattern for a given tetromino type"""
    match tet_type:
        case 1:
            return [[False, False, False, False], [True, True, True, True]]
        case 2:
            return [[True, False, False, False], [True, True, True, False]]
        case 3:
            return [[False, False, True, False], [True, True, True, False]]
        case 4:
            return [[False, True, True, False], [False, True, True, False]]
        case 5:
            return [[False, True, True, False], [True, True, False, False]]
        case 6:
            return [[False, True, False, False], [True, True, True, False]]
        case 7:
            return [[True, True, False, False], [False, True, True, False]]
        case _:
            print("Invalid tet_index")
            return []

def spawn_tetromino(
        grid: list[list[bool]], 
        focused_tetromino: Tetromino, 
        piece_sequence: list[int],
        all_tets: list[Tetromino],
        cell_owners: list[list[Tetromino | None]]
    ):
    width = len(grid[0])

    # Checks if the spawn location is obstructed
    can_spawn: bool = True
    for y in range(2):
        for x in range(4):
            if grid[y][int(width / 2) - 2 + x]:
                can_spawn = False
                break
    
    # Uses 'random bag' to add pieces to the queue
    if len(piece_sequence) < 7:
        to_add = [1, 2, 3, 4, 5, 6, 7]
        shuffle(to_add)
        piece_sequence += to_add
    
    if can_spawn:
        tet_cells: list[list[int]] = []

        tetromino_type: int = piece_sequence[0]
        piece_sequence.pop(0)

        pattern = tet_to_pattern(tetromino_type)
        for y, row in enumerate(pattern):
            cell_index: int = 0
            for cell in row:
                if cell:
                    grid[y][int(width / 2) - 2 + cell_index] = True
                    tet_cells.append([int(width / 2) - 2 + cell_index, y])
                cell_index += 1

        new_tet = Tetromino(tet_cells)
        new_tet.tet_type = tetromino_type
        all_tets.append(new_tet)
        add_tetromino(new_tet, grid, cell_owners)
        focused_tetromino = new_tet

        return [True, new_tet]
    else:
        return [False, focused_tetromino]

def update_scores(lines_just_cleared: int) -> int:
    match lines_just_cleared:
        case 1:
            return 40
        case 2:
            return 100
        case 3:
            return 300
        case 4:
            return 1200
        case _:
            return 0


