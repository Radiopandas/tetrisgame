import pygame

from tetromino import Tetromino
from json_parser import get_file_data
from utility_funcs import tet_to_pattern

pygame.init()

###################################################################################################
#------------------------------------------ Global vars ------------------------------------------#
###################################################################################################
screen_dimensions = pygame.display.Info()

screen_w = 640
screen_h = 360

screen_scale: int = int(screen_dimensions.current_h / screen_h)

grid_width: int = 0
grid_height: int = 0
cell_width: int = 0

font: str = 'Lexus'

base_font = None
base_font_size: int = 0

piece_display_font = None
piece_display_font_size: int = 0 # 16

controls_font = None
controls_font_size: int = 0 # 16

controls_title_font = None
controls_title_font_size: int = 0 # 24

board_offset: int = 0

###################################################################################################
#---------------------------------------- Setup functions ----------------------------------------#
###################################################################################################

def set_grid_size(width: int, height: int):
    global grid_width, grid_height
    grid_width = width
    grid_height = height


def initialise_base_font(size: int):
    global base_font, base_font_size
    base_font_size = size * screen_scale
    base_font = pygame.font.SysFont(font, base_font_size)


def initialise_piece_display_font(size: int):
    global piece_display_font, piece_display_font_size
    piece_display_font_size = size * screen_scale
    piece_display_font = pygame.font.SysFont(font, piece_display_font_size)


def initialise_controls_font(size: int):
    global controls_font, controls_font_size
    controls_font_size = size * screen_scale
    controls_font = pygame.font.SysFont(font, controls_font_size)


def initialise_controls_title_font(size: int):
    global controls_title_font, controls_title_font_size
    controls_title_font_size = size * screen_scale
    controls_title_font = pygame.font.SysFont(font, controls_title_font_size)



###################################################################################################
#--------------------------------------- Utility functions ---------------------------------------#
###################################################################################################

def reset():
    global grid_width, grid_height, cell_width
    grid_width = 0
    grid_height = 0
    cell_width = 0


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
        
###################################################################################################
#---------------------------------------- Main functions -----------------------------------------#
###################################################################################################

def draw_grid(
        screen: pygame.Surface,
        tetrominos: list[Tetromino],
        ghost_piece: Tetromino,
        outline_thickness: int
    ):
    global cell_width, board_offset
    # Calculates how wide to make each cell
    cell_width = (screen_h // (grid_height + 2)) * screen_scale

    # Calculates the board offset to have the grid centred
    board_offset = (screen_dimensions.current_w // 2) - cell_width * ((grid_width / 2) + 1)

    # Draws the ghost piece
    if ghost_piece:
        ghost_piece_colour = set_draw_colour(8)
        for cell in ghost_piece.cells:
            x, y = cell[0], cell[1]
            cell_rect = pygame.Rect(
                cell_width * (x + 1) + board_offset, 
                cell_width * (y + 1), 
                cell_width, 
                cell_width
            )
            pygame.draw.rect(screen, ghost_piece_colour, cell_rect)

    # Draws the Tetrominos
    for tetromino in tetrominos:
        cells = tetromino.cells
        tetromino_colour = set_draw_colour(tetromino.tet_type)
        for cell in cells:
            x, y = cell[0], cell[1]
            cell_rect = pygame.Rect(
                cell_width * (x + 1) + board_offset, 
                cell_width * (y + 1), 
                cell_width, 
                cell_width
            )
            pygame.draw.rect(screen, tetromino_colour, cell_rect)
    
    
    
    # Draws the grid outline
    outline_rect = pygame.Rect(
        cell_width + board_offset - outline_thickness,
        cell_width - outline_thickness,
        cell_width * grid_width + 2 * outline_thickness,
        cell_width * grid_height + 2 * outline_thickness
    )
    pygame.draw.rect(screen, "white", outline_rect, outline_thickness)


def draw_stats(screen: pygame.Surface, score: int, lines: int, level: int):
    global board_offset
    text_area_x_offset = board_offset + cell_width * (grid_width + 2)

    # Calculates the positions to display each stat.
    level_position = (text_area_x_offset + cell_width, 3 * cell_width - 20)
    lines_position = (text_area_x_offset + cell_width, 5 * cell_width - 20)
    score_position = (text_area_x_offset + cell_width, 7 * cell_width - 20)

    # Renders all the stats.
    level_display = base_font.render(
        f"Level: {level:02}", False, 
        (255, 255, 255)
    )
    lines_display = base_font.render(
        f"Lines cleared: {lines:03}", False, 
        (255, 255, 255)
    )
    score_display = base_font.render(
        f"Score: {score:05}", False, 
        (255, 255, 255)
    )

    # Merges them all onto the screen.
    screen.blit(level_display, level_position)
    screen.blit(lines_display, lines_position)
    screen.blit(score_display, score_position)


def draw_next_pieces(screen: pygame.Surface, next_pieces: list[int]):
    global piece_display_font, board_offset
    for index, piece in enumerate(next_pieces):
        # Creates a grid of which tiles to draw.
        pattern: list = tet_to_pattern(piece)

        piece_colour = set_draw_colour(piece)

        # Calculates the position to display the next tetromino.
        text_area_x_offset: int = board_offset + cell_width * (grid_width + 2)
        position = pygame.math.Vector2(
            text_area_x_offset + cell_width + (cell_width // 2 if piece not in [1, 4] else 0),
            (12 + (3 * index)) * cell_width - (cell_width // 2 if piece == 1 else 0)
        )

        # Draws the cells in the tetromino.
        for y, row in enumerate(pattern):
            for x, cell in enumerate(row):
                if cell:
                    cell_rect = pygame.Rect(
                        position.x + cell_width * x,
                        position.y + cell_width * y,
                        cell_width,
                        cell_width
                    )
                    pygame.draw.rect(screen, piece_colour, cell_rect)
    
    # Draws a bounding box around the pieces.
    outline_thickness: int = 2 * screen_scale # How thick to draw the box.
    border_thickness: int = 7 * screen_scale # How much of a gap to leave around the pieces.
    outline_rect = pygame.Rect(
        text_area_x_offset + cell_width - border_thickness,
        12 * cell_width - border_thickness,
        4 * cell_width + 2 * border_thickness,
        8 * cell_width + 2 * border_thickness
    )
    pygame.draw.rect(screen, "white", outline_rect, outline_thickness)

    # Draws some small lines to differentiate the very next piece.
    # Left line.
    pygame.draw.line(screen, "white",
        (text_area_x_offset + cell_width - border_thickness,
            (12 + 2.5) * cell_width),
        (text_area_x_offset + 2 * cell_width - border_thickness + outline_thickness,
        (12 + 2.5) * cell_width),
        outline_thickness
    )

    # Right line.
    pygame.draw.line(screen, "white",
        (text_area_x_offset + 6 * cell_width - border_thickness - outline_thickness,
            (12 + 2.5) * cell_width),
        (text_area_x_offset + 5 * cell_width - border_thickness - outline_thickness,
            (12 + 2.5) * cell_width),
        outline_thickness
    )

    # Draws some text to make clear what is being drawn.
    text_pos = pygame.math.Vector2( 
        text_area_x_offset + cell_width,
        10.4 * cell_width
    )
    text_display = piece_display_font.render("Next piece", False, "white")
    screen.blit(text_display, text_pos)


def draw_held_piece(screen: pygame.Surface, held_piece: int):
    global piece_display_font, board_offset

    # Calculates the display offset.
    x_offset: int = board_offset - 5 * cell_width
    
    if held_piece:
        pattern = tet_to_pattern(held_piece)
        piece_colour = set_draw_colour(held_piece)
    
        # Calculates the position to display the held piece.
        position = pygame.math.Vector2(
            x_offset + cell_width + (cell_width // 2 if held_piece not in [1, 4] else 0),
            3 * cell_width - (cell_width // 2 if held_piece == 1 else 0)
        )

        # Draws the held piece according to 'pattern'.
        for y, row in enumerate(pattern):
            for x, cell in enumerate(row):
                if cell:
                    cell_rect = pygame.Rect(
                        position.x + cell_width * x, 
                        position.y + cell_width * y,
                        cell_width,
                        cell_width
                    )
                    pygame.draw.rect(screen, piece_colour, cell_rect)
    
    # Draws an outline around the held piece.
    outline_thickness: int = 2 * screen_scale
    border_thickness: int = 3 * screen_scale
    outline_rect = pygame.Rect(
        x_offset + cell_width - border_thickness,
        2 * cell_width - border_thickness,
        4 * cell_width + 2 * border_thickness,
        4 * cell_width + 2 * border_thickness
    )
    pygame.draw.rect(screen, "white", outline_rect, outline_thickness)

    # Draws some text explaining what is being drawn.
    text_pos = pygame.math.Vector2(
        x_offset + cell_width - border_thickness + 4 * screen_scale,
        cell_width - border_thickness
    )
    text_display = piece_display_font.render("Held piece", False, "white")
    screen.blit(text_display, text_pos)


def draw_controls(screen: pygame.Surface, controls: dict):
    global board_offset, controls_font, controls_title_font

    # Calculates the x-offset for the controls display area,
    controls_area_x_offset: int = 100 * screen_scale

    # Calculates the positions for each control,
    control_positions: dict = {}
    for index, control in enumerate(controls.keys()):
        control_position = pygame.math.Vector2(
            controls_area_x_offset,
            index * controls_font_size * 2 + 50 * screen_scale + 128 * screen_scale
        )
        control_positions[control] = control_position
    
    # Renders them all to text surfaces,
    rendered_controls: dict = {}
    for index, control in enumerate(controls.keys()):
        control_display = controls_font.render(
            f"{control} : {controls[control]}", False, "white"
        )
        rendered_controls[control] = control_display
    
    # Displays them all.
    for control in rendered_controls.keys():
        screen.blit(rendered_controls[control], control_positions[control])
    
    # Draws the bounding box.
    outline_thickness: int = 3 * screen_scale
    border_thickness: int = 13 * screen_scale
    outline_rect = pygame.Rect(
        controls_area_x_offset - border_thickness,
        178 * screen_scale - border_thickness,
        controls_area_x_offset - 30 * screen_scale + 73 * screen_scale,
        117 * screen_scale + 2 * border_thickness - 2 * outline_thickness
    )
    pygame.draw.rect(screen, "white", outline_rect, outline_thickness)

    # Draws 'Controls' above the controls box
    controls_title_pos = pygame.math.Vector2(
        controls_area_x_offset,
        178 * screen_scale - 2.1 * controls_font_size
    )
    controls_title_display = controls_title_font.render("Controls", False, "white")
    screen.blit(controls_title_display, controls_title_pos)