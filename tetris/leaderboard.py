import pygame
from input_box import InputBox, ACTIVE_COLOUR
from json_parser import write_to_scoreboard, get_file_data
import pygame.docs

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

# Fonts and stuff
input_box_font_size: int = 40 * screen_scale
names_font = None
names_font_size = 20 * screen_scale
scores_font = None
scores_font_size = 20 * screen_scale
score_title_font = None
score_title_font_size = 12 * screen_scale
leaderboard_title_font = None
leaderboard_title_font_size = 25 * screen_scale


leaderboard_names_characterset: list[str] = [
    'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 
    'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm', '1', '2', '3', '4', '5', '6', 
    '7', '8', '9', '0', '-', '!'
]

name_input_box = InputBox(
    screen_w * screen_scale // 2, 
    screen_h * screen_scale // 2, 
    input_box_font_size * 2, # Should be roughly 2x the font size
    prompt="", 
    font_size=input_box_font_size,
    can_defocus=False,
    max_input_length=3
)

name_input_box.centred_text = True

name_input_box.character_set = leaderboard_names_characterset
name_input_box.colour = ACTIVE_COLOUR

displayed_scores: list = []
scores_to_display: int = 0





# -----------------------------------------
# Leaderboard display positioning stuff
# -----------------------------------------
leaderboard_left: int = 30 * screen_scale
leaderboard_top: int = 45 * screen_scale
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

current_score: int = 0

###################################################################################################
#--------------------------------------- Utility functions ---------------------------------------#
###################################################################################################

def set_score(score: int) -> None:
    global current_score
    current_score = score

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
    # before sending the score to the server.
    if info["Score"] and info["Lines cleared"]:
        write_to_scoreboard(name, info)


def draw_input_box(screen: pygame.Surface):
    global name_input_box, score_title_font, score_title_font_size

    # Renders the score.
    if not score_title_font:
        score_title_font = pygame.font.SysFont('Lexus', score_title_font_size)

    score_surface = score_title_font.render(f"Your score: {current_score:05}", True, "white")
    score_rect = score_surface.get_rect()
    score_rect.center = (
        screen_w * screen_scale // 2,
        (screen_h * screen_scale // 2) + (input_box_font_size // 2)
    )

    # Creates the background rect for the score
    score_background_rect = score_surface.get_rect()
    score_background_rect.center = (
        screen_w * screen_scale // 2 - 3 * screen_scale,
        (screen_h * screen_scale // 2) + (input_box_font_size // 2) - 3 * screen_scale
    )
    score_background_rect.width += 6 * screen_scale
    score_background_rect.height += 6 * screen_scale

    # Actually draws the score and background.
    pygame.draw.rect(screen, "black", score_background_rect)
    screen.blit(score_surface, score_rect)

    

    # Draws the prompt.


    # Draws the actual box that the user enters their name into.
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
        score_surface = names_font.render(f"{score:05}", True, "white")
        score_rect = score_surface.get_rect()
        score_rect.left = leaderboard_left + 60 * screen_scale
        score_rect.top = leaderboard_top + int(score_rect.height * (index * 1.5))
        screen.blit(score_surface, score_rect)


def draw_scoreboard(screen: pygame.Surface):
    """Draws the scoreboard onto the screen."""
    global displayed_scores, leaderboard_title_font, leaderboard_title_font_size
    # Seperates out the relevant scoreboard data.
    names: list[str] = []
    scores: list[int] = []
    for score in displayed_scores:
        names.append(score["Name"])
        scores.append(score["Score"])
    
    
    # Calculates the size of the bounding rect.
    outline_rect = pygame.Rect(
        leaderboard_left - 6 * screen_scale,
        leaderboard_top - 6 * screen_scale,
        113 * screen_scale,
        200 * screen_scale
    )

    pygame.draw.rect(screen, "white", outline_rect, width=2 * screen_scale)

    # Draws the names and the scores.
    draw_names(screen, names)
    draw_scores(screen, scores)

    # Draws the bounding rect.
    
    # Draws the title
    if not leaderboard_title_font:
        leaderboard_title_font = pygame.font.SysFont('Lexus', leaderboard_title_font_size)
    
    # Renders the text.
    title_surface = leaderboard_title_font.render("Leaderboard", True, "white")

    # Gets and positions the leaderboard rect.
    title_rect = title_surface.get_rect()
    title_rect.centerx = leaderboard_left - 6 * screen_scale + 113 * screen_scale // 2
    title_rect.centery = leaderboard_top//2

    screen.blit(title_surface, title_rect)
    

    # Blits the canvas onto the main screen
    #screen.blit(leaderboard_canvas, (0, 0, 0, 0))