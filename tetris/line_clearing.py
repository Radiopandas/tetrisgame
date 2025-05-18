from tetromino import Tetromino
from gravity import line_clearing_gravity
from time import sleep



def split_tetrominos(
        tetrominos_to_check: list[Tetromino], 
        cell_owners: list[list[Tetromino | None]], 
        all_tets: list[Tetromino]
    ) -> None:
    """Splits broken tetrominos into multiple Tetromino objects."""
    
    for tetromino in tetrominos_to_check:
        split_cell = tetromino.get_split_cell()

        # If split cell is empty, the current tetromino isn't split up.
        if not split_cell:
            continue

        # Removes the split_cell from everything so it can be
        # made into its own object.
        tetromino.cells.remove(split_cell)
        cell_owners[split_cell[1]][split_cell[0]] = None

        # Turns the split off cell into its own Tetromino.
        new_tet = Tetromino([split_cell])
        new_tet.can_move = False
        new_tet.tet_type = tetromino.tet_type
        all_tets.append(new_tet)
        cell_owners[split_cell[1]][split_cell[0]] = new_tet


def delete_rows(
        grid: list[list[bool]], 
        rows: list[int], 
        cell_owners: list[list[Tetromino | None]], 
        all_tets: list[Tetromino]
    ) -> None:
    """Clears rows and splits tetrominos."""
    # Stores which tetrominos to check for split cells, ignoring duplicates.
    to_be_checked: set[Tetromino] = set()

    # Iterates through 'rows', setting the cells in each row to be empty.
    for row in rows:
        cur_row = grid[row]
        for x, cell in enumerate(cur_row):
            # Since 'rows' only consists of filled rows, every cell in 
            # Cell_owners[row] is guaranteed to only contain Tetromino objects.
            cur_tet: Tetromino = cell_owners[row][x]
            cur_tet.cells.remove([x, row])
            to_be_checked.add(cur_tet)
            cell_owners[row][x] = None
            grid[row][x] = False


    if len(to_be_checked) > 0:
        split_tetrominos(list(to_be_checked), cell_owners, all_tets)

def check_rows(
        grid: list[list[bool]], 
        cell_owners: list[list[Tetromino | None]], 
        all_tets: list[Tetromino]
    ) -> list[int]:
    """Clears and returns the number of filled rows in the grid."""
    rows_to_delete: list[int] = []

    for y, row in enumerate(grid):

        # Checks for missing cells in the row
        if False in row:
            continue

        # Makes sure every cell in the row is stopped (Isn't able to move down)
        is_valid_row: bool = True
        for x, cell in enumerate(row):
            # Since the row is filled, the row cell_owners[y]
            # Is guaranteed to only contain Tetromino objects
            if cell_owners[y][x].can_move:
                is_valid_row = False
                break
        
        # If the prior conditions are met, marks the row to be cleared.
        if is_valid_row:
            rows_to_delete.append(y)
    
    delete_rows(grid, rows_to_delete, cell_owners, all_tets)

    if len(rows_to_delete) > 0:
        #sleep(0.1)
        
        #line_clearing_gravity(rows_to_delete, grid, cell_owners, all_tets)
        pass

    return rows_to_delete