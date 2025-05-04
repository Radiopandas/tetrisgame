#from utility_funcs import tet_to_pattern, held_piece
import utility_funcs
import pygame

width: int = 0
height: int = 0

def set_held_piece(_held_piece: int):
    pass

def set_grid_size(_width: int, _height: int):
    global height, width
    height = _height
    width = _width


# Some setup stuff for pygame
pygame.init()
pygame.font.init()

# Sets up the screen
screen_info = pygame.display.Info()
screen_w = screen_info.current_w
screen_h = screen_info.current_h
# Subtracts 60 to leave room for the control bar
screen_h -= 60

screen = pygame.display.set_mode((screen_w, screen_h))

cell_width: int = 0

# Sets up the font
font_size: int = 0
base_font = None


background_colour = pygame.Color(20, 20, 20)

var_defaults = [0, 0, 0, 0, None]

def reset():
    global width, height, cell_width, font_size, base_font, var_defaults

    width, height, cell_width, font_size, base_font = var_defaults

def set_draw_colour(piece_type: int) -> pygame.Color:
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

def print_grid(grid, ghost_tiles):
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

def draw_grid(grid, cell_owners, board_offset: int, ghost_tiles: list, outline_thickness: int):
    global cell_width
    # Calculates the width of each printed cell
    cell_width = screen_h // (height + 2)
    # Width of the area that the actual game board is printed in

    
    # Prints the tetrominos
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell:
                colour = set_draw_colour(cell_owners[y][x].tet_type)
                new_rect = pygame.Rect(cell_width * (x + 1 + board_offset), cell_width * (y + 1), cell_width, cell_width)
                pygame.draw.rect(screen, colour, new_rect)
            else:
                if ghost_tiles[y][x]:
                    colour = set_draw_colour(8)
                    new_rect = pygame.Rect(cell_width * (x + 1 + board_offset), cell_width * (y + 1), cell_width, cell_width)
                    pygame.draw.rect(screen, colour, new_rect)
    
    # Prints the grid outline
    outline_rect = pygame.Rect(((board_offset + 1) * cell_width - outline_thickness), cell_width - outline_thickness, cell_width * (width + 2) - 2*(cell_width - outline_thickness), cell_width * (height + 2) - 2*(cell_width - outline_thickness))
    pygame.draw.rect(screen, "white", outline_rect, outline_thickness)


def draw_stats(board_offset, score, lines, level):
    global base_font, font_size
    # Initialises the font for displaying the text
    if not base_font:
        font_size = screen_h // (height + 2)
        base_font = pygame.font.SysFont('Lexus', font_size)
    
    # How many pixels from the left the stats area should be offset
    text_area_offset = cell_width * (width + board_offset + 2)

    # Calculates the positions to display each stat
    level_position = (text_area_offset + cell_width, 3 * cell_width)
    lines_position = (text_area_offset + cell_width, 5 * cell_width)
    score_position = (text_area_offset + cell_width, 7 * cell_width)
    
    # Renders all the stats.
    level_display = base_font.render(f"Level: {level:02}", False, (255, 255, 255), (155, 155, 155))
    lines_display = base_font.render(f"Lines cleared: {lines:03}", False, (255, 255, 255), (155, 155, 155))
    score_display = base_font.render(f"Score: {score:05}", False, (255, 255, 255), (155, 155, 155))

    # Merges them all onto the screen.
    screen.blit(level_display, level_position)
    screen.blit(lines_display, lines_position)
    screen.blit(score_display, score_position)


def draw_next_pieces(next_pieces: list[int], board_offset: int):
    for i in range(len(next_pieces)):
        # Creates a grid of which tiles to draw
        pattern: list = utility_funcs.tet_to_pattern(next_pieces[i])

        piece_colour = set_draw_colour(next_pieces[i])

        # Calculates the position to display the next tet.
        text_area_offset: int = cell_width * (width + board_offset + 2)
        position = (text_area_offset + cell_width, (9 +(3 * i)) * cell_width)

        for y, row in enumerate(pattern):
            for x, cell in enumerate(row):
                if cell:
                    new_rect = pygame.Rect(position[0] + cell_width * x, position[1] + cell_width * y, cell_width, cell_width)
                    pygame.draw.rect(screen, piece_colour, new_rect)


def draw_held_piece(held_piece: int, board_offset: int):
    if not held_piece:
        return
        
    # Gets the pattern of the held piece
    pattern: list = utility_funcs.tet_to_pattern(held_piece)

    piece_colour = set_draw_colour(held_piece)

    # Calculates the position to display the held piece
    offset: int = cell_width * (board_offset - 5)
    position = (offset + cell_width, 4 * cell_width)

    for y, row in enumerate(pattern):
            for x, cell in enumerate(row):
                if cell:
                    new_rect = pygame.Rect(position[0] + cell_width * x, position[1] + cell_width * y, cell_width, cell_width)
                    pygame.draw.rect(screen, piece_colour, new_rect)
    

def draw_game(grid, cell_owners, board_offset, ghost_tiles, score, lines_cleared, piece_sequence, held_piece = None) -> None:
    """Calls several other functions to draw everything onto the screen."""

    draw_grid(grid, cell_owners, board_offset, ghost_tiles, 5)

    draw_stats(board_offset, score, lines_cleared, lines_cleared // 10)

    draw_next_pieces(piece_sequence[0:3], board_offset)

    draw_held_piece(held_piece, board_offset)

    #draw_grid_lines(20)


def draw_start_menu(board_offset: int) -> bool:
    global screen_w

    # Initialises the fonts
    title_font = pygame.font.SysFont('Lexus', 100)

    # Calculates the offset required to be in the centre of the screen
    screen_midpoint = screen_w // 2

    # Draw the title
    title_position = (screen_midpoint - 126, 100)
    title_display = title_font.render("SIRTET", False, (255, 255, 255), (155, 155, 155))

    screen.blit(title_display, title_position)
    
    
    # Prints instructions ('Press enter to begin')
    instructions_position = (screen_midpoint - 281, 300)
    instructions_display = title_font.render("Press \'0\' to begin", False, (255, 255, 255), (155, 155, 155))

    screen.blit(instructions_display, instructions_position)

    #draw_grid_lines(20)
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                print("akjsdhkgjasdhj")
                return True
        elif event.type == pygame.QUIT:
            pygame.quit()
    return False

def draw_grid_lines(h_lines):
    spacing = screen_w // h_lines

    #print(f"Gridline spacing: {spacing}")

    v_lines = screen_h // spacing

    for x in range(h_lines):
        pygame.draw.line(screen, (0, 0, 0), (spacing * x, 0), (spacing * x, screen_h), width = 5)
    
    for y in range(v_lines):
        pygame.draw.line(screen, (0, 0, 0), (0, spacing * y), (screen_w, spacing * y), width = 5)
    
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())