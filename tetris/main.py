import rotation
import gravity
import line_clearing
import draw_game
from tetromino import Tetromino
import utility_funcs
import movement
import pygame
from random import shuffle

from time import sleep

# A bunch of global variables that are rather necessary
width: int = 10
height: int = 22

focused_tetromino: Tetromino = Tetromino([])
grid: list[list[bool]] = []
cell_owners: list[list[Tetromino | None]]
all_tetrominos: list[Tetromino] = []
ghost_piece_tiles: list[list[bool]] = utility_funcs.create_grid(width, height, False)

score: int = 0
lines_cleared: int = 0

gravity_cooldown: int = 15
piece_sequence: list[int] = [1, 2, 3, 4, 5, 6, 7]
held_piece: int = 0

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
    global focused_tetromino, continue_game, piece_spawn_cooldown, movement_cooldown, score, lines_cleared, gravity_cooldown

    if not keep_playing:
        return

    if frame % gravity_rate == 0:
        draw_game.print_grid(grid, ghost_piece_tiles)
        gravity.apply_gravity(grid, all_tets, cell_owners)
        movement.update_ghost_piece_2(grid, focused_tet, ghost_piece_tiles)
        
        lines_just_cleared = line_clearing.check_rows(grid, cell_owners, all_tets)
        score += utility_funcs.update_scores(lines_just_cleared)
        lines_cleared += lines_just_cleared
        if gravity_rate > 10:
            gravity_cooldown -= utility_funcs.update_gravity_rate(lines_cleared, lines_just_cleared)
        movement.update_ghost_piece_2(grid, focused_tet, ghost_piece_tiles)
    
    if not focused_tet.can_move and piece_spawn_cooldown == 0:
        spawn_results = utility_funcs.spawn_tetromino_2(grid, focused_tet, piece_sequence, all_tets, cell_owners)
        continue_game = spawn_results[0]
        focused_tetromino = spawn_results[1]
        movement.update_ghost_piece_2(grid, focused_tet, ghost_piece_tiles)
        piece_spawn_cooldown = 20

        utility_funcs.piece_has_been_held = False

    if piece_spawn_cooldown > 0:  
        piece_spawn_cooldown -= 1
    
    if movement_cooldown == 0:
        
        if movement.get_movement_2(grid, focused_tetromino, cell_owners):

            movement.update_ghost_piece_2(grid, focused_tet, ghost_piece_tiles)
            draw_game.print_grid(grid, ghost_piece_tiles)
            movement_cooldown += 7
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
    shuffle(piece_sequence)
    
    # Stuff for testing
    focused_tetromino = Tetromino([[0, 1], [1, 1], [2, 1], [3, 1]])#, [4, 1], [5, 1], [6, 1], [7, 1], [8, 1]])
    all_tetrominos.append(focused_tetromino)
    utility_funcs.add_tetromino(focused_tetromino, grid, cell_owners)

    #utility_funcs.hold_piece(piece_sequence)
    #print(f"Piece sequence: {piece_sequence}")
    #sleep(3)
    

    #focused_tetromino = utility_funcs.start_game(grid, focused_tetromino, piece_sequence, all_tetrominos, cell_owners)

    clock = pygame.time.Clock() 
    running: bool = True
    while running:
        frame += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
            elif event.type == pygame.KEYDOWN:
                if movement.pygame_event_handler(event, grid, focused_tetromino, cell_owners, piece_sequence, all_tetrominos):
                    movement.update_ghost_piece_2(grid, focused_tetromino, ghost_piece_tiles)
                    movement.update_ghost_piece_2(grid, focused_tetromino, ghost_piece_tiles)
                    pass
        
        draw_game.screen.fill(draw_game.background_colour)

        draw_game.draw_game(grid, cell_owners, 13, ghost_piece_tiles, score, lines_cleared, piece_sequence)

        update(frame, grid, all_tetrominos, continue_game, gravity_cooldown, cell_owners, focused_tetromino, piece_sequence)

        dt = clock.tick(60) / 1000
    
    pygame.quit()


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
update_score - utility_funcs

# TODO pygame specific
pygame_get_movement - movement
event_handler - movement

set_draw_colour - draw_grid  
draw_grid - draw_grid
draw_stats - draw_grid
draw_next_piece - draw_grid
draw_gui - draw_grid

Add an easy way to reset variables to their initial values. Maybe store them in a dict (hardcoded ofc)

Replace spawn_piece (utility_funcs) with two functions: 
 - One that generates and returns a list of coordinates
 - One that calls the previous functions, converts that 
    list of coordinates into a tetromino and returns it plus 
    a boolean value (this func would be called wherever spawn_piece is currently called).

"""