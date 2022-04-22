from cmath import rect
import pygame
from sys import exit

pygame.init()

#Sets the Screen Size and Icon
screen = pygame.display.set_mode((448, 512))
pygame.display.set_caption("Depressed Monkey and boi")
#pygame.display.set_icon("icon.ico")
game_active = True

#This helps us set the Framerate
clock = pygame.time.Clock()

#Setting the images for the game so far
bg_surf = pygame.image.load("images/level1.png").convert_alpha()
bg_rect = bg_surf.get_rect(topleft = (0, 0))

player_surf = pygame.image.load("images/mario/mario1.png").convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80, 496))
player_grav = 0
player_speed = 0
isGround = False

barrel_surf = pygame.image.load("images/barrel/barrel1.png").convert_alpha()
barrel_rect = barrel_surf.get_rect(midbottom = (440, 496))

test_font = pygame.font.Font("font/W95FA.otf", 30)
score_surf = test_font.render("lmao monke", False, "White")
score_rect = score_surf.get_rect(midtop = (224, 10))

while True:


    #Checks input from the player
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pygame.transform.flip(player_surf, False, False)
                    player_speed = -3

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    pygame.transform.flip(player_surf, True, False)
                    player_speed = 3

            else:
                player_speed = 0
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and isGround:
                    player_grav = -4.5
                    isGround = False

    if game_active:

        barrel_rect.x -= 2.5

        if barrel_rect.right <= 0:
            barrel_rect.left = 448

        screen.blit(bg_surf, bg_rect)
        screen.blit(score_surf, score_rect)
        screen.blit(barrel_surf, barrel_rect)

        #Player
        player_grav += 0.3
        player_rect.x += player_speed
        player_rect.y += player_grav

        if player_rect.bottom >= 496:
            isGround = True
            player_rect.bottom = 496

        screen.blit(player_surf, player_rect)

        #Collisions
        if barrel_rect.colliderect(player_rect):
                game_active = False


    pygame.display.update()
    clock.tick(30)