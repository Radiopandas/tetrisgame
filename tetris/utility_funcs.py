from tetromino import Tetromino
from random import shuffle
from time import sleep # Delete after

piece_sequence: list[int] = []
piece_has_been_held: bool = False
held_piece: int = 0

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


# 
def generate_tetromino(
        grid: list[list[bool]], 
        piece_sequence: list[int],
    ):

    width: int = len(grid[0])

    # Checks if the spawn location is obstructed
    can_spawn: bool = True
    for y in range(2):
        for x in range(4):
            if grid[y][int(width / 2) - 2 + x]:
                can_spawn = False
                break
    
    # Uses 'random bag' to add pieces to the queue if they are needed
    if len(piece_sequence) < 7:
        to_add = [1, 2, 3, 4, 5, 6, 7]
        shuffle(to_add)
        piece_sequence += to_add
    
    # Actually generates the coordinates of the new piece.
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
        

        return [True, tet_cells, tetromino_type]
    else:
        return [False, [], 0]

def spawn_tetromino_2(
        grid: list[list[bool]], 
        focused_tetromino: Tetromino, 
        piece_sequence: list[int],
        all_tets: list[Tetromino],
        cell_owners: list[list[Tetromino | None]]
    ):
    # Gets the coordinates of the new piece's tiles
    spawn_success, new_tet_cells, new_tet_type = generate_tetromino(grid, piece_sequence)

    # Checks that spawning succeeded (Spawn area wasn't obstructed).
    if not spawn_success:
        return [False, focused_tetromino]

    # Turns them into a tetromino
    new_tet = Tetromino(new_tet_cells)
    new_tet.tet_type = new_tet_type
    all_tets.append(new_tet)
    add_tetromino(new_tet, grid, cell_owners)

    return [True, new_tet]

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
    
    # Uses 'random bag' to add pieces to the queue if they are needed
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

def clear_tetromino(
        tet: Tetromino,
        grid: list[list[bool]],
        all_tets: list[Tetromino],
        cell_owners: list[list[Tetromino | None]]
    ) -> None:
    #all_tets.remove(tet)
    for cell in tet.cells:
        x, y = cell[0], cell[1]
        grid[y][x] = False
        cell_owners[y][x] = None
    


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

def update_gravity_rate(total_lines_cleared: int, lines_just_cleared: int) -> int:
    if total_lines_cleared // 10 != (total_lines_cleared - lines_just_cleared) // 10:
        #print("Gravity changed I guess")
        #sleep(5)
        return 5
    return 0


def hold_piece(sequence: list[int], focused_tet: Tetromino) -> None:
    global held_piece, piece_has_been_held

    if not piece_has_been_held:
        """Moves the current piece to be held and immediately spawns the next piece"""
        _held_piece = focused_tet.tet_type

        # If a piece is already held, adds it to the start of the queue
        if held_piece:
            sequence.insert(0, held_piece)
        
        # Marks that a piece has been held
        piece_has_been_held = True

        print(f"Held piece: {_held_piece}")
        print(f"Sequence: {sequence}")

        held_piece = 0 + _held_piece
        
        return True

    return False

def hold_piece_2(
        grid: list[list[bool]], 
        focused_tetromino: Tetromino, 
        piece_sequence: list[int],
        all_tets: list[Tetromino],
        cell_owners: list[list[Tetromino | None]]
    ):
    global held_piece, piece_has_been_held
    
    if not piece_has_been_held:
        _held_piece = focused_tetromino.tet_type

        # If a piece is already held, adds it to the start of the queue
        if held_piece:
            piece_sequence.insert(0, held_piece)

        # Marks that a piece has been held already
        piece_has_been_held = True

        held_piece = 0 + _held_piece



    