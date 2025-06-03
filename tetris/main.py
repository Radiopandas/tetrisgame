import rotation
import gravity
import line_clearing
import draw_game
from tetromino import Tetromino
import utility_funcs
import movement
import pygame #
import copy #
import attractor
import input_handling
import leaderboard
import draw_settings_menu
import server_client
import debug_console
from random import shuffle #

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

gravity_cooldown: int = 60
piece_sequence: list[int] = [1, 2, 3, 4, 5, 6, 7]
held_piece: int = 0

attractor_needs_to_wait: bool = False

display_start_menu: bool = True
continue_game: bool = True
movement_cooldown: int = 0
piece_spawn_cooldown: int = 0
frame: int = 0

instant_gravity_after_clearing: bool = True

# Only to be used when displaying the game to people
DEBUG_MODE: bool = True
can_quit: bool = True
use_server: bool = False

all_vars = [
    width, height, focused_tetromino, grid, cell_owners, all_tetrominos,
    ghost_piece_tiles, score, lines_cleared, gravity_cooldown,
    piece_sequence, held_piece, continue_game, movement_cooldown,
    piece_spawn_cooldown, frame
    ]

var_defaults = [
    10, 22, Tetromino([]), [], [], [],
    utility_funcs.create_grid(width, height, False), 0, 0, 60,
    [1, 2, 3, 4, 5, 6, 7] if not debug_console.debug_mode else [1, 1, 1, 1, 1, 1, 1]
    , 0, True, 0, 0, 0
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
    
    if debug_console.debug_mode:
        piece_sequence = [1, 1, 1, 1, 1, 1, 1]


def restart_game():
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
    utility_funcs.init_colour_gradient(pygame.Color("Red"), pygame.Color("Blue"), width, height)
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
    global focused_tetromino, continue_game, piece_spawn_cooldown, \
        movement_cooldown, score, lines_cleared, gravity_cooldown, \
        display_start_menu, attractor_needs_to_wait, \
        instant_gravity_after_clearing

    if not keep_playing:
        return


    if input_handling.just_hard_dropped:
        # Checks for and clears filled rows.
        lines_just_cleared = line_clearing.check_rows(grid, cell_owners, all_tets)
        # Increments the number of lines cleared, updates the score and potentially
        # updates the gravity rate.
        score += utility_funcs.update_scores(lines_just_cleared)
        lines_cleared += lines_just_cleared
        if gravity_rate > 10:
            gravity_cooldown -= utility_funcs.update_gravity_rate(lines_cleared, lines_just_cleared)
            if gravity_cooldown < 10:
                gravity_cooldown = 10

        # Moves all lines down by the number of lines cleared
        if lines_just_cleared > 0 and instant_gravity_after_clearing:
            movement.ghost_piece.cells = []
            for i in range(lines_just_cleared):
                
                draw_game.screen.fill(draw_game.background_colour)
                draw_game.main_game(
                grid, cell_owners, 13, ghost_piece_tiles, 
                score, lines_cleared, piece_sequence, all_tetrominos, 
                focused_tetromino, utility_funcs.held_piece, False
                )
                if display_start_menu:
                    draw_game.start_menu()

                pygame.display.flip()
                gravity.apply_gravity(grid, all_tets, cell_owners, focused_tet)
                sleep(0.05)
            pygame.display.flip()
        input_handling.just_hard_dropped = False
        #movement.update_ghost_piece(grid, focused_tet, ghost_piece_tiles)

    # Calls the gravity functions, as well as several related functions
    # periodically instead of every single frame.
    if focused_tetromino.gravity_frame % gravity_rate == 0:
        # Applies gravity to every piece, then updates the ghost piece
        # To account for the new changes.
        draw_game.print_grid(grid, ghost_piece_tiles)
        gravity.apply_gravity(grid, all_tets, cell_owners, focused_tet)
        #movement.update_ghost_piece(grid, focused_tet, ghost_piece_tiles)
        
        # Checks for and clears filled rows.
        lines_just_cleared = line_clearing.check_rows(grid, cell_owners, all_tets)
        # Increments the number of lines cleared, updates the score and potentially
        # updates the gravity rate.
        score += utility_funcs.update_scores(lines_just_cleared)
        lines_cleared += lines_just_cleared
        if gravity_rate > 10:
            gravity_cooldown -= utility_funcs.update_gravity_rate(lines_cleared, lines_just_cleared)
            if gravity_cooldown < 10:
                gravity_cooldown = 10

        # Moves all lines down by the number of lines cleared
        if lines_just_cleared > 0 and instant_gravity_after_clearing:
            for i in range(lines_just_cleared):
                
                draw_game.screen.fill(draw_game.background_colour)
                draw_game.main_game(
                grid, cell_owners, 13, ghost_piece_tiles, 
                score, lines_cleared, piece_sequence, all_tetrominos, focused_tetromino,
                utility_funcs.held_piece, False
                )
                if display_start_menu:
                    draw_game.start_menu()

                pygame.display.flip()
                gravity.apply_gravity(grid, all_tets, cell_owners, focused_tet)
                sleep(0.05) 
            pygame.display.flip()
    
    #input_handling.reset_singular_inputs()
    if display_start_menu:
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
                #movement.update_ghost_piece(grid, focused_tet, ghost_piece_tiles)
            else:
                if input_handling.attractor_input_processor(
                    next_input, grid, cell_owners, focused_tetromino
                    ):
                    movement.update_ghost_piece(grid, focused_tet, ghost_piece_tiles)
            movement_cooldown += 7
        elif movement_cooldown > 0:
            movement_cooldown -= 1
    
    # If the current focused piece can't move, it must be on the ground
    # Thus it needs to spawn a new piece for the player to control.
    # Overridden by display_start_menu, since it uses its own functions
    # to do things such as spawning pieces.
    if not focused_tet.can_move and not display_start_menu:
        # Attempts to spawn a new piece, then assigns it to focused_tetromino.
        spawn_results = utility_funcs.spawn_tetromino(grid, focused_tet, piece_sequence, all_tets, cell_owners)
        continue_game = spawn_results[0]
        focused_tetromino = spawn_results[1]

        # Allows piece holding to be used again.
        utility_funcs.piece_has_been_held = False
    
    
    movement.update_ghost_piece(grid, focused_tet, ghost_piece_tiles)


if __name__ == "__main__":
    clock = pygame.time.Clock()

    if use_server:
        HOST = input("Host: ")
        PORT = int(input("Port: "))

        # Creates a connection to the leaderboard server.
        server_client.initialise_server_connection(HOST, PORT)


    # Runs basically forever
    run_game: bool = True
    while run_game:
        # Resets (almost) all variables before running the game
        restart_game()

        # Displays the start menu and the attractor until the user
        # presses <Enter> to start the game
        display_start_menu = True
        background_iter = 0
        piece_sequence = attractor.setup_piece_sequence(piece_sequence)
        piece_sequence = attractor.setup_piece_sequence(piece_sequence)
        while display_start_menu:
            # Allows you to quit whilst the attractor runs
            for event in pygame.event.get():
                if event.type == pygame.QUIT and can_quit:
                    display_start_menu = False
                    run_game = False
                    pygame.quit()
                
                elif event.type == pygame.KEYDOWN:
                    # Key combo to quit the game.
                    if event.key == 45 and (event.mod == 8513 or event.mod == 8769): # ctrl+alt+shift+capslock+'-'
                        display_start_menu = False
                        run_game = False
                        pygame.quit()
                    
                    # Key to close the start menu
                    elif event.key == pygame.K_RETURN:
                        display_start_menu = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_coords = pygame.mouse.get_pos()
                    draw_settings_menu.check_pressed_buttons(mouse_coords, draw_game.screen)
            
            if not display_start_menu:
                break

            # Draws the start menu and attractor onto the screen.
            draw_game.screen.fill(draw_game.background_colour)
            draw_game.main_game(
                grid, cell_owners, 13, ghost_piece_tiles, 
                score, lines_cleared, piece_sequence, all_tetrominos, focused_tetromino,
                utility_funcs.held_piece
            )

            draw_game.start_menu()

            if not draw_settings_menu.settings_menu_open and not debug_console.console_visible:
                #focused_tetromino.gravity_frame += (1 if not input_handling.soft_dropping else 30)
                #frame += 1
                focused_tetromino.gravity_frame += 1
                update(frame, grid, all_tetrominos, continue_game, gravity_cooldown, cell_owners, focused_tetromino, piece_sequence)
                gravity_cooldown = 60

            # Flips the updated display onto the screen
            pygame.display.flip()
            
            # Waits ~1/60 seconds to try and make the game run at 60 fps.
            dt = clock.tick(60) / 1000

            # Reinserts the attractor's piece sequence into 'piece_sequence'
            # whenever the attractor is about to loop.
            if attractor.attractor_step == len(attractor.steps) - 1:
                piece_sequence = attractor.setup_piece_sequence(piece_sequence)
        
        # Checks if the game was quit during the start menu.
        if not run_game:
            break

        # Resets (almost) all variables to undo changes made by the attractor.
        restart_game()
        
        # Spawns the starting piece.
        focused_tetromino = utility_funcs.spawn_tetromino(grid, focused_tetromino, piece_sequence, all_tetrominos, cell_owners)[1]
        all_tetrominos.append(focused_tetromino)
        utility_funcs.add_tetromino(focused_tetromino, grid, cell_owners)
        


        # Main game loop.
        running: bool = True
        frame = 0
        while running:
            
            # Uses pygame.event.get() to get pygame.QUIT events and
            # any controls that can't be held down, such as rotation.
            for event in pygame.event.get():
                if event.type == pygame.QUIT and can_quit:
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    # Key combo to quit the game.
                    if event.key == 45 and (event.mod == 8513 or event.mod == 8769): # ctrl+Lalt/Ralt+shift+capslock+'-'
                        running = False
                    
                    elif event.key == pygame.K_SLASH and (event.mod == 8513 or event.mod == 8769):
                        debug_console.console_visible = not debug_console.console_visible
                        debug_console.command_input_box.flush_buffer()
                        continue

                    if debug_console.console_visible:
                        command_entered: str = debug_console.command_input_box.handle_event(event)
                        if command_entered:
                            debug_console.handle_command(command_entered.lower())
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_coords = pygame.mouse.get_pos()
                    draw_settings_menu.check_pressed_buttons(mouse_coords, draw_game.screen)

            
            if not running:
                run_game = False
                break
            
            # Handles repeating inputs (movement/soft drop) and
            # non-repeating inputs(rotation, hold, hard drop).
            if not draw_settings_menu.settings_menu_open and not debug_console.console_visible:
                input_handling.get_inputs(
                    grid,
                    cell_owners,
                    focused_tetromino,
                    piece_sequence,
                    all_tetrominos
                )
            
            # Flushes the screen then draws the game.
            draw_game.screen.fill(draw_game.background_colour)
            draw_ghost_piece = False if input_handling.just_hard_dropped else True
            draw_game.main_game(grid, cell_owners, 13, ghost_piece_tiles, score, lines_cleared, piece_sequence, all_tetrominos, focused_tetromino, utility_funcs.held_piece, draw_ghost_piece)

            if debug_console.console_visible:
                debug_console.draw_console(draw_game.screen)
            # Flips the updated display onto the screen.
            pygame.display.flip()


            # Runs all the functions that operate the game.
            if not draw_settings_menu.settings_menu_open and not debug_console.console_visible:
                update(frame, grid, all_tetrominos, continue_game, gravity_cooldown, cell_owners, focused_tetromino, piece_sequence)
                focused_tetromino.gravity_frame += 1
                if focused_tetromino.is_on_ground:
                    if not focused_tetromino.check_is_grounded(grid):
                        focused_tetromino.is_on_ground = False
                        focused_tetromino.locking_frame = 0
                    else:
                        focused_tetromino.locking_frame += 1
                        if focused_tetromino.locking_frame == focused_tetromino.MAX_LOCKING_FRAME:
                            focused_tetromino.can_move = False
                            focused_tetromino.is_locked = True

            # Waits ~1/60 seconds to try and make the game run at 60 fps.
            dt = clock.tick(60) / 1000

            # Reduces the cooldowns of all repeatable inputs by the deltaTime
            if not focused_tetromino.is_locked:
                input_handling.update_cooldowns(dt)

            if not continue_game:
                running = False
        

        if not run_game:
            break

        # Waits for the user to enter a name so their score can be stored.
        name_entered: bool = False
        leaderboard.set_score(score)
        leaderboard.draw_name_input = True
        leaderboard.name_input_box.visible = True
        while not name_entered:
            # Continues drawing the game
            draw_game.screen.fill(draw_game.background_colour)
            draw_game.main_game(grid, cell_owners, 13, ghost_piece_tiles, score, lines_cleared, piece_sequence, all_tetrominos, focused_tetromino, utility_funcs.held_piece, draw_ghost_piece)

            pygame.display.update()
            # Checks for quit events, then checks for the user typing
            # into the input box.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_game = False
                    break
                
                else:
                    entered_name = leaderboard.name_input_box.handle_event(event)
                    if entered_name:
                        name_entered = True

                        leaderboard_info = {
                            "Name": entered_name,
                            "Score": score,
                            "Lines cleared": lines_cleared
                        }

                
                        if use_server:
                            server_client.send(leaderboard_info)


                        leaderboard.draw_name_input = False
            
            dt = clock.tick(60) / 1000
        
    if use_server:
        server_client.end_server_connection()
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

Make the buttons change colour slightly when being hovered over

Add a local scoreboard (or, if there is time, a scoreboard that syncs across the network.)

Issue 1:
    When you hard drop a piece, line clearing gets automatically called.
    apply_gravity() then gets called, during which time all cells are marked as able to move.
    Problem occurs when line clearing clears all the cells of the piece.
    When this happens, the gravity function basically skips it and thus it is never marked as
    unable to move, causing a new piece to never be spawned.
    FIXED - Gravity now checks that tetrominos actually have pieces before modifying them.

Issue 2:
    When you hard drop a piece into a line clear, you are able to move it for a few frames
    When the game is trying to run gravity extra times to move pieces down after clearing a line
    FIXED - Gravity now takes an optional 'focused_tet' argument. It checks if this isn't None
        and if input_handling.just_hard_dropped is true, in which case it sets 
        'focused_tet'.can_move back to False after applying gravity to everything

Issue 3:
    When you hard drop a piece and lines get cleared, the ghost piece gets drawn when it really shouldn't.
    FIXED(I think) - Before calling gravity repeatedly after clearing lines, sets the ghost piece's cells to be empty.

If performance is an issue, could make a gravity function that just moves every cell above
a certain row down a certain amount to be used after line clearing.


Change draw_settings_menu and draw_leaderboard to draw everything onto mini canvases that can then be blitted onto the screen
This way, we can save on processing by only redrawing their canvases when they are updated.
Also makes layering easier and would allow the settings menu to have a solid background.
 - draw_settings_menu DONE
 - draw_leaderboard

Change the name entering to:
 - Display what score you got.
 - Only allow 3 characters
 - have the box that they enter the name into be underneath the question.

TODO Maybe:
 - Change the customising controls to allow for null binds. Either
   - Allow for a key to be bound to multiple things (Flip the input map so that the action names are the 'keys' and the pygame keys are the 'values')
   - Make it so that when you bind a control that is already bound, it unbinds the previous action. (eg; LeftArrow is bound to move_left. The user tries to map LeftArrow to rotate_left. This succeeds and move_left is now mapped to nothing.)

 - Add a locking delay to pieces after they land.
 - Base gravity off of each piece instead of a global clock.

When you clear a line and a singylar cell is left to drop, doesn't spawn a new piece until it has fallen completely.
 - for Debugging, just make all the pieces lines to best recreate it.
"""

