from tetromino import Tetromino


def split_tetrominos(
        tetrominos_to_check: list[Tetromino], 
        cell_owners: list[list[Tetromino | None]], 
        all_tets: list[Tetromino]
    ):
    
    for tetromino in tetrominos_to_check:
        split_cell = tetromino.get_split_cell()

        # If split cell is empty, the current tetromino is intact
        if not split_cell:
            continue

        # Removes the split_cell from everything so it can be
        # made into its own object
        tetromino.cells.remove(split_cell)
        cell_owners[split_cell[1]][split_cell[0]] = None

        new_tet = Tetromino([split_cell])
        new_tet.tet_type = tetromino.tet_type
        all_tets.append(new_tet)
        cell_owners[split_cell[1]][split_cell[0]] = new_tet


def delete_rows(
        grid: list[list[bool]], 
        rows: list[int], 
        cell_owners: list[list[Tetromino | None]], 
        all_tets: list[Tetromino]
    ):
    # Stores which tetrominos to check for split cells
    to_be_checked: set[Tetromino] = set()

    for row in rows:
        cur_row = grid[row]

        for x, cell in enumerate(cur_row):
            cur_tet: Tetromino = cell_owners[row][x]
            cur_tet.cells.remove([x, row])
            to_be_checked.add(cur_tet)
            cell_owners[row][x] = None
            grid[row][x] = False

            #if len(cur_tet.cells) == 0:
                #all_tets.remove(cur_tet)

    
    if len(to_be_checked) > 0:
        #split_tetrominos(to_be_checked, cell_owners, all_tets)
        pass
            

def check_rows(grid, cell_owners: list[list[Tetromino | None]], all_tets):
    rows_to_delete: list[int] = []

    for y, row in enumerate(grid):

        # Checks for missing cells in the row
        if False in row:
            continue

        # Makes sure every cell in the row is stopped (Isn't able to move down)
        is_valid_row: bool = True
        for x, cell in enumerate(row):
            if cell_owners[y][x].can_move:
                is_valid_row = False
                break
        
        if is_valid_row:
            rows_to_delete.append(y)
    
    delete_rows(grid, rows_to_delete, cell_owners, all_tets)
    