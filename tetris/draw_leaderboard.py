import pygame
from input_box import InputBox, ACTIVE_COLOUR
from json_parser import write_to_scoreboard, get_file_data
from time import sleep

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
    50 * 3 * screen_scale, # Should be roughly 3x the font size
    prompt="Enter a name: ", 
    font_size=50 * screen_scale,
    can_defocus=False,
    max_input_length=5
)

name_input_box.character_set = leaderboard_names_characterset
name_input_box.colour = ACTIVE_COLOUR

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
leaderboard_left: int = 30 * screen_scale
leaderboard_top: int = 100 * screen_scale
# -----------------------------------------

displayed_scores = [
    {
            "Name": "TEST2",
            "Score": 16620,
            "Lines cleared": 83
    },
    {
        "Name": "NOTME",
        "Score": 15480,
        "Lines cleared": 97
    },
    {
        "Name": "CORNE",
        "Score": 2140,
        "Lines cleared": 46
    },
    {
        "Name": "A",
        "Score": 1380,
        "Lines cleared": 8
    },
    {
        "Name": "SAMMM",
        "Score": 220,
        "Lines cleared": 5
    },
]



###################################################################################################
#--------------------------------------- Utility functions ---------------------------------------#
###################################################################################################


###################################################################################################
#---------------------------------------- Setup functions ----------------------------------------#
###################################################################################################

def receive_new_top_scores(new_top_scores: list[dict]):
    global displayed_scores
    print(new_top_scores)
    displayed_scores = new_top_scores
    

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
        global leaderboard_canvas, names_font, names_font_size
        if not names_font:
            names_font = pygame.font.SysFont('Lexus', names_font_size)
        
        for index, score in enumerate(scores):
            score_surface = names_font.render(f"{str(score):05}", True, "white")
            score_rect = score_surface.get_rect()
            score_rect.left = leaderboard_left + 60 * screen_scale
            score_rect.top = leaderboard_top + int(score_rect.height * (index * 1.5))
            screen.blit(score_surface, score_rect)


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