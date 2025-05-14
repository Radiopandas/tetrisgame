import pygame
from input_box import InputBox
from json_parser import write_to_scoreboard, get_file_data

###################################################################################################
#------------------------------------------ Global vars ------------------------------------------#
###################################################################################################

display_info = pygame.display.Info()
screen_w: int = 640
screen_h: int = 360
screen_scale: int = int(display_info.current_h / screen_h)

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

###################################################################################################
#--------------------------------------- Utility functions ---------------------------------------#
###################################################################################################

def get_top_scores(scores_to_get: int = 3):
    """Finds and returns the top scores from scoreboard.json"""
    scoreboard_data = get_file_data('scoreboard.json', data_path="Scores")

    top_runs: list = []
    top_runs = scoreboard_data[0:scores_to_get]
    
    return top_runs
            

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
    


def draw_highscore(screen: pygame.Surface):
    pass