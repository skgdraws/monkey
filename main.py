import pygame
from sys import exit

pygame.init()

#Sets the Screen Size and Icon
screen = pygame.display.set_mode((448, 512))
pygame.display.set_caption("Monkey")
#pygame.display.set_icon("icon.ico")

#This helps us set the Framerate
clock = pygame.time.Clock()

#Setting the images for the game so far
bg_surf = pygame.image.load("images/level1.png").convert_alpha()
bg_rect = bg_surf.get_rect(topleft = (0, 0))

player_surf = pygame.image.load("images/mario/mario1.png").convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80, 496))

while True:

    #Checks input from the player
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(bg_surf, bg_rect)
    screen.blit(player_surf, player_rect)

    pygame.display.update()
    clock.tick(60)