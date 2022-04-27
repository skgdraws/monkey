import pygame

from support import import_folder

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()          #initializes the Sprite module to be used later

        self.image = pygame.Surface((size, size))
        # self.image = pygame.image.load("images/tiles/ground1.png")
        self.rect = self.image.get_rect(topleft = pos)

    def update(self, shift):
        self.rect.x += shift

class AnimatedTile(Tile):
    def __init__(self, pos, size, path):
        super().__init__(pos, size)
        self.frames = import_folder(path)
        self.frameIndex = 0
        self.animSpeed = 0.15
        self.image = self.frames[self.frameIndex]

    def animate(self):
        self.frameIndex += self.animSpeed
        
        if self.frameIndex >= len(self.frames):
            self.frameIndex = 0
        
        self.image = self.frames[int(self.frameIndex)]
    
    def update(self, shift):
        self.rect.x += shift
        self.animate()

class StaticTile(Tile):

    def __init__(self, pos, size, surface):
        super().__init__(pos, size)
        self.image = surface

class Saved(pygame.sprite.Sprite):
    def __init__(self, pos, size, surface):
        super().__init__()          #initializes the Sprite module to be used later

        self.image = surface
        # self.image = pygame.image.load("images/tiles/ground1.png")
        self.rect = self.image.get_rect(midleft = pos)

    def update(self, shift):
        self.rect.x += shift

class checkFloor(Tile):

    def __init__(self, pos, size):
        super().__init__(pos, size)
        self.hasArrived = False