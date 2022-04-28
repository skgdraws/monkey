import pygame
from gamover import hall_of_fame

class MainMenu:

    def __init__(self, screen, create_overworld):
        
        # Setting up Screen
        self.screen = screen
        self.create_overworld = create_overworld

        # Time
        self.startTime = pygame.time.get_ticks()
        self.allowInput = False
        self.timerLength = 1500

        #inputs
        self.down_key = False
        self.up_key = False
        self.enter = False

        # Font and text stuff
        self.font = pygame.font.Font("font/kongtext.ttf", 15)

        # Logo thing
        self.logo_image = pygame.image.load("images/logo.png").convert_alpha()
        self.logo_sprite = Logo(self.logo_image, (224, 80))
        self.logo = pygame.sprite.GroupSingle()
        self.logo.add(self.logo_sprite)

        #Option Selection
        self.state = 'skg'

        self.skg_pos = (140, 300)
        self.skg_text = self.font.render("Play as SKG", False, "#FFFFFF")
        self.skg_text_rect = self.skg_text.get_rect(topleft = self.skg_pos)
        
        self.m00n_pos = (140, 330)
        self.m00n_text = self.font.render("Play as M00N", False, "#FFFFFF")
        self.m00n_text_rect = self.m00n_text.get_rect(topleft = self.m00n_pos)
        
        self.score_pos = (140, 360)
        self.score_text = self.font.render("High Scores", False, "#FFFFFF")
        self.score_text_rect = self.score_text.get_rect(topleft = self.score_pos)

        # Credits
        self.credits = self.font.render("Hecho por Franco Sagot - 2022", False, "#FFFFFF")
        self.credits_rect = self.credits.get_rect(center = (224, 500))

        # Cursor
        self.icon_image = pygame.image.load("images/ui/life-icon.png")
        self.offset = -50
        self.icon_rect = self.icon_image.get_rect(topleft = (self.skg_pos[0] + self.offset, self.skg_pos[1] - 7))

    def inputs(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.up_key = True

        elif keys[pygame.K_DOWN]:
            self.down_key = True
            
        elif keys[pygame.K_RETURN]:
            self.enter = True

    def reset_inputs(self):
        self.up_key = False
        self.down_key = False
        self.enter = False

    def check_input(self):
        if self.enter:
            if self.state == 'skg':
                self.create_overworld(0, 0, 'skg')

            elif self.state == 'm00n':
                self.create_overworld(0, 0, 'm00n')

            elif self.state == 'score':
                self.create_scores()

    def move_icon(self):
        
        if self.down_key and self.allowInput:
            if self.state == 'skg':
                self.allowInput = False
                self.icon_rect.topleft = (self.m00n_pos[0] + self.offset, self.m00n_pos[1])
                self.state = 'm00n'

            elif self.state == 'm00n':
                self.allowInput = False
                self.icon_rect.topleft = (self.score_pos[0] + self.offset, self.score_pos[1])
                self.state = 'scores'

            elif self.state == 'scores':
                self.allowInput = False
                self.icon_rect.topleft = (self.skg_pos[0] + self.offset, self.skg_pos[1])
                self.state = 'skg'
            
        elif self.up_key and self.allowInput:
            if self.state == 'skg':
                self.allowInput = False
                self.icon_rect.topleft = (self.score_pos[0] + self.offset, self.score_pos[1])
                self.state = 'scores'
            
            elif self.state == 'm00n':
                self.allowInput = False
                self.icon_rect.topleft = (self.skg_pos[0] + self.offset, self.skg_pos[1])
                self.state = 'skg'

            elif self.state == 'scores':
                self.allowInput = False
                self.icon_rect.topleft = (self.m00n_pos[0] + self.offset, self.m00n_pos[1])
                self.state = 'm00n'

    def input_timer(self):

        if not self.allowInput:
            currentTime = pygame.time.get_ticks()
            if currentTime - self.startTime >= self.timerLength:
                self.allowInput = True

    def run(self):
        
        self.input_timer()
        self.inputs()
        self.check_input()
        self.move_icon()
        self.logo.draw(self.screen)
        self.screen.blit(self.credits, self.credits_rect)
        self.screen.blit(self.skg_text, self.skg_text_rect)
        self.screen.blit(self.m00n_text, self.m00n_text_rect)
        self.screen.blit(self.score_text, self.score_text_rect)
        self.screen.blit(self.icon_image, self.icon_rect)
        self.reset_inputs()

class Logo(pygame.sprite.Sprite):

    def __init__(self, surface, pos):
        super().__init__()

        self.image = surface
        self.rect = self.image.get_rect(center = pos)
