import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()          #initializes the Sprite module to be used later

        # self.image = pygame.Surface((size, size))
        # self.image.fill("Gold")
        self.image = pygame.image.load("images/tiles/ground1.png")
        self.rect = self.image.get_rect(topleft = pos)

class Ladder(pygame.sprite.Sprite):
    
    def __init__(self, pos, size):
        super().__init__()

        # self.image = pygame.Surface((size, size))
        # self.image.fill("Gold")
        self.image = pygame.image.load("images/tiles/ladder.png")
        self.rect = self.image.get_rect(topleft = pos)

# class Saved(pygame)