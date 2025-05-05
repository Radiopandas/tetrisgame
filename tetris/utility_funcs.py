from tetromino import Tetromino
from random import shuffle
from time import sleep # Delete after

piece_sequence: list[int] = []
piece_has_been_held: bool = False
held_piece: int = 0

var_defaults = [[], False, 0]

def reset():
    """Resets all necessary local global variables."""
    global piece_sequence, piece_has_been_held, held_piece, var_defaults

    piece_sequence, piece_has_been_held, held_piece = var_defaults


def create_grid(width: int, height: int, value = False): return [[value for x in range(width)] for y in range(height)]


def get_range(nums: list): return max(nums) - min(nums) + 1


def add_tetromino(
        tetromino: Tetromino, 
        grid: list[list[bool]],
        owners: list[list[Tetromino | None]]
    ):
    """Inserts a tetromino into 'grid' and 'owners'."""
    for cell in tetromino.cells:
        grid[cell[1]][cell[0]] = True
        owners[cell[1]][cell[0]] = tetromino


def tet_to_pattern(tet_type: int) -> list[list[bool]]:
    """Returns an array containing the pattern for a given tetromino type."""
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


def generate_tetromino(
        grid: list[list[bool]], 
        piece_sequence: list[int],
    ):
    """Generates and returns an array of cells that make up a Tetromino."""
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
    
    # Checks that the spawn area isn't obstructed, then it
    # actually generates the coordinates of the new piece.
    if can_spawn:
        tet_cells: list[list[int]] = []

        tetromino_type: int = piece_sequence[0]
        piece_sequence.pop(0)

        # Based on 'pattern', generates the cells for the new piece.
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


def spawn_tetromino(
        grid: list[list[bool]], 
        focused_tetromino: Tetromino, 
        piece_sequence: list[int],
        all_tets: list[Tetromino],
        cell_owners: list[list[Tetromino | None]]
    ) -> tuple[bool, Tetromino]:
    """Spawns and returns a new Tetromino, as well as whether the spawn area
    is obstructed by other pieces."""

    # Gets the coordinates of the new piece's tiles
    spawn_success, new_tet_cells, new_tet_type = generate_tetromino(grid, piece_sequence)

    # Checks that spawning succeeded (Spawn area wasn't obstructed).
    if not spawn_success:
        results = (False, focused_tetromino)
        return results

    # Turns them into a tetromino
    new_tet = Tetromino(new_tet_cells)
    new_tet.tet_type = new_tet_type
    all_tets.append(new_tet)
    add_tetromino(new_tet, grid, cell_owners)

    results = (True, new_tet)
    return results


def clear_tetromino(
        tet: Tetromino,
        grid: list[list[bool]],
        all_tets: list[Tetromino],
        cell_owners: list[list[Tetromino | None]]
    ) -> None:
    """Removes a given Tetromino from 'grid' and 'cell_owners'."""
    for cell in tet.cells:
        x, y = cell[0], cell[1]
        grid[y][x] = False
        cell_owners[y][x] = None


def update_scores(lines_just_cleared: int) -> int:
    """Returns how much to increment the score based on the number
    of lines cleared in one go."""
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
    """Returns how much to decrease the graivty cooldown by, based on how 
    many lines have been cleared(total) and were just cleared."""
    if total_lines_cleared // 10 != (total_lines_cleared - lines_just_cleared) // 10:
        return 5
    return 0    


def hold_piece(sequence: list[int], focused_tet: Tetromino) -> bool:
    """Moves the current piece to be held and immediately spawns the next piece, 
    unless the current piece has already been held. Returns whether this 
    process was successful or not."""
    global held_piece, piece_has_been_held

    if not piece_has_been_held:
        _held_piece = focused_tet.tet_type

        # If a piece is already held, adds it to the start of the queue
        if held_piece:
            sequence.insert(0, held_piece)
        
        # Marks that a piece has been held
        piece_has_been_held = True

        # No clue why I did this
        held_piece = 0 + _held_piece
        
        return True

    return False
