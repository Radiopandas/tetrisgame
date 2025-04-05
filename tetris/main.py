import rotation
import gravity
import line_clearing
import draw_game
from tetromino import Tetromino
import utility_funcs
import movement
import pygame

from time import sleep

# A bunch of global variables that are rather necessary
width: int = 10
height: int = 22

focused_tetromino: Tetromino
grid: list[list[bool]] = []
cell_owners: list[list[Tetromino | None]]
all_tetrominos: list[Tetromino] = []
ghost_piece_tiles: list[list[bool]] = utility_funcs.create_grid(width, height, False)

gravity_cooldown: int = 15
piece_sequence: list[int] = []

continue_game: bool = True
movement_cooldown: int = 0
piece_spawn_cooldown: int = 0
frame: int = 0

def update(
        frame: int, 
        grid, 
        all_tets: list[Tetromino], 
        keep_playing: bool,
        gravity_rate: int,
        cell_owners: list[list[Tetromino | None]],
        focused_tet: Tetromino,
        piece_sequence: list[int],
        ):
    # For some fucking reason if I don't do it like this everything breaks
    global focused_tetromino, continue_game, piece_spawn_cooldown, movement_cooldown

    if not keep_playing:
        return

    if frame % gravity_rate == 0:
        draw_game.print_grid(grid, ghost_piece_tiles)
        gravity.apply_gravity(grid, all_tets, cell_owners)
        movement.update_ghost_piece(grid, focused_tet, ghost_piece_tiles)
        
        line_clearing.check_rows(grid, cell_owners, all_tets)
        movement.update_ghost_piece(grid, focused_tet, ghost_piece_tiles)
        #draw_game.print_grid(grid)
    
    if not focused_tet.can_move and piece_spawn_cooldown == 0:
        spawn_results = utility_funcs.spawn_tetromino(grid, focused_tet, piece_sequence, all_tets, cell_owners)
        continue_game = spawn_results[0]
        focused_tetromino = spawn_results[1]
        movement.update_ghost_piece(grid, focused_tet, ghost_piece_tiles)
        piece_spawn_cooldown = 20
    if piece_spawn_cooldown > 0:
        piece_spawn_cooldown -= 1
    
    if movement_cooldown == 0:
        if movement.get_movement(grid, focused_tet, cell_owners):
            movement.update_ghost_piece(grid, focused_tet, ghost_piece_tiles)
            draw_game.print_grid(grid, ghost_piece_tiles)
            movement_cooldown += 5
    elif movement_cooldown > 0:
        movement_cooldown -= 1


if __name__ == "__main__":
    
    # Set up functions
    grid = utility_funcs.create_grid(width, height, False)
    cell_owners = utility_funcs.create_grid(width, height, None)
    gravity.set_grid_size(width, height)
    movement.set_grid_size(width, height)
    rotation.set_grid_size(width, height)
    draw_game.set_grid_size(width, height)
    
    # Stuff for testing
    focused_tetromino = Tetromino([[0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [5, 1], [6, 1], [7, 1], [8, 1], [9, 1]])
    all_tetrominos.append(focused_tetromino)
    utility_funcs.add_tetromino(focused_tetromino, grid, cell_owners)
    


    

    #while continue_game:
        #update(frame, grid, all_tetrominos, continue_game, gravity_cooldown, cell_owners, focused_tetromino, piece_sequence)
        #frame += 1
        #sleep(0.02)
    clock = pygame.time.Clock()
    running: bool = True
    while running:
        frame += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        draw_game.screen.fill(draw_game.background_colour)

        draw_game.draw_game(grid, cell_owners, 15, ghost_piece_tiles)

        update(frame, grid, all_tetrominos, continue_game, gravity_cooldown, cell_owners, focused_tetromino, piece_sequence)

        dt = clock.tick(60) / 1000
    
    pygame.quit()


"""    for i in range(80):
        update(frame, grid, all_tetrominos, continue_game, gravity_cooldown, cell_owners, focused_tetromino, piece_sequence, movement_cooldown, piece_spawn_cooldown)
        if not continue_game:
            break
        frame += 1
        sleep(0.1)"""




"""
TODO:
get_range - utility_funcs
rotate_grid - utility_funcs
add_tetromino - utility_funcs
split_tetrominos - line_clearing
try_move_down - gravity
apply_gravity - gravity
delete_rows - line_clearing
check_rows - line_clearing
tet_to_pattern - utility_funcs
spawn_tetromino - utility_funcs
move_tet - movement
get_wall_kicks - rotation
check_rotation_validity - rotation
rotate_tet - rotation
quick_drop - movement
ghost_piece - movement
update_score
get_movement - movement

# TODO pygame specific
pygame_get_movement
event_handler

set_draw_colour
draw_grid
draw_score
draw_cleared_lines
draw_next_piece
draw_gui

"""