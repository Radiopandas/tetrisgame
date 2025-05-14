import pygame
from input_box import InputBox
from json_parser import write_to_scoreboard, get_file_data

pygame.init()

###################################################################################################
#------------------------------------------ Global vars ------------------------------------------#
###################################################################################################

display_info = pygame.display.Info()
screen_w: int = 640
screen_h: int = 360
screen_scale: int = int(display_info.current_h / screen_h)

leaderboard_canvas = pygame.Surface((display_info.current_w, display_info.current_h))

draw_name_input: bool = False

leaderboard_names_characterset: list[str] = [
    'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 
    'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm', '1', '2', '3', '4', '5', '6', 
    '7', '8', '9', '0', '-', '!'
]

name_input_box = InputBox(
    screen_w * screen_scale // 2, 
    screen_h * screen_scale // 2, 
    100 * screen_scale, 
    prompt="Enter a name: ", 
    font_size=30 * screen_scale,
    can_defocus=False,
    max_input_length=5
)

name_input_box.character_set = leaderboard_names_characterset

displayed_scores: list = []
scores_to_display: int = 0

# Fonts and stuff
names_font = None
names_font_size = 20 * screen_scale
scores_font = None
scores_font_size = 20 * screen_scale
title_font = None
title_font_size = 30 * screen_scale

# -----------------------------------------
# Leaderboard display positioning stuff
# -----------------------------------------
leaderboard_left: int = 100 * screen_scale
leaderboard_top: int = 100 * screen_scale
# -----------------------------------------

###################################################################################################
#--------------------------------------- Utility functions ---------------------------------------#
###################################################################################################

def get_top_scores(scores_to_get: int = 3):
    """Finds and returns the top scores from scoreboard.json"""
    global scores_to_display
    if scores_to_display != scores_to_get:
        scores_to_display = scores_to_get

    scoreboard_data = get_file_data('scoreboard.json', data_path="Scores")

    top_runs: list = []
    top_runs = scoreboard_data[0:scores_to_get]
    
    return top_runs


def update_top_scores():
    global scores_to_display, displayed_scores
    displayed_scores = get_top_scores(scores_to_display)

print(*get_top_scores(3), sep="\n")


###################################################################################################
#---------------------------------------- Setup functions ----------------------------------------#
###################################################################################################

def initialise_scoreboard():
    """Reads the top scores from scoreboard.json and stores them for later use."""
    global displayed_scores

    displayed_scores = get_top_scores(3)
    pass

###################################################################################################
#---------------------------------------- Main functions -----------------------------------------#
###################################################################################################
def handle_entered_score(name: str, info: dict):
    print(f"{name} achieved: {info}")
    # Checks that 'info' contains the correct information
    if info["Score"] and info["Lines cleared"]:
        write_to_scoreboard(name, info)


def draw_input_box(screen: pygame.Surface):
    global name_input_box
    name_input_box.draw(screen)
    


def draw_names(screen: pygame.Surface, names: list[str]):
    global leaderboard_canvas, names_font, names_font_size
    if not names_font:
        names_font = pygame.font.SysFont('Lexus', names_font_size)
    
    for index, name in enumerate(names):
        name_surface = names_font.render(name, True, "white")
        name_rect = name_surface.get_rect()
        name_rect.left = leaderboard_left
        name_rect.top = leaderboard_top + int(name_rect.height * (index * 1.5))
        screen.blit(name_surface, name_rect)


def draw_scores(screen: pygame.Surface, scores: list[int]):
    pass


def draw_scoreboard(screen: pygame.Surface):
    #screen.fill("azure4")
    """Draws the scoreboard onto the screen."""
    global displayed_scores
    # Seperates out the relevant scoreboard data.
    names: list[str] = []
    scores: list[int] = []
    for score in displayed_scores:
        names.append(score["Name"])
        scores.append(score["Score"])
    
    # Draws the names and the scores.
    draw_names(screen, names)
    draw_scores(screen, scores)
    
    # Calculates the size of the bounding rect.

    # Draws the bounding rect.
    
    # Draws the title

    # Blits the canvas onto the main screen
    #screen.blit(leaderboard_canvas, (0, 0, 0, 0))