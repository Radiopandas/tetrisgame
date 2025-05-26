import pygame
from draw_buttons import Button, update_all_buttons
from json_parser import get_file_data
from input_handling import update_input_map, event_is_valid_control, reset_controls, input_map, input_display

# TESTING ONLY
from time import sleep

###################################################################################################
#------------------------------------------ Global vars ------------------------------------------#
###################################################################################################
display_info = pygame.display.Info()
screen_w = 640
screen_h = 360
screen_scale = int(display_info.current_h / screen_h)

settings_canvas_1 = pygame.Surface((screen_w * 0.75 * screen_scale, screen_h * screen_scale))
settings_canvas_1.set_alpha(150)
settings_canvas_2 = pygame.Surface((screen_w * 0.25 * screen_scale, screen_h * screen_scale))


settings_menu_open: bool = False

# How much of a gap there is between the buttons as a multiple of their height.
control_button_spacing: float = 1.5 

# Used to convert certain events(arrow keys) to symbols
non_unicode_events: dict = get_file_data('settings.json', 'pygame_events_details', 'non_unicode_events')

controls_title_font = None
controls_title_font_size: int = 40 * screen_scale

controls_instructions_font = None
controls_instructions_font_size: int = 10 * screen_scale

buttons: dict[str, Button] = {}
control_button_width: int = 25
setting_btn_width: int = 30

# What order the buttons are in, where 0 is the bottom of the list.
button_order: dict = {
    "move_left_btn": 6,
    "move_right_btn": 5,
    "soft_drop_btn": 2,
    "hard_drop_btn": 1,
    "rotate_right_btn": 3,
    "rotate_left_btn": 4,
    "hold_piece_btn": 0
}

# Images
settings_icon: pygame.Surface = None

###################################################################################################
#---------------------------------------- Setup functions ----------------------------------------#
###################################################################################################

def get_settings_icon(icon_path='images\settings_icon.png'):
    global settings_icon
    # Gets the settings icon
    settings_icon = pygame.image.load(icon_path)

    

def get_button_keys(input_dict: dict, name_dict: dict, button_action: str):
    """Returns the key that 'action' is mapped to in 'input_dict'"""
    for action, key in input_dict.items():
        if action == button_action:
            return name_dict[action]


def initialise_settings_buttons():
    """Initialises all the buttons related to the settings menu and
    adds them to the list of all_buttons in draw_buttons.py"""
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
    settings_btn.button_icon = settings_icon

    move_left_btn = Button(
        [setting_btn_width * screen_scale * 0.75, (setting_btn_width * 0.75 + control_button_width) * screen_scale],
        [
            (screen_h - (3 + button_order["move_left_btn"] * control_button_spacing) * control_button_width) * screen_scale,
            screen_h * screen_scale - (2 + button_order["move_left_btn"] * control_button_spacing) * control_button_width * screen_scale
        ],
        pygame.Color(100, 100, 0),
        pygame.Color(200, 0, 200),
        False,
        "controls_btns",
        "move_left_btn",
        "Move piece left",
        get_button_keys(input_map, input_display, "move_left"),
    )

    move_right_btn = Button(
        [setting_btn_width * screen_scale * 0.75, (setting_btn_width * 0.75 + control_button_width) * screen_scale],
        [
            (screen_h - (3 + button_order["move_right_btn"] * control_button_spacing) * control_button_width) * screen_scale,
            screen_h * screen_scale - (2 + button_order["move_right_btn"] * control_button_spacing) * control_button_width * screen_scale
        ],
        pygame.Color(100, 100, 0),
        pygame.Color(200, 0, 200),
        False,
        "controls_btns",
        "move_right_btn",
        "Move piece right",
        get_button_keys(input_map, input_display, "move_right"),
    )

    soft_drop_btn = Button(
        [setting_btn_width * screen_scale * 0.75, (setting_btn_width * 0.75 + control_button_width) * screen_scale],
        [
            (screen_h - (3 + button_order["soft_drop_btn"] * control_button_spacing) * control_button_width) * screen_scale,
            screen_h * screen_scale - (2 + button_order["soft_drop_btn"] * control_button_spacing) * control_button_width * screen_scale
        ],
        pygame.Color(100, 100, 0),
        pygame.Color(200, 0, 200),
        False,
        "controls_btns",
        "soft_drop_btn",
        "Soft drop",
        get_button_keys(input_map, input_display, "soft_drop"),
    )

    hard_drop_btn = Button(
        [setting_btn_width * screen_scale * 0.75, (setting_btn_width * 0.75 + control_button_width) * screen_scale],
        [
            (screen_h - (3 + button_order["hard_drop_btn"] * control_button_spacing) * control_button_width) * screen_scale,
            screen_h * screen_scale - (2 + button_order["hard_drop_btn"] * control_button_spacing) * control_button_width * screen_scale
        ],
        pygame.Color(100, 100, 0),
        pygame.Color(200, 0, 200),
        False,
        "controls_btns",
        "hard_drop_btn",
        "Hard drop",
        get_button_keys(input_map, input_display, "hard_drop"),
    )

    rotate_right_btn = Button(
        [setting_btn_width * screen_scale * 0.75, (setting_btn_width * 0.75 + control_button_width) * screen_scale],
        [
            (screen_h - (3 + button_order["rotate_right_btn"] * control_button_spacing) * control_button_width) * screen_scale,
            screen_h * screen_scale - (2 + button_order["rotate_right_btn"] * control_button_spacing) * control_button_width * screen_scale
        ],
        pygame.Color(100, 100, 0),
        pygame.Color(200, 0, 200),
        False,
        "controls_btns",
        "rotate_right_btn",
        "Rotate right",
        get_button_keys(input_map, input_display, "rotate_right"),
    )

    rotate_left_btn = Button(
        [setting_btn_width * screen_scale * 0.75, (setting_btn_width * 0.75 + control_button_width) * screen_scale],
        [
            (screen_h - (3 + button_order["rotate_left_btn"] * control_button_spacing) * control_button_width) * screen_scale,
            screen_h * screen_scale - (2 + button_order["rotate_left_btn"] * control_button_spacing) * control_button_width * screen_scale
        ],
        pygame.Color(100, 100, 0),
        pygame.Color(200, 0, 200),
        False,
        "controls_btns",
        "rotate_left_btn",
        "Rotate left",
        get_button_keys(input_map, input_display, "rotate_left"),
    )

    hold_piece_btn = Button(
        [setting_btn_width * screen_scale * 0.75, (setting_btn_width * 0.75 + control_button_width) * screen_scale],
        [
            (screen_h - (3 + button_order["hold_piece_btn"] * control_button_spacing) * control_button_width) * screen_scale,
            screen_h * screen_scale - (2 + button_order["hold_piece_btn"] * control_button_spacing) * control_button_width * screen_scale
        ],
        pygame.Color(100, 100, 0),
        pygame.Color(200, 0, 200),
        False,
        "controls_btns",
        "hold_piece_btn",
        "Hold piece",
        get_button_keys(input_map, input_display, "hold_piece"),
    )

    reset_controls_btn = Button(
        [setting_btn_width * screen_scale * 0.75, (setting_btn_width * 0.75 + control_button_width) * screen_scale], 
        [
            (screen_h - 1.7 * control_button_width) * screen_scale,
            screen_h * screen_scale - 1.3 * control_button_width * screen_scale
        ],
        pygame.Color(100, 100, 0),
        pygame.Color(200, 0, 200),
        False,
        "settings_util_btns",
        "reset_controls_btn",
        "Reset to defaults", 
        corner_radius= 2 * screen_scale
    )

    reset_controls_btn.set_label_font_size(new_ratio=1.0)

    buttons["settings_btn"] = settings_btn
    buttons["reset_controls_btn"] = reset_controls_btn

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

def is_in_group(button: Button, group: str):
    if button.button_group == group:
        return True
    return False


def get_input():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            return event
    
    return None


def update_button_symbol(button: Button, event: pygame.event.Event):
    symbol: str = ''
    if event.unicode and event.unicode not in [" ", "\t"]:
        symbol = event.unicode
    else:
        if non_unicode_events[str(event.key)]:
            symbol = non_unicode_events[str(event.key)]
    
    if symbol:
        button.button_symbol = symbol.capitalize()


def call_button(button: Button, screen: pygame.Surface):
    global settings_menu_open
    match button.button_group:
        case "settings_btns":
            settings_menu_open = not settings_menu_open
            change_menu_is_opened()
        case "controls_btns":
            # Gets an input from the user.
            button.set_is_pressed()
            button.draw_self(screen)
            pygame.display.update()
            key_pressed = None
            while not key_pressed:
                key_pressed = get_input()
            
            # If it is an allowed input (Any normal keyboard symbols + arrow keys)
            # Binds it to the relevant action and displays it on the button.
            if event_is_valid_control(key_pressed):
                update_input_map(key_pressed.key, button.button_name[0:-4])
            
                update_button_symbol(button, key_pressed)
            
            button.set_is_pressed()
        case "settings_util_btns":
            controls_buttons: list[Button] = list(filter(lambda sequence: is_in_group(sequence, "controls_btns"), buttons.values()))
            reset_controls(controls_buttons)
        case _:
            print("Unknown button group detected")
            

def change_menu_is_opened():
    """Toggles each button between being visible and hidden."""
    global buttons

    for button in buttons.values():
        if button.button_group != "settings_btns":
            button.button_active = not button.button_active
        elif button.button_group == "settings_btns":
            button.set_is_pressed()

    update_all_buttons(buttons)


def check_pressed_buttons(mouse_coords: tuple[int, int], screen: pygame.Surface):
    global buttons

    for button in buttons.values():
        if button.button_active:
            if button.check_is_pressed(mouse_coords):
                print("Button pressed I guess")
                call_button(button, screen)



###################################################################################################
#---------------------------------------- Main functions -----------------------------------------#
###################################################################################################

def draw_buttons(screen: pygame.Surface):
    global settings_canvas_2, buttons

    for button in buttons.values():
        if button.button_group == "settings_btns":
            button.draw_self(screen)
        else:
            button.draw_self(settings_canvas_2)

def draw_settings_menu(screen: pygame.Surface):
    global controls_title_font, controls_title_font_size, \
        controls_instructions_font, controls_instructions_font_size
    

    # Creates the main background.
    settings_canvas_2.fill((20, 20, 20))

    # Renders the buttons onto the main canvas.
    draw_buttons(screen)
    
    screen.blit(settings_canvas_2, (0, 0, 0, 0))

    # Darkens the rest of the screen slightly.
    screen.blit(settings_canvas_1, (screen_w * 0.25 * screen_scale, 0, 0, 0))


    # Draws text to make it clear that the controls are being displayed
    if not controls_title_font:
        controls_title_font = pygame.font.SysFont('Lexus', controls_title_font_size)
    title_pos = (
        setting_btn_width * screen_scale * 0.75,
        setting_btn_width * screen_scale * 0.75
    )
    title_display = controls_title_font.render("Controls", False, "white")
    screen.blit(title_display, title_pos)


    # Draws instructions for changing controls
    if not controls_instructions_font:
        controls_instructions_font = pygame.font.SysFont('Lexus', controls_instructions_font_size)
    instructions_pos = (
        setting_btn_width * screen_scale * 0.85,
        setting_btn_width * screen_scale * 0.75 + 26 * screen_scale
    )
    instructions_display = controls_instructions_font.render("Click the boxes to change", False, "white")
    screen.blit(instructions_display, instructions_pos)