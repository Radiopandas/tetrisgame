import pygame

pygame.init()

###################################################################################################
#------------------------------------------ Global vars ------------------------------------------#
###################################################################################################
screen_dimensions = pygame.display.Info()
screen_w = 640
screen_h = 360

screen_scale: int = int(screen_dimensions.current_h / screen_h)

title_font = None
title_font_size: int = 0

instructions_font = None
instructions_font_size: int = 0

###################################################################################################
#---------------------------------------- Setup functions ----------------------------------------#
###################################################################################################

def initialise_title_font(size: int):
    global title_font, title_font_size
    title_font_size = size * screen_scale
    title_font = pygame.font.SysFont('Lexus', title_font_size)

def initialise_instructions_font(size: int):
    global instructions_font, instructions_font_size
    instructions_font_size = size * screen_scale
    instructions_font = pygame.font.SysFont('Lexus', instructions_font_size)

###################################################################################################
#---------------------------------------- Main functions -----------------------------------------#
###################################################################################################

def draw_start_menu(screen: pygame.Surface):
    global screen_w, \
        title_font, title_font_size, \
        instructions_font, instructions_font_size

    # Calculates the offset required to be centred.
    screen_midpoint = screen_dimensions.current_w // 2

    # Calculates the positions for the title and instructions
    title_pos = pygame.math.Vector2(
        screen_midpoint,
        33 * screen_scale
    )

    instructions_pos = pygame.math.Vector2(
        screen_midpoint,
        120 * screen_scale
    )

    # Draws the title and instructions
    title_display = title_font.render("SIRTET", False, "white")
    instructions_display = instructions_font.render("Press \'Enter\' to begin", False, "white", "black")
    
    # Positions them both
    title_rect = title_display.get_rect(midtop=title_pos)
    instructions_rect = instructions_display.get_rect(midtop=instructions_pos)
    # Adds them to the screen
    screen.blit(title_display, title_rect)
    screen.blit(instructions_display, instructions_rect)

    # Draws a bounding box around the title
    title_rect_thickness: int = 2 * screen_scale
    title_rect_border: int = 3 * screen_scale
    #title_rect = pygame.Rect(
    #    title_pos.x - title_rect_border, 
    #    title_pos.y - title_rect_border,
    #    84 * screen_scale + 2 * title_rect_border, # 252 is the approximate width of the title(currently)
    #    20 * screen_scale + 2 * title_rect_border # 60 is a magical number
    #)
    title_rect.left -= title_rect_border
    title_rect.top -= title_rect_border
    title_rect.width += 2 * title_rect_border
    title_rect.height += 1 * title_rect_border
    pygame.draw.rect(screen, "azure4", title_rect, title_rect_thickness)


#910 431
#1827


"""
Needed Functions
draw_start_menu
"""