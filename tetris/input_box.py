import pygame

pygame.init()

INACTIVE_COLOUR = pygame.Color("lightskyblue3")
ACTIVE_COLOUR = pygame.Color("dodgerblue2")

class InputBox:
    rect: pygame.Rect # Outline for the text area.
    extra_width: int # How much wider than the text self.rect should be.
    colour: pygame.Color # Current outline/background colour.
    font: pygame.font.SysFont # Current font to use for rendering text.
    text_surface: pygame.Surface # Surface with rendered text.
    prompt: str # Question that is displayed in the input box.
    
    active: bool # Whether the box is currently selected and should take inputs.
    text: str = "" # User entered text.
    previous_text: str = "" # Previous string of text from before K_RETURN was pressed.

    visible: bool = False # Don't think this is ever used
    max_input_length: int # How long an input can be. If max_input_length is 0, there is no limit.


    # Prevents the box being defocused and, thus, 
    # other functions receiving inputs.
    can_defocus: bool = True

    centred_text: bool = False

    character_set: list[str] = []

    def __init__(self, 
                middle_x, 
                middle_y, 
                width, 
                prompt="", 
                font_size=32, 
                font="Lexus", 
                can_defocus=True,
                max_input_length=0
        ):
        self.colour = INACTIVE_COLOUR
        self.prompt = prompt
        self.font = pygame.font.SysFont(font, font_size)
        self.text_surface = self.font.render(self.prompt + self.text, True, "white", "black")
        self.extra_width = width
        self.rect = self.text_surface.get_rect()
        
        self.rect.width = self.rect.width + self.extra_width
        self.rect.center = (middle_x, middle_y)
        
        self.active = False
        self.can_defocus = can_defocus
        self.max_input_length = max_input_length


    def handle_event(self, event):
        return_pressed = False
        # Checks if the box was clicked.
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active if self.can_defocus else True
            else:
                self.active = False if self.can_defocus else True
            
            self.colour = ACTIVE_COLOUR if self.active else INACTIVE_COLOUR
        
        # Checks for typing(keyboard inputs).
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Marks that the text in the box should be returned.
                return_pressed  = True
                # 'Resets' the input box
                self.previous_text = self.text
                self.text = ""
                self.active = False
                self.colour = INACTIVE_COLOUR
            
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            
            else:
                if self.max_input_length > 0:
                    if len(self.text) < self.max_input_length:
                        if self.character_set:
                            if event.unicode.lower() in self.character_set:
                                self.text += event.unicode.upper()
                        else:
                            self.text += event.unicode.upper()
                else:
                    if self.character_set:
                        if event.unicode.lower() in self.character_set:
                            self.text += event.unicode.upper()
                    else:
                        self.text += event.unicode.upper()
            
            # Updates the display
            self.text_surface = self.font.render(self.prompt + self.text, True, "white", "black")
        
        # If necessary, returns the text from the box.
        if return_pressed:

            # Returns the entered text
            return self.previous_text

    
    def draw(self, screen: pygame.Surface):
        # Draws the text background onto the screen.
        pygame.draw.rect(screen, "black", self.rect)
        # Positions the text if necessary:
        text_rect = self.text_surface.get_rect()
        if self.centred_text:
            text_rect.center = self.rect.center

        # Blits the text onto the screen.
        screen.blit(self.text_surface, text_rect)
        # Blits the outline rectangle onto the screen.
        pygame.draw.rect(screen, self.colour, self.rect, 2)