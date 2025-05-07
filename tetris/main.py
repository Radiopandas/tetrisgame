import rotation
import gravity
import line_clearing
import draw_game
from tetromino import Tetromino
import utility_funcs
import movement
import pygame
import copy
import attractor
import json_parser
import input_handling
from random import shuffle

from time import sleep

# A bunch of global variables that are rather necessary
width: int = 10
height: int = 22

focused_tetromino: Tetromino = Tetromino([])
grid: list[list[bool]] = []
cell_owners: list[list[Tetromino | None]] = []
all_tetrominos: list[Tetromino] = []
ghost_piece_tiles: list[list[bool]] = utility_funcs.create_grid(width, height, False)

score: int = 0
lines_cleared: int = 0

gravity_cooldown: int = 15
piece_sequence: list[int] = [1, 2, 3, 4, 5, 6, 7]
held_piece: int = 0

attractor_needs_to_wait: bool = False

display_start_menu: bool = True
continue_game: bool = True
movement_cooldown: int = 0
piece_spawn_cooldown: int = 0
frame: int = 0

# Only to be used when displaying the game to people
can_quit: bool = True

all_vars = [
    width, height, focused_tetromino, grid, cell_owners, all_tetrominos,
    ghost_piece_tiles, score, lines_cleared, gravity_cooldown,
    piece_sequence, held_piece, continue_game, movement_cooldown,
    piece_spawn_cooldown, frame
    ]

var_defaults = [
    10, 22, Tetromino([]), [], [], [],
    utility_funcs.create_grid(width, height, False), 0, 0, 15,
    [1, 2, 3, 4, 5, 6, 7], 0, True, 0, 0, 0
]

def reset_game():
    """Resets all local global variables and calls reset() on all other scripts."""

    # Resets the variables in all loaded modules
    utility_funcs.reset()
    rotation.reset()
    movement.reset()
    gravity.reset()
    draw_game.reset()
    attractor.reset()

    # Resets local variables
    global width, height, focused_tetromino, grid, cell_owners, all_tetrominos, \
        ghost_piece_tiles, score, lines_cleared, gravity_cooldown, \
        piece_sequence, held_piece, continue_game, movement_cooldown, \
        piece_spawn_cooldown, frame, var_defaults
    
    defaults = copy.deepcopy(var_defaults)
    width, height, focused_tetromino, grid, cell_owners, all_tetrominos, \
        ghost_piece_tiles, score, lines_cleared, gravity_cooldown, \
        piece_sequence, held_piece, continue_game, movement_cooldown, \
        piece_spawn_cooldown, frame = defaults


def start_game():
    """Resets everything then calls several setup functions."""

    global grid, cell_owners, width, height, piece_sequence

    reset_game()
    sleep(0.05)

    grid = utility_funcs.create_grid(width, height, False)
    cell_owners = utility_funcs.create_grid(width, height, None)
    gravity.set_grid_size(width, height)
    movement.set_grid_size(width, height)
    rotation.set_grid_size(width, height)
    draw_game.set_grid_size(width, height)
    shuffle(piece_sequence)


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
    global focused_tetromino, continue_game, piece_spawn_cooldown, movement_cooldown, score, lines_cleared, gravity_cooldown, display_start_menu, attractor_needs_to_wait

    if not keep_playing:
        return

    # Calls the gravity functions, as well as several related functions
    # periodically instead of every single frame.
    if frame % gravity_rate == 0:
        # Applies gravity to every piece, then updates the ghost piece
        # To account for the new changes.
        draw_game.print_grid(grid, ghost_piece_tiles)
        gravity.apply_gravity(grid, all_tets, cell_owners)
        movement.update_ghost_piece(grid, focused_tet, ghost_piece_tiles)
        
        # Checks for and clears filled rows.
        lines_just_cleared = line_clearing.check_rows(grid, cell_owners, all_tets)
        # Increments the number of lines cleared, updates the score and potentially
        # updates the gravity rate.
        score += utility_funcs.update_scores(lines_just_cleared)
        lines_cleared += lines_just_cleared
        if gravity_rate > 10:
            gravity_cooldown -= utility_funcs.update_gravity_rate(lines_cleared, lines_just_cleared)
        movement.update_ghost_piece(grid, focused_tet, ghost_piece_tiles)
    
    # If the current focused piece can't move, it must be on the ground
    # Thus it needs to spawn a new piece for the player to control.
    # Overridden by display_start_menu, since it uses its own functions
    # to do things such as spawning pieces.
    if not focused_tet.can_move and piece_spawn_cooldown == 0 and not display_start_menu:
        # Attempts to spawn a new piece, then assigns it to focused_tetromino.
        spawn_results = utility_funcs.spawn_tetromino(grid, focused_tet, piece_sequence, all_tets, cell_owners)
        continue_game = spawn_results[0]
        focused_tetromino = spawn_results[1]
        # As always, updates the ghost piece after messing with the pieces.
        movement.update_ghost_piece(grid, focused_tet, ghost_piece_tiles)
        # Adds a cooldown to prevent pieces being spammed.
        piece_spawn_cooldown = 20

        # Allows piece holding to be used again.
        utility_funcs.piece_has_been_held = False

    # Increments the piece spawning cooldown every frame.
    if piece_spawn_cooldown > 0:  
        piece_spawn_cooldown -= 1
    
    # 
    if not display_start_menu:
        if movement_cooldown == 0:
            # Gets player inputs, then calls other functions if movement
            # occurred / tried to occur.
            #if movement.get_movement(grid, focused_tetromino, cell_owners):
            if input_handling.get_repeatable_inputs(grid, cell_owners, focused_tetromino):
                movement.update_ghost_piece(grid, focused_tet, ghost_piece_tiles)
                draw_game.print_grid(grid, ghost_piece_tiles)
                # Prevents pieces being moved too quickly, especially when 
                # the input is being held.
                movement_cooldown += 7
        
        elif movement_cooldown > 0:
            movement_cooldown -= 1
    else:
        # Implements the attractor whenever the start menu is open.
        # Cooldown is to prevent the attractor running in ~4 seconds.
        # The cooldown is also required to allow gravity 
        # and line clearing time to be run. 
        if movement_cooldown == 0:
            next_input: str = attractor.return_attractor_input()
            # Seperates out piece spawning inputs from movement inputs.
            if next_input in ["1", "2", "3", "4", "5", "6", "7"]:
                spawn_results = utility_funcs.spawn_tetromino(
                    grid, focused_tet, piece_sequence, 
                    all_tets, cell_owners
                )
                focused_tetromino = spawn_results[1]
                movement.update_ghost_piece(grid, focused_tet, ghost_piece_tiles)
            else:
                movement.process_given_input(
                    next_input, grid, focused_tetromino, 
                    cell_owners, piece_sequence, all_tetrominos, 
                    ghost_piece_tiles
                )
            movement_cooldown += 7 # TESTING ONLY, replace with 7 once done creating the attractor steps
        elif movement_cooldown > 0:
            movement_cooldown -= 1



if __name__ == "__main__":
    clock = pygame.time.Clock() 

    # Runs basically forever
    run_game: bool = True
    while run_game:
        # Resets (almost) all variables before running the game
        start_game()

        # Displays the start menu and the attractor until the user
        # presses <key> to start the game
        display_start_menu = True
        background_iter = 0
        piece_sequence = attractor.setup_piece_sequence(piece_sequence)
        piece_sequence = attractor.setup_piece_sequence(piece_sequence)
        while display_start_menu:
            # Draws the start menu and attractor onto the screen.
            draw_game.screen.fill(draw_game.background_colour)
            draw_game.main_game(
                grid, cell_owners, 13, ghost_piece_tiles, 
                score, lines_cleared, piece_sequence, all_tetrominos,
                utility_funcs.held_piece
            )
            display_start_menu = False if draw_game.start_menu(13) else True

            frame += 1
            update(frame, grid, all_tetrominos, continue_game, gravity_cooldown, cell_owners, focused_tetromino, piece_sequence)

            # Flips the updated display onto the screen
            pygame.display.flip()

            # Allows you to quit whilst the attractor runs
            # TODO FIX THIS IT IS BROKEN
            for event in pygame.event.get():
                if event.type == pygame.QUIT and can_quit:
                    pygame.quit()
                    run_game = False
                    print("Hola")
                    sleep(5)
                    break
            
            # Waits ~1/60 seconds to try and make the game run at 60 fps.
            dt = clock.tick(60) / 1000

            # Reinserts the attractor's piece sequence into 'piece_sequence'
            # whenever the attractor is about to loop.
            if attractor.attractor_step == len(attractor.steps) - 1:
                piece_sequence = attractor.setup_piece_sequence(piece_sequence)
        
        # Resets (almost) all variables to undo changes made by the attractor.
        start_game()
        
        # Spawns the starting piece
        focused_tetromino = utility_funcs.spawn_tetromino(grid, focused_tetromino, piece_sequence, all_tetrominos, cell_owners)[1]
        all_tetrominos.append(focused_tetromino)
        utility_funcs.add_tetromino(focused_tetromino, grid, cell_owners)
        


        # Main game loop
        running: bool = True
        frame = 0
        while running:
            frame += 1
            # Uses pygame.event.get() to get pygame.QUIT events and
            # any controls that can't be held down, such as rotation.
            for event in pygame.event.get():
                if event.type == pygame.QUIT and can_quit:
                    running = False
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    #if movement.pygame_event_handler(event, grid, focused_tetromino, cell_owners, piece_sequence, all_tetrominos):
                    if input_handling.handle_pygame_events(event, grid, cell_owners, focused_tetromino, piece_sequence, all_tetrominos):
                        movement.update_ghost_piece(grid, focused_tetromino, ghost_piece_tiles)
            
            # Flushes the screen then draws the game.
            draw_game.screen.fill(draw_game.background_colour)
            draw_game.main_game(grid, cell_owners, 13, ghost_piece_tiles, score, lines_cleared, piece_sequence, all_tetrominos, utility_funcs.held_piece)

            # Flips the updated display onto the screen.
            pygame.display.flip()

            # Runs all the functions that operate the game.
            update(frame, grid, all_tetrominos, continue_game, gravity_cooldown, cell_owners, focused_tetromino, piece_sequence)

            # Waits ~1/60 seconds to try and make the game run at 60 fps.
            dt = clock.tick(60) / 1000

            if not continue_game:
                break
        
        # Funny message whenever the player loses.
        print("Player lost lollllll")
        sleep(3)


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

Make pretty
Make the attractor change the next_pieces display.

Whenever the attractor loops again, it needs to reinsert the pieces into piece_sequence

Documentation
 - attractor.py DONE
 - draw_game.py DONE
 - gravity.py DONE
 - line_clearing.py DONE
 - main.py 
 - movement.py DONE
 - rotation.py DONE
 - tetromino.py DONE
 - utility_funcs.py DONE

Customisable controls 

"""