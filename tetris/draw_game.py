"""
Filename: draw_game.py
Last updated: 5/05/2025
Description: Python script containing various functions to draw the game
in a seperate window using pygame.
"""
import utility_funcs
import pygame
from tetromino import Tetromino

width: int = 0
height: int = 0


def set_grid_size(_width: int, _height: int):
    """Called from 'main.py' to tell 'draw_game.py' the play_area size."""
    global height, width
    height = _height
    width = _width


# Some setup stuff for pygame.
pygame.init()
pygame.font.init()

# Sets up the screen.
screen_info = pygame.display.Info()
screen_w = screen_info.current_w
screen_h = screen_info.current_h
# Subtracts 60 to leave room for the control bar at the top.
screen_h -= 60

screen = pygame.display.set_mode((screen_w, screen_h))

cell_width: int = 0

# Sets up the font.
font_size: int = 0
base_font = None


background_colour = pygame.Color(20, 20, 20)

var_defaults = [0, 0, 0, 0, None]

def reset():
    """Resets all necessary local global variables."""
    global width, height, cell_width, font_size, base_font, var_defaults

    width, height, cell_width, font_size, base_font = var_defaults

def set_draw_colour(piece_type: int) -> pygame.Color:
    """Returns a pygame.Color object representing the colour 
    to draw a piece with."""
    match piece_type:
        case 1:
            return pygame.Color(0, 255, 255)
        case 2:
            return pygame.Color(0, 0, 255)
        case 3:
            return pygame.Color(255, 170, 0)
        case 4:
            return pygame.Color(255, 255, 0)
        case 5:
            return pygame.Color(0, 255, 0)
        case 6:
            return pygame.Color(153, 0, 255)
        case 7:
            return pygame.Color(255, 0, 0)
        case 8:
            return pygame.Color(198, 198, 198)
        case _:
            return pygame.Color(255, 255, 255)

def print_grid(
        grid: list[list[bool]], 
        ghost_tiles: list[list[bool]]
    ):
    """Prints the Tetris game in the terminal using box drawing characters."""
    print("\033c")
    print("┏" + "━━" * len(grid[0]) + "┓")
    for y, row in enumerate(grid):
        print('┃', end="")
        for x, cell in enumerate(row):
            if cell:
                print("██", end="")
            else:
                if ghost_tiles[y][x]:
                    print("██", end="")
                else:
                    print("  ", end="")
        print('┃')
    
    print("┗" + "━━" * len(grid[0]) + "┛")

def draw_grid(
        grid: list[list[bool]],
        cell_owners: list[list[Tetromino | None]], 
        board_offset: int, 
        ghost_tiles: list[list[bool]], 
        outline_thickness: int
    ):
    """Draws each cell in the grid using pygame.draw.rect()."""
    global cell_width
    # Calculates the width of each printed cell
    cell_width = screen_h // (height + 2)
    # Width of the area that the actual game board is printed in

    
    # Prints the tetrominos
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            # If a cell isn't empty, gets relevant colour, calculates the 
            # coordinates and draws the cell.
            if cell:
                colour = set_draw_colour(cell_owners[y][x].tet_type)
                new_rect = pygame.Rect(cell_width * (x + 1 + board_offset), cell_width * (y + 1), cell_width, cell_width)
                pygame.draw.rect(screen, colour, new_rect)
            else:
                # If a cell is empty on the main grid but filled on
                # ghost_tiles, draws it anyways using a different colour.
                if ghost_tiles[y][x]:
                    colour = set_draw_colour(8)
                    new_rect = pygame.Rect(cell_width * (x + 1 + board_offset), cell_width * (y + 1), cell_width, cell_width)
                    pygame.draw.rect(screen, colour, new_rect)
    
    # Prints the grid outline
    outline_rect = pygame.Rect(
        ((board_offset + 1) * cell_width - outline_thickness), 
        cell_width - outline_thickness, 
        cell_width * (width + 2) - 2*(cell_width - outline_thickness), 
        cell_width * (height + 2) - 2*(cell_width - outline_thickness)
    )
    pygame.draw.rect(screen, "white", outline_rect, outline_thickness)


def draw_stats(board_offset: int, score: int, lines: int, level: int):
    """Draws the current level, lines cleared and score using pygame
    text displays."""
    global base_font, font_size
    # Initialises the font for displaying the text.
    if not base_font:
        font_size = screen_h // (height + 2)
        base_font = pygame.font.SysFont('Lexus', font_size)
    
    # How many pixels from the left the stats area should be offset.
    text_area_offset = cell_width * (width + board_offset + 2)

    # Calculates the positions to display each stat.
    level_position = (text_area_offset + cell_width, 3 * cell_width)
    lines_position = (text_area_offset + cell_width, 5 * cell_width)
    score_position = (text_area_offset + cell_width, 7 * cell_width)
    
    # Renders all the stats.
    level_display = base_font.render(
        f"Level: {level:02}", False, 
        (255, 255, 255), (155, 155, 155)
    )
    lines_display = base_font.render(
        f"Lines cleared: {lines:03}", False, 
        (255, 255, 255), (155, 155, 155)
    )
    score_display = base_font.render(
        f"Score: {score:05}", False, 
        (255, 255, 255), (155, 155, 155)
    )

    # Merges them all onto the screen.
    screen.blit(level_display, level_position)
    screen.blit(lines_display, lines_position)
    screen.blit(score_display, score_position)


def draw_next_pieces(next_pieces: list[int], board_offset: int):
    """Draws the next 3 pieces in 'piece_sequence'(main.py) 
    using pygame.draw.rect()."""

    for i in range(len(next_pieces)):
        # Creates a grid of which tiles to draw
        pattern: list = utility_funcs.tet_to_pattern(next_pieces[i])

        piece_colour = set_draw_colour(next_pieces[i])

        # Calculates the position to display the next tetromino.
        text_area_offset: int = cell_width * (width + board_offset + 2)
        position = (text_area_offset + cell_width, (9 +(3 * i)) * cell_width)

        # Actually draws each cell in the tetromino
        for y, row in enumerate(pattern):
            for x, cell in enumerate(row):
                if cell:
                    new_rect = pygame.Rect(
                        position[0] + cell_width * x, 
                        position[1] + cell_width * y, 
                        cell_width, 
                        cell_width
                        )
                    pygame.draw.rect(screen, piece_colour, new_rect)


def draw_held_piece(held_piece: int, board_offset: int):
    """Draws the current held piece if there is one, otherwise returns early."""
    if not held_piece:
        return
        
    # Gets the pattern and colour of the held piece.
    pattern: list = utility_funcs.tet_to_pattern(held_piece)
    piece_colour = set_draw_colour(held_piece)

    # Calculates the position to display the held piece.
    offset: int = cell_width * (board_offset - 5)
    position = (offset + cell_width, 4 * cell_width)

    # Draws the cells of the held piece according to 'pattern'.
    for y, row in enumerate(pattern):
            for x, cell in enumerate(row):
                if cell:
                    new_rect = pygame.Rect(position[0] + cell_width * x, position[1] + cell_width * y, cell_width, cell_width)
                    pygame.draw.rect(screen, piece_colour, new_rect)
    

def draw_game(
        grid: list[list[bool]],
        cell_owners: list[list[Tetromino | None]], 
        board_offset: int, 
        ghost_tiles: list[list[bool]], 
        score: int, 
        lines_cleared: int, 
        piece_sequence: list[int], 
        held_piece: int = None
    ) -> None:
    """Calls several other functions to draw everything onto the screen."""

    draw_grid(grid, cell_owners, board_offset, ghost_tiles, 5)

    draw_stats(board_offset, score, lines_cleared, lines_cleared // 10)

    draw_next_pieces(piece_sequence[0:3], board_offset)

    draw_held_piece(held_piece, board_offset)


def draw_start_menu(board_offset: int) -> bool:
    """Draws a start menu consisting of the title and basic instructions."""
    global screen_w

    # Initialises the fonts.
    title_font = pygame.font.SysFont('Lexus', 100)

    # Calculates the offset required to be in the centre of the screen.
    screen_midpoint = screen_w // 2

    # Draws the title.
    title_position = (screen_midpoint - 126, 100)
    title_display = title_font.render("SIRTET", False, (255, 255, 255), (155, 155, 155))

    screen.blit(title_display, title_position)
    
    
    # Prints instructions ('Press '0' to begin').
    instructions_position = (screen_midpoint - 281, 300)
    instructions_display = title_font.render("Press \'0\' to begin", False, (255, 255, 255), (155, 155, 155))

    screen.blit(instructions_display, instructions_position)
    
    # Checks for the user pressing <key> to exit the start screen.
    # Returns True if <key> is pressed, else False. 
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                return True
        elif event.type == pygame.QUIT:
            pygame.quit()
    return False

def draw_grid_lines(h_lines: int):
    """Draws a grid on the screen in solid black lines for the sake
    of more easily aligning visual elements."""
    spacing = screen_w // h_lines

    v_lines = screen_h // spacing

    # Draws all the horizontal lines.
    for x in range(h_lines):
        pygame.draw.line(screen, (0, 0, 0), (spacing * x, 0), (spacing * x, screen_h), width = 5)
    
    # Draws all the vertical lines.
    for y in range(v_lines):
        pygame.draw.line(screen, (0, 0, 0), (0, spacing * y), (screen_w, spacing * y), width = 5)
    
    # Prints the position of a mouse click to allow for easier calculations.
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())