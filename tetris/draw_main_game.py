import pygame

from tetromino import Tetromino
from json_parser import get_file_data
from utility_funcs import tet_to_pattern, set_cell_colour
from random import choice, randint

from math import sqrt

pygame.init()

###################################################################################################
#------------------------------------------ Global vars ------------------------------------------#
###################################################################################################
screen_dimensions = pygame.display.Info()

cur_h = screen_dimensions.current_h

screen_w = 640
screen_h = 360


screen_scale: int = screen_dimensions.current_h // screen_h

ghost_layer: pygame.Surface #= pygame.Surface((screen_w * screen_scale, screen_h * screen_scale))
#ghost_layer.set_alpha(50)

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

fun_mode: bool = True

purple_monkey_dishwasher: pygame.Surface = None


# Honestly this can just be deleted.
fun_mode_colours = [
    pygame.Color("AliceBlue"),
    pygame.Color("AntiqueWhite"),
    pygame.Color("Aqua"),
    pygame.Color("Aquamarine"),
    pygame.Color("Azure"),
    pygame.Color("Beige"),
    pygame.Color("Bisque"),
    pygame.Color("Black"),
    pygame.Color("BlanchedAlmond"),
    pygame.Color("Blue"),
    pygame.Color("BlueViolet"),
    pygame.Color("Brown"),
    pygame.Color("BurlyWood"),
    pygame.Color("CadetBlue"),
    pygame.Color("Chartreuse"),
    pygame.Color("Chocolate"),
    pygame.Color("Coral"),
    pygame.Color("CornflowerBlue"),
    pygame.Color("Cornsilk"),
    pygame.Color("Crimson"),
    pygame.Color("Cyan"),
    pygame.Color("DarkBlue"),
    pygame.Color("DarkCyan"),
    pygame.Color("DarkGoldenRod"),
    pygame.Color("DarkGray"),
    pygame.Color("DarkGreen"),
    pygame.Color("DarkKhaki"),
    pygame.Color("DarkMagenta"),
    pygame.Color("DarkOliveGreen"),
    pygame.Color("DarkOrange"),
    pygame.Color("DarkOrchid"),
    pygame.Color("DarkRed"),
    pygame.Color("DarkSalmon"),
    pygame.Color("DarkSeaGreen"),
    pygame.Color("DarkSlateBlue"),
    pygame.Color("DarkSlateGray"),
    pygame.Color("DarkTurquoise"),
    pygame.Color("DarkViolet"),
    pygame.Color("DeepPink"),
    pygame.Color("DeepSkyBlue"),
    pygame.Color("DimGray"),
    pygame.Color("DodgerBlue"),
    pygame.Color("FireBrick"),
    pygame.Color("FloralWhite"),
    pygame.Color("ForestGreen"),
    pygame.Color("Fuchsia"),
    pygame.Color("Gainsboro"),
    pygame.Color("GhostWhite"),
    pygame.Color("Gold"),
    pygame.Color("Goldenrod"),
    pygame.Color("Gray"),
    pygame.Color("Green"),
    pygame.Color("GreenYellow"),
    pygame.Color("Honeydew"),
    pygame.Color("HotPink"),
    pygame.Color("IndianRed"),
    pygame.Color("Indigo"),
    pygame.Color("Ivory"),
    pygame.Color("Khaki"),
    pygame.Color("Lavender"),
    pygame.Color("LavenderBlush"),
    pygame.Color("LawnGreen"),
    pygame.Color("LemonChiffon"),
    pygame.Color("LightBlue"),
    pygame.Color("LightCoral"),
    pygame.Color("LightCyan"),
    pygame.Color("LightGoldenrodYellow"),
    pygame.Color("LightGray"),
    pygame.Color("LightGreen"),
    pygame.Color("LightPink"),
    pygame.Color("LightSalmon"),
    pygame.Color("LightSeaGreen"),
    pygame.Color("LightSkyBlue"),
    pygame.Color("LightSlateGray"),
    pygame.Color("LightSteelBlue"),
    pygame.Color("LightYellow"),
    pygame.Color("Lime"),
    pygame.Color("LimeGreen"),
    pygame.Color("Linen"),
    pygame.Color("Magenta"),
    pygame.Color("Maroon"),
    pygame.Color("MediumAquamarine"),
    pygame.Color("MediumBlue"),
    pygame.Color("MediumOrchid"),
    pygame.Color("MediumPurple"),
    pygame.Color("MediumSeaGreen"),
    pygame.Color("MediumSlateBlue"),
    pygame.Color("MediumSpringGreen"),
    pygame.Color("MediumTurquoise"),
    pygame.Color("MediumVioletRed"),
    pygame.Color("MidnightBlue"),
    pygame.Color("MintCream"),
    pygame.Color("MistyRose"),
    pygame.Color("Moccasin"),
    pygame.Color("NavajoWhite"),
    pygame.Color("Navy"),
    pygame.Color("OldLace"),
    pygame.Color("Olive"),
    pygame.Color("OliveDrab"),
    pygame.Color("Orange"),
    pygame.Color("OrangeRed"),
    pygame.Color("Orchid"),
    pygame.Color("PaleGoldenrod"),
    pygame.Color("PaleGreen"),
    pygame.Color("PaleTurquoise"),
    pygame.Color("PaleVioletRed"),
    pygame.Color("PapayaWhip"),
    pygame.Color("PeachPuff"),
    pygame.Color("Peru"),
    pygame.Color("Pink"),
    pygame.Color("Plum"),
    pygame.Color("PowderBlue"),
    pygame.Color("Purple"),
    pygame.Color("Red"),
    pygame.Color("RosyBrown"),
    pygame.Color("RoyalBlue"),
    pygame.Color("SaddleBrown"),
    pygame.Color("Salmon"),
    pygame.Color("SandyBrown"),
    pygame.Color("SeaGreen"),
    pygame.Color("SeaShell"),
    pygame.Color("Sienna"),
    pygame.Color("Silver"),
    pygame.Color("SkyBlue"),
    pygame.Color("SlateBlue"),
    pygame.Color("SlateGray"),
    pygame.Color("Snow"),
    pygame.Color("SpringGreen"),
    pygame.Color("SteelBlue"),
    pygame.Color("Tan"),
    pygame.Color("Teal"),
    pygame.Color("Thistle"),
    pygame.Color("Tomato"),
    pygame.Color("Turquoise"),
    pygame.Color("Violet"),
    pygame.Color("Wheat"),
    pygame.Color("White"),
    pygame.Color("WhiteSmoke"),
    pygame.Color("Yellow"),
    pygame.Color("YellowGreen")
]


###################################################################################################
#---------------------------------------- Setup functions ----------------------------------------#
###################################################################################################

def set_grid_size(width: int, height: int):
    global grid_width, grid_height
    grid_width = width
    grid_height = height


def initialise_ghost_layer(width, height):
    global ghost_layer
    cell_width = (screen_h // (grid_height + 2)) * screen_scale
    
    ghost_layer = pygame.Surface(((width + 1) * cell_width, (height + 1) * cell_width))
    ghost_layer.set_alpha(80)


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
        outline_thickness: int,
        background_colour: pygame.Color,
        focused_tet: Tetromino,
        draw_ghost_piece: bool = True
    ):
    global cell_width, board_offset, purple_monkey_dishwasher
    # Calculates how wide to make each cell
    cell_width = (screen_h // (grid_height + 2)) * screen_scale

    # Calculates the board offset to have the grid centred
    board_offset = (screen_dimensions.current_w // 2) - cell_width * ((grid_width / 2) + 1)

    if not purple_monkey_dishwasher:
        purple_monkey_dishwasher = pygame.image.load(".\images\purple_monkey_dishwasher.jpg")
        purple_monkey_dishwasher = pygame.transform.scale(purple_monkey_dishwasher, (grid_width * cell_width, grid_height * cell_width))
    
    #screen.blit(purple_monkey_dishwasher, (cell_width + board_offset, cell_width))

    # Draws the ghost piece
    if ghost_piece and draw_ghost_piece:
        ghost_piece_colour = set_draw_colour(ghost_piece.tet_type)

        ghost_layer.fill(background_colour)
        for cell in ghost_piece.cells:
            x, y = cell[0], cell[1]
            cell_rect = pygame.Rect(
                cell_width * (x + 1), 
                cell_width * (y + 1), 
                cell_width, 
                cell_width
            )
            
            pygame.draw.rect(ghost_layer, ghost_piece_colour, cell_rect)
        # Positions the ghost_piece_layers
        ghost_layer_pos = (
            board_offset, 
            0, 
        )

        screen.blit(ghost_layer, ghost_layer_pos)
    # Draws the Tetrominos
    for tetromino in tetrominos:
        cells = tetromino.cells
        #tetromino_colour = set_draw_colour(tetromino.tet_type)

        for cell in cells:
            tetromino_colour = set_cell_colour(round(sqrt(cell[0] ** 2 + cell[1] ** 2)))
            x, y = cell[0], cell[1]
            cell_rect = pygame.Rect(
                cell_width * (x + 1) + board_offset, 
                cell_width * (y + 1), 
                cell_width, 
                cell_width
            )

            image_rect = pygame.Rect(
                cell_width * (x), 
                cell_width * (y), 
                cell_width, 
                cell_width
            )
            
            pygame.draw.rect(screen, tetromino_colour, cell_rect)
            #screen.blit(purple_monkey_dishwasher, cell_rect)
            screen.blit(purple_monkey_dishwasher.subsurface(image_rect), cell_rect)
    
    
    
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
    outline_thickness: int = 2 * screen_scale
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