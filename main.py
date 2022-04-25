import pygame
import sys
from settings import *
from level import Level, test_level
from levelselect import Overworld

class Game:
    def __init__(self):
        self.max_level = 1
        self.overworld = Overworld(0, self.max_level, screen, self.create_level)
        self.status = 'overworld'

    def create_level(self, current_level):
        self.level = test_level(current_level, screen, self.create_overworld)
        self.status = 'level'
        print(current_level)

    def create_overworld(self, curLevel, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        
        self.overworld = Overworld(curLevel, self.max_level, screen, self.create_level)
        self.status = 'overworld'

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        
        elif self.status == 'level':
            self.level.run()

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
gameStart = True
# level = Level(level_data, screen)
game = Game()

while gameStart:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill("#000000")
    game.run()
    # level.run()

    pygame.display.update()
    clock.tick(60)