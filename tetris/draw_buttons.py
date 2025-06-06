import pygame


#Testing
from time import sleep

pygame.init()

display_info = pygame.display.Info()
screen_w = 640
screen_h = 360
screen_scale = int(display_info.current_h / screen_h)

###################################################################################################
#---------------------------------------- Setup functions ----------------------------------------#
###################################################################################################

button_font_size: int = 20 * screen_scale
button_font = pygame.font.SysFont('Lexus', button_font_size)

class Button:
    
    x_coords: list[int] = [] # x_coords: [left, right]
    y_coords: list[int] = [] # y_coords: [top, bottom]

    default_colour: pygame.Color = pygame.Color(0, 0, 0)
    pressed_colour: pygame.Color = pygame.Color(100, 100, 100)

    button_active: bool = False
    button_pressed: bool = False

    # Current groups options
    # "controls_btns"
    # "settings_btns"
    # "settings_util_btns"
    button_group: str = ""
    button_name: str = ""

    # Note: 'button_text' is displayed next to the buttons,
    # 'button_symbol' is displayed inside the buttons
    button_label: str = ""
    button_symbol: str = ""
    button_icon: pygame.Surface = None
    corner_radius: int = -1
    button_rect: pygame.Rect = None


    label_size: int = 0
    symbol_size: int = 0

    label_font = None
    symbol_font = None


    # Button methods.
    def __init__(
            self,
            x_coords: list[int],
            y_coords: list[int],
            default_colour: pygame.Color,
            pressed_colour: pygame.Color,
            is_active: bool,
            group: str,
            name: str,
            label: str = "A Button",
            symbol: str = "",
            label_size: int = 0,
            symbol_size: int = 0,
            corner_radius: int = -1
        ):
        self.x_coords = x_coords
        self.y_coords = y_coords
        self.default_colour = default_colour
        self.pressed_colour = pressed_colour
        self.button_active = is_active
        self.button_group = group
        self.button_name = name
        self.button_label = label
        self.button_symbol = symbol
        self.label_size = label_size
        self.symbol_size = symbol_size
        self.corner_radius = corner_radius
    

    def __str__(self):
        return f"Class \'Button\'. x_coords: {self.x_coords}, y_coords: {self.y_coords}, default_colour: {self.default_colour}, pressed_colour: {self.pressed_colour}"


    def draw_self(self, screen: pygame.Surface) -> None:
        # Draws the actual button.
        x_dif = self.x_coords[1] - self.x_coords[0]
        y_dif = self.y_coords[1] - self.y_coords[0]

        if self.label_size == 0:
            self.label_size = int(y_dif * 2 / 3)

        if self.symbol_size == 0:
            self.symbol_size = int(y_dif * 2 / 3)

        if not self.label_font:
            self.label_font = pygame.font.SysFont('Lexus', self.label_size)
        
        if not self.symbol_font:
            self.symbol_font = pygame.font.SysFont('Lexus', self.symbol_size)
        
        draw_colour = self.default_colour if not self.button_pressed else self.pressed_colour

        # Draws the button as a pygame.Rect object
        if not self.button_rect:

            self.button_rect = pygame.Rect(
                    self.x_coords[0],
                    self.y_coords[0],
                    x_dif,
                    y_dif
                )
        if not self.button_icon:
            pygame.draw.rect(screen, draw_colour, self.button_rect, border_radius=self.corner_radius)
            pygame.draw.rect(screen, "black", self.button_rect, width=1 * screen_scale, border_radius=self.corner_radius)


            # Draws the symbols inside the button
            if self.button_symbol:
                # Calculates the position to display the symbol
                symbol_pos = (self.x_coords[0] + x_dif * 0.5, self.y_coords[0] + y_dif * 0.5)
                # Renders the text
                symbol_surface = self.symbol_font.render(f"{self.button_symbol}", False, "white")
                # Positions it
                symbol_rect = symbol_surface.get_rect(center=symbol_pos)
                # Merges it onto the screen
                screen.blit(symbol_surface, symbol_rect)
        else:
            icon_width: int = self.button_icon.get_size()[0]
            new_icon_scale: float = x_dif / icon_width
            self.button_icon = pygame.transform.scale_by(self.button_icon, new_icon_scale)
            screen.blit(self.button_icon, self.button_rect)


        # Draws the text next to each button.
        # Calculates the position to display the text.
        label_pos = (self.x_coords[1] + x_dif * 0.25, self.y_coords[0] + y_dif * 0.5)
        # Renders the text
        label_surface = self.label_font.render(f"{self.button_label}", False, "white")
        # Positions it
        label_rect = label_surface.get_rect(midleft=label_pos )
        # Merges it onto the screen
        screen.blit(label_surface, label_rect)


    def check_is_pressed(self, mouse_pos: tuple[int, int]) -> bool:
        if self.button_active:
            x, y = mouse_pos
            left, right = self.x_coords
            top, bottom = self.y_coords
            if left <= x <= right and top <= y <= bottom:
                return True
        return False
    

    def set_is_pressed(self):
        self.button_pressed = not self.button_pressed
    

    def set_label_font_size(self, new_size: int = 0, new_ratio: float = 0):
        if new_size:
            self.label_size = new_size
        
        if new_ratio:
            y_dif = self.y_coords[1] - self.y_coords[0]
            self.label_size = int(y_dif * new_ratio)




###################################################################################################
#------------------------------------------ Global vars ------------------------------------------#
###################################################################################################

all_buttons: dict[str, Button] = {}

###################################################################################################
#--------------------------------------- Utility Functions ---------------------------------------#
###################################################################################################

def update_all_buttons(new_buttons: dict[str, Button]) -> None:
    global all_buttons
    for name, button in new_buttons.items():
        all_buttons[name] = button


###################################################################################################
#---------------------------------------- Main functions -----------------------------------------#
###################################################################################################

def draw_buttons(screen: pygame.Surface):
    global all_buttons
    
    for button in all_buttons.values():
        if button.button_active:
            button.draw_self(screen)


def check_pressed_buttons(mouse_coords: tuple[int, int]):
    global all_buttons

    for button in all_buttons.values():
        if button.button_active:
            if button.check_is_pressed(mouse_coords):
                print("Button pressed I guess")
                sleep(2)