import pygame
import input_handling

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
    "settings_button": [40 * screen_scale, 40 * screen_scale + 40 * screen_scale],
    "move_left_btn": [60 * screen_scale, 120 * screen_scale]
}

button_y_coords: dict = {
    "settings_button": [screen_h * screen_scale - (80 * screen_scale), screen_h * screen_scale - (40 * screen_scale)],
    "move_left_btn": [screen_h * screen_scale - (140 * screen_scale), screen_h * screen_scale - (80 * screen_scale)]
}

settings_menu_open: bool = False

controls_buttons: list[str] = ["move_left_btn", "move_right_btn"]

###################################################################################################
#---------------------------------------- Setup functions ----------------------------------------#
###################################################################################################

class Button:
    # x_coords: [left, right]
    x_coords: list[int] = []
    # y_coords: [top, bottom]
    y_coords: list[int] = []

    default_colour: pygame.Color = pygame.Color(0, 0, 0)
    pressed_colour: pygame.Color = pygame.Color(100, 100, 100)

    button_active: bool = False

    def draw_self(self, screen: pygame.Surface) -> None:
        x_dif = self.x_coords[1] - self.x_coords[0]
        y_dif = self.y_coords[1] - self.y_coords[0]

        button_rect = pygame.Rect(
            self.x_coords[0],
            self.y_coords[0],
            x_dif,
            y_dif
        )
        pygame.draw.rect(screen, self.default_colour, button_rect)


    def check_is_pressed(self, mouse_pos: tuple[int, int]) -> bool:
        x, y = mouse_pos
        left, right = self.x_coords
        top, bottom = self.y_coords
        if left <= x <= right and top <= y <= bottom:
            return True
        return False


###################################################################################################
#--------------------------------------- Utility Functions ---------------------------------------#
###################################################################################################

def get_button_effect(button_name: str):
    global controls_buttons
    if button_name in controls_buttons:
        print(f"button pressed: {button_name}")

        # Gets the first pressed input and maps it to the relevant action
        event_captured: bool = False
        while not event_captured:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key != pygame.K_ESCAPE:
                        input_handling.update_input_map(event.key, button_name[0:-4])
                        event_captured = True
                        break

    else:
        print("random button pressed")
        sleep(3)

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
    pygame.draw.rect(screen, "green" if button == "settings_button" else "blue", settings_button_rect)


def draw_controls_buttons(screen: pygame.Surface, controls):
    """Draws a button and text for every control"""
    global controls_buttons

    for button in controls_buttons:
        pass
    pass

def check_pressed_buttons(mouse_coords):
    mouse_x = mouse_coords[0]
    mouse_y = mouse_coords[1]

    # Checks every button to find ones that have the right x range
    for x_button in button_x_coords.keys():
        left, right = button_x_coords[x_button]
        if left <= mouse_x <= right:
            top, bottom = button_y_coords[x_button]
            if top <= mouse_y <= bottom:
                get_button_effect(x_button)