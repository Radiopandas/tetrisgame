import pygame

#Testing
from time import sleep

pygame.init()

###################################################################################################
#------------------------------------------ Global vars ------------------------------------------#
###################################################################################################
display_info = pygame.display.Info()
screen_w = 640
screen_h = 360
screen_scale = display_info.current_h / 360

button_x_coords: dict = {
    "settings_button": [40 * screen_scale, 40 * screen_scale + 40 * screen_scale]
}

button_y_coords: dict = {
    "settings_button": [screen_h * screen_scale - (80 * screen_scale), screen_h * screen_scale - (40 * screen_scale)]
}

settings_menu_open: bool = False

###################################################################################################
#---------------------------------------- Setup functions ----------------------------------------#
###################################################################################################



###################################################################################################
#---------------------------------------- Main functions -----------------------------------------#
###################################################################################################

def draw_button(screen: pygame.Surface, button: str):
    """Draws a singular button onto the screen."""
    x_coords = button_x_coords[button]
    y_coords = button_y_coords[button]

    x_dif: int = x_coords[1] - x_coords[0]
    y_dif: int = y_coords[1] - y_coords[0]

    settings_button_rect = pygame.Rect(
        x_coords[0],
        y_coords[0],
        x_dif,
        y_dif
    )
    pygame.draw.rect(screen, "green", settings_button_rect)


def draw_controls_buttons(screen: pygame.Surface, controls):
    """Draws a button and text for every control"""
    pass


def check_pressed_buttons(mouse_coords):
    mouse_x = mouse_coords[0]
    mouse_y = mouse_coords[1]

    # Checks every button to find ones that have the right x range
    for x_button in button_x_coords.keys():
        left, right = button_x_coords[x_button]
        if left <= mouse_x <= right:
            for y_button in button_y_coords.keys():
                top, bottom = button_y_coords[y_button]
                if top <= mouse_y <= bottom:
                    print(f"Button pressed: {x_button}")
                    sleep(3)