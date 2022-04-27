import pygame
import sys
from settings import *
from level import Level
from levelselect import Overworld
from ui import UI

class Game:
    def __init__(self):

        #Game Attributes
        self.max_level = 4
        self.lives = 3
        self.curLives = 3
        self.score = 0

        #Overworld
        self.overworld = Overworld(0, self.max_level, screen, self.create_level)
        self.status = 'overworld'

        #UI
        self.ui = UI(screen)

    def create_level(self, current_level):
        self.level = Level(current_level, screen, self.create_overworld, self.update_score, self.update_lives)
        self.status = 'level'

    def create_overworld(self, curLevel, new_max_level):
        
        if curLevel > new_max_level:
            curLevel = new_max_level
        
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        
        self.overworld = Overworld(curLevel, self.max_level, screen, self.create_level)
        self.status = 'overworld'

    def update_score(self, amount):
        self.score += amount
    
    def update_lives(self, amount):
        self.curLives += amount

    def checkGameOver(self):
        if self.curLives <= 0:
            
            self.max_level = 4
            self.score = 0
            self.curLives = 3
            self.overworld = Overworld(0, self.max_level, screen, self.create_level)
            self.status = 'overworld'

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        
        elif self.status == 'level':
            self.level.run()
            self.ui.show_lives(self.curLives)
            self.ui.show_score(self.score)
            self.checkGameOver()

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Monkey")
clock = pygame.time.Clock()
game = Game()
gameStart = True


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
