import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__()
        #imports the sprites
        player_walk1 = pygame.image.load("images/skg/run/skg-run1.png").convert_alpha()
        player_walk2 = pygame.image.load("images/skg/run/skg-run2.png").convert_alpha()
        player_walk3 = pygame.image.load("images/skg/run/skg-run3.png").convert_alpha()
        self.player_walk = [player_walk1, player_walk2, player_walk3]
        self.player_index = 0
        self.player_jump = pygame.image.load("images/skg/jump/skg-jump.png").convert_alpha()

        #Sets up the player itself
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 496))
        self.gravity = 0
        self.speed = 0

    def player_input(self):
        self.keys = pygame.key.get_pressed()

        #Checks input for jumping
        if self.keys[pygame.K_SPACE] and self.rect.bottom == 496 and self.keys[pygame.K_LEFT]:
            self.gravity = -4.5
            self.speed = -1
        
        elif self.keys[pygame.K_SPACE] and self.rect.bottom == 496 and self.keys[pygame.K_RIGHT]:
            self.gravity = -4.5
            self.speed = 1
        
        elif self.keys[pygame.K_SPACE] and self.rect.bottom == 496:
            self.gravity = -4.5

        #Checks imput for movement
        if self.keys[pygame.K_RIGHT] or self.keys[pygame.K_d]:
            self.speed = 3
        
        elif self.keys[pygame.K_LEFT] or self.keys[pygame.K_a]:
            self.speed = -3

        elif self.rect.bottom == 496:
            self.speed = 0

    def apply_movement(self):
        self.gravity += 0.3
        self.rect.bottom += self.gravity
        self.rect.x += self.speed
        
        if self.rect.bottom >= 496:
            self.rect.bottom = 496

    def animation_state(self):
        if self.rect.bottom < 496:
            self.image = self.player_jump
        
        elif self.rect.bottom == 496 and (self.keys[pygame.K_a] or self.keys[pygame.K_d] or self.keys[pygame.K_RIGHT] or self.keys[pygame.K_LEFT]):
            self.player_index += 0.151666666666
            
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
        
        else:
            self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_movement()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):     
        super().__init__()   
        if type == "blue barrel":
            blue_barrel_frame1 = pygame.image.load("images/barrel/bluebarrel1.png").convert_alpha()
            blue_barrel_frame2 = pygame.image.load("images/barrel/bluebarrel2.png").convert_alpha()
            blue_barrel_frame3 = pygame.image.load("images/barrel/bluebarrel3.png").convert_alpha()
            blue_barrel_frame4 = pygame.image.load("images/barrel/bluebarrel4.png").convert_alpha()
            self.frames = [blue_barrel_frame1, blue_barrel_frame2, blue_barrel_frame3, blue_barrel_frame4]
            ypos = 456

        else:
            #Obstacles
            barrel_frame1 = pygame.image.load("images/barrel/barrel1.png").convert_alpha()
            barrel_frame2 = pygame.image.load("images/barrel/barrel2.png").convert_alpha()
            barrel_frame3 = pygame.image.load("images/barrel/barrel3.png").convert_alpha()
            barrel_frame4 = pygame.image.load("images/barrel/barrel4.png").convert_alpha()
            self.frames = [barrel_frame1, barrel_frame2, barrel_frame3, barrel_frame4]
            ypos = 496

        self.animation_index = 0    
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(648, 800), ypos))

    def animation_state(self):
            self.animation_index += 0.151666666666
            
            if self.animation_index >= len(self.frames):
                self.animation_index = 0
            self.image = self.frames[int(self.animation_index)]

    def destroy(self):

        if self.rect.x <= -50:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= 2.5
        self.destroy()

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True

pygame.init()

#Sets the Screen Size and Icon
screen = pygame.display.set_mode((448, 512))
pygame.display.set_caption("Monke")
#pygame.display.set_icon("icon.ico")
game_active = False

#This helps us set the Framerate
clock = pygame.time.Clock()

score = 0

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

#Setting the images for the game so far
bg_surf = pygame.image.load("images/level1.png").convert_alpha()
bg_rect = bg_surf.get_rect(topleft = (0, 0))

score_text = pygame.font.Font("font/W95FA.otf", 30)
score_surf = score_text.render("Score: " + str(score), False, "#afafaf")
score_rect = score_surf.get_rect(center = (224, 30))

#Intro Screen
player_stand = pygame.image.load("images/skg/run/skg-run1.png").convert_alpha()
player_stand = pygame.transform.scale2x(player_stand)
player_stand = pygame.transform.scale2x(player_stand)
#player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (224, 250))

game_name = pygame.font.Font("font/W95FA.otf", 50)
name_surf = game_name.render("Monke", False, "White")
name_rect = name_surf.get_rect(midtop = (224, 30))

inst_font = pygame.font.Font("font/W95FA.otf", 30)
inst_surf = inst_font.render("Press Space to start", False, "#afafaf")
inst_rect = inst_surf.get_rect(center = (224, 350))

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:

    #Checks input from the player
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(["blue barrel", "barrel", "barrel"])))

    if game_active:

        screen.blit(bg_surf, bg_rect)
        screen.blit(score_surf, score_rect)
        
        obstacle_group.draw(screen)
        obstacle_group.update()
        
        player.draw(screen)
        player.update()

        #Collisions
        game_active = collision_sprite()

    else:
        screen.fill((16, 16, 16))
        screen.blit(player_stand, player_stand_rect)
        
        screen.blit(name_surf, name_rect)
        screen.blit(inst_surf, inst_rect)

    pygame.display.update()
    clock.tick(60)