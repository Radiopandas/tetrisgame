import tetromino
import pygame

width: int = 0
height: int = 0

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

cell_width: int 

# Sets up the font
font_size: int
my_font: pygame.font.SysFont = None


background_colour = pygame.Color(150, 150, 150)

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

def draw_grid(grid, cell_owners, board_offset: int, ghost_tiles: list):
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
    # Top row
    for x in range(width + 2):
        new_rect = pygame.Rect(cell_width * (x + board_offset), 0, cell_width, cell_width)
        pygame.draw.rect(screen, "black", new_rect)
    # Edges
    for y in range(height):
        new_rect = pygame.Rect(cell_width * (board_offset), cell_width * (y+1), cell_width, cell_width)
        pygame.draw.rect(screen, "black", new_rect)
        new_rect = pygame.Rect(cell_width * (width +1 + board_offset), cell_width * (y+1), cell_width, cell_width)
        pygame.draw.rect(screen, "black", new_rect)
    # Bottom row
    for x in range(width + 2):
        new_rect = pygame.Rect(cell_width * (x + board_offset), cell_width * (height + 1), cell_width, cell_width)
        pygame.draw.rect(screen, "black", new_rect) 

def draw_score(score: int, board_offset: list):
    global my_font, font_size, cell_width
    if not my_font:
        font_size = screen_h // (height + 2) * 2
        my_font = pygame.font.SysFont('Arial', font_size)
    
    play_area_width: int = cell_width * (width + 2)
    score_position = (play_area_width + cell_width * (board_offset + 1), 5 * cell_width)
    score_display = my_font.render(f"Score: {score:05}", False, (0, 0, 0))
    screen.blit(score_display, score_position)


def draw_game(grid, cell_owners, board_offset, ghost_tiles):
    draw_grid(grid, cell_owners, board_offset, ghost_tiles)

    draw_score(100, board_offset)

    # Flips the updated display onto the screen
    pygame.display.flip()