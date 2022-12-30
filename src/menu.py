import pygame

class MainMenu:

    def __init__(self, screen, create_overworld):
        
        # Setting up Screen
        self.screen = screen
        self.create_overworld = create_overworld

        #Audio
        self.cursor_sound = pygame.mixer.Sound("assets/audio/sfx/move_cursor.wav")
        self.cursor_sound.set_volume(0.5)
        self.select_sound = pygame.mixer.Sound("assets/audio/sfx/select.wav")
        self.select_sound.set_volume(0.5)

        #inputs
        self.down_key = False
        self.up_key = False
        self.enter = False
        self.allowInput = True

        # Font and text stuff
        self.font = pygame.font.Font("assets/font/kongtext.ttf", 15)

        # Logo thing
        self.logo_image = pygame.image.load("assets/images/logo.png").convert_alpha()
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

        # Credits
        self.credits = self.font.render("Made by SKG Art", False, "#FFFFFF")
        self.credits_rect = self.credits.get_rect(center = (224, 480))
        self.music_credits = self.font.render("Music by Lil Tico", False, "#FFFFFF")
        self.music_credits_rect = self.music_credits.get_rect(center = (224, 500))

        # Cursor
        self.icon_image = pygame.image.load("assets/images/ui/life-icon-skg.png")
        self.offset = -50
        self.icon_rect = self.icon_image.get_rect(topleft = (self.skg_pos[0] + self.offset, self.skg_pos[1] - 10))

    def inputs(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.up_key = True

        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.down_key = True
            
        elif keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
            self.enter = True

    def reset_inputs(self):
        self.up_key = False
        self.down_key = False
        self.enter = False
        pygame.time.delay(100)

    def check_input(self):
        if self.enter:
            if self.state == 'skg':
                self.create_overworld(0, 0, 'skg')
                self.select_sound.play()

            elif self.state == 'm00n':
                self.create_overworld(0, 0, 'm00n')
                self.select_sound.play()

    def move_icon(self):
        
        if self.down_key and self.allowInput:
            if self.state == 'skg':
                self.icon_image = pygame.image.load("assets/images/ui/life-icon-m00n.png")
                self.icon_rect.topleft = (self.m00n_pos[0] + self.offset, self.m00n_pos[1] - 10)
                self.state = 'm00n'
                self.cursor_sound.play()
                self.reset_inputs()

            elif self.state == 'm00n':
                self.icon_image = pygame.image.load("assets/images/ui/life-icon-skg.png")
                self.icon_rect.topleft = (self.skg_pos[0] + self.offset, self.skg_pos[1] - 10)
                self.state = 'skg'
                self.cursor_sound.play()
                self.reset_inputs()

            
        elif self.up_key and self.allowInput:
            if self.state == 'skg':
                self.icon_image = pygame.image.load("assets/images/ui/life-icon-m00n.png")
                self.icon_rect.topleft = (self.m00n_pos[0] + self.offset, self.m00n_pos[1] - 10)
                self.state = 'm00n'
                self.cursor_sound.play()
                self.reset_inputs()

            
            elif self.state == 'm00n':
                self.icon_image = pygame.image.load("assets/images/ui/life-icon-skg.png")
                self.icon_rect.topleft = (self.skg_pos[0] + self.offset, self.skg_pos[1] - 10)
                self.state = 'skg'
                self.cursor_sound.play()
                self.reset_inputs()


    def run(self):
        
        self.inputs()
        self.check_input()
        self.move_icon()
        self.reset_inputs()
        self.logo.draw(self.screen)
        self.screen.blit(self.music_credits, self.music_credits_rect)
        self.screen.blit(self.credits, self.credits_rect)
        self.screen.blit(self.skg_text, self.skg_text_rect)
        self.screen.blit(self.m00n_text, self.m00n_text_rect)
        self.screen.blit(self.icon_image, self.icon_rect)

class Logo(pygame.sprite.Sprite):

    def __init__(self, surface, pos):
        super().__init__()

        self.image = surface
        self.rect = self.image.get_rect(center = pos)
