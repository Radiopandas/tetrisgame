import pygame
from draw_buttons import Button, update_all_buttons
from json_parser import get_file_data
from input_handling import update_input_map, event_is_valid_control

# TESTING ONLY
from time import sleep

###################################################################################################
#------------------------------------------ Global vars ------------------------------------------#
###################################################################################################
display_info = pygame.display.Info()
screen_w = 640
screen_h = 360
screen_scale = int(display_info.current_h / screen_h)

settings_menu_open: bool = False

buttons: dict[str, Button] = {}

# Testing only (for now)
control_button_width: int = 25
setting_btn_width: int = 30

# Used to convert certain events(arrow keys) to symbols
non_unicode_events: dict = get_file_data('settings.json', 'pygame_events_details', 'non_unicode_events')

controls_title_font = None
controls_title_font_size: int = 40 * screen_scale


###################################################################################################
#---------------------------------------- Setup functions ----------------------------------------#
###################################################################################################
def initialise_settings_buttons():
    """
    Replace later with a less shitty way of doing this.
    Could store the base values in settings.json then multiply them by screen_scale 
    in the actual script. Would require default_colour and pressed_colour to be changed from
    pygame.Color objects to tuples[int, int, int]
    """
    settings_btn = Button(
        [0, setting_btn_width * screen_scale],
        [screen_h * screen_scale - setting_btn_width * screen_scale, screen_h * screen_scale],
        pygame.Color(100, 100, 0),
        pygame.Color(200, 0, 200),
        True,
        "settings_btns",
        "settings_btn",
        "Settings"
    )

    move_left_btn = Button(
        [setting_btn_width * screen_scale * 0.75, (setting_btn_width * 0.75 + control_button_width) * screen_scale],
        [
            screen_h * screen_scale - 2 * control_button_width * screen_scale - control_button_width * screen_scale, 
            screen_h * screen_scale - 2 * control_button_width * screen_scale
        ],
        pygame.Color(100, 100, 0),
        pygame.Color(200, 0, 200),
        False,
        "controls_btns",
        "move_left_btn",
        "Move piece left",
        "A"
    )

    move_right_btn = Button(
        [setting_btn_width * screen_scale * 0.75, (setting_btn_width * 0.75 + control_button_width) * screen_scale],
        [
            screen_h * screen_scale - 3.5 * control_button_width * screen_scale - control_button_width * screen_scale, 
            screen_h * screen_scale - 3.5 * control_button_width * screen_scale
        ],
        pygame.Color(100, 100, 0),
        pygame.Color(200, 0, 200),
        False,
        "controls_btns",
        "move_right_btn",
        "Move piece right",
        "D"
    )

    soft_drop_btn = Button(
        [setting_btn_width * screen_scale * 0.75, (setting_btn_width * 0.75 + control_button_width) * screen_scale],
        [
            screen_h * screen_scale - 5 * control_button_width * screen_scale - control_button_width * screen_scale, 
            screen_h * screen_scale - 5 * control_button_width * screen_scale
        ],
        pygame.Color(100, 100, 0),
        pygame.Color(200, 0, 200),
        False,
        "controls_btns",
        "soft_drop_btn",
        "Soft drop",
        "S"
    )

    hard_drop_btn = Button(
        [setting_btn_width * screen_scale * 0.75, (setting_btn_width * 0.75 + control_button_width) * screen_scale],
        [
            screen_h * screen_scale - 6.5 * control_button_width * screen_scale - control_button_width * screen_scale, 
            screen_h * screen_scale - 6.5 * control_button_width * screen_scale
        ],
        pygame.Color(100, 100, 0),
        pygame.Color(200, 0, 200),
        False,
        "controls_btns",
        "hard_drop_btn",
        "Hard drop",
        "W"
    )

    rotate_right_btn = Button(
        [setting_btn_width * screen_scale * 0.75, (setting_btn_width * 0.75 + control_button_width) * screen_scale],
        [
            screen_h * screen_scale - 8 * control_button_width * screen_scale - control_button_width * screen_scale, 
            screen_h * screen_scale - 8 * control_button_width * screen_scale
        ],
        pygame.Color(100, 100, 0),
        pygame.Color(200, 0, 200),
        False,
        "controls_btns",
        "rotate_right_btn",
        "Rotate right",
        "E"
    )

    rotate_left_btn = Button(
        [setting_btn_width * screen_scale * 0.75, (setting_btn_width * 0.75 + control_button_width) * screen_scale],
        [
            screen_h * screen_scale - 9.5 * control_button_width * screen_scale - control_button_width * screen_scale, 
            screen_h * screen_scale - 9.5 * control_button_width * screen_scale
        ],
        pygame.Color(100, 100, 0),
        pygame.Color(200, 0, 200),
        False,
        "controls_btns",
        "rotate_left_btn",
        "Rotate left",
        "Q"
    )

    hold_piece_btn = Button(
        [setting_btn_width * screen_scale * 0.75, (setting_btn_width * 0.75 + control_button_width) * screen_scale],
        [
            screen_h * screen_scale - 11 * control_button_width * screen_scale - control_button_width * screen_scale, 
            screen_h * screen_scale - 11 * control_button_width * screen_scale
        ],
        pygame.Color(100, 100, 0),
        pygame.Color(200, 0, 200),
        False,
        "controls_btns",
        "hold_piece_btn",
        "Hold piece",
        "H" 
    )

    buttons["settings_btn"] = settings_btn

    buttons["move_left_btn"] = move_left_btn
    buttons["move_right_btn"] = move_right_btn
    buttons["soft_drop_btn"] = soft_drop_btn
    buttons["hard_drop_btn"] = hard_drop_btn
    buttons["rotate_right_btn"] = rotate_right_btn
    buttons["rotate_left_btn"] = rotate_left_btn
    buttons["hold_piece_btn"] = hold_piece_btn

    update_all_buttons(buttons)

###################################################################################################
#--------------------------------------- Utility Functions ---------------------------------------#
###################################################################################################

def get_input():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            return event
    
    return None


def update_button_symbol(button: Button, event: pygame.event.Event):
    symbol: str = ''
    if event.unicode:
        symbol = event.unicode
    else:
        if non_unicode_events[str(event.key)]:
            symbol = non_unicode_events[str(event.key)]
    
    button.button_symbol = symbol.capitalize()


def call_button(button: Button):
    global settings_menu_open
    match button.button_group:
        case "settings_btns":
            settings_menu_open = not settings_menu_open
            change_menu_is_opened()
        case "controls_btns":
            # Gets an input from the user.
            key_pressed = None
            while not key_pressed:
                key_pressed = get_input()
            
            # If it is an allowed input (Any normal keyboard symbols + arrow keys)
            # Binds it to the relevant action and displays it on the button.
            if event_is_valid_control(key_pressed):
                update_input_map(key_pressed.key, button.button_name[0:-4])
            
            update_button_symbol(button, key_pressed)
            

def change_menu_is_opened():
    """Toggles each button between being visible and hidden."""
    global buttons

    for button in buttons.values():
        if button.button_group != "settings_btns":
            button.button_active = not button.button_active

    update_all_buttons(buttons)


def check_pressed_buttons(mouse_coords: tuple[int, int]):
    global buttons

    for button in buttons.values():
        if button.button_active:
            if button.check_is_pressed(mouse_coords):
                print("Button pressed I guess")
                call_button(button)



###################################################################################################
#---------------------------------------- Main functions -----------------------------------------#
###################################################################################################

def draw_settings_menu(screen: pygame.Surface):
    global controls_title_font, controls_title_font_size

    # Creates the background
    screen.fill("black")

    # Draws text to make it clear that the controls are being displayed
    if not controls_title_font:
        controls_title_font = pygame.font.SysFont('Lexus', controls_title_font_size)
    title_pos = (
        setting_btn_width * screen_scale * 0.75,
        setting_btn_width * screen_scale * 0.75
    )
    title_display = controls_title_font.render("Controls", False, "white")
    screen.blit(title_display, title_pos)