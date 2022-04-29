import pygame, sys
from settings import *
from menu import MainMenu
from levelselect import Overworld
from level import Level
from ui import UI
from settings import screen_height, screen_width
from gamover import game_over, hall_of_fame

class Game:
    def __init__(self, screen):

        #Game Attributes
        self.max_level = 0
        self.lives = 3
        self.curLives = 3
        self.score = 0
        self.savedscore = 0
        self.screen = screen
        self.display = pygame.Rect(0, 0, screen_width, screen_height)
        self.allowInput = True
        self.player = 'skg'

        #audio
        self.bg_music = pygame.mixer.Sound("audio/music/stack_overflow.wav")
        self.bg_music.set_volume(0.1)

        #States
        self.overworld = Overworld(0, self.max_level, self.screen, self.create_level, self.player)
        self.mainMenu = MainMenu(self.screen, self.create_overworld)
        self.status = 'main menu'
        self.bg_music.play(loops= -1)

        #UI
        self.ui = UI(screen)

    def create_level(self, current_level):
        self.level = Level(current_level, self.screen, self.create_overworld, self.update_score, self.update_lives, self.player)
        self.status = 'level'

    def create_overworld(self, curLevel, new_max_level, player):
        
        if curLevel > new_max_level:
            curLevel = new_max_level
        
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        
        else:
            new_max_level = self.max_level
        
        self.overworld = Overworld(curLevel, self.max_level, self.screen, self.create_level, player)
        self.player = player
        self.status = 'overworld'

    def update_score(self, amount):
        self.score += amount

    def update_lives(self, amount):
        self.curLives += amount

    def checkGameOver(self):
        if self.curLives <= 0:
            
            self.max_level = 0
            self.savedscore = self.score
            self.score = 0
            self.curLives = 3
            self.overworld = Overworld(0, self.max_level, self.screen, self.create_level, self.player)
            self.status = 'game over'

    def run(self):

        if self.status == 'main menu':
            self.mainMenu.run()

        elif self.status == 'overworld':
            self.overworld.run()
                
        elif self.status == 'level':
            self.level.run()
            self.ui.show_lives(self.curLives)
            self.ui.show_score(self.score)
            self.checkGameOver()

        elif self.status == 'game over':
            self.mainMenu.run()
            game_over(self.savedscore)
            hall_of_fame()
            self.status = 'main menu'
            

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Monkey")
clock = pygame.time.Clock()

icon = pygame.image.load('images/skg-icon.png')
pygame.display.set_icon(icon)

game = Game(screen)
game.allowInput = True

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                game.allowInput = True

            if event.key == pygame.K_DOWN:
                game.allowInput = True

    screen.fill("#000000")
    game.run()
    pygame.display.update()
    clock.tick(60)