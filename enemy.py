import pygame
from tiles import AnimatedTile

class Enemy(AnimatedTile):

    def __init__(self, pos, size):
        super().__init__(pos, size, 'images/barrel/normal/roll')

        self.rect.y += size - self.image.get_size()[1]
        self.speed = 1
        self.gravity = 0.3

        hitbox = pygame.Surface((16, 32))
        self.detection_zone = hitbox.get_rect(midtop = (self.rect.x, self.rect.y - 15))

    def move(self):
        self.rect.x += self.speed
        self.detection_zone.x += self.speed

    def reverse_image(self):
        if self.speed < 0:
            self.image = pygame.transform.flip(self.image, True, False)
            
        
    def reverse(self):
        self.speed *= -1
        
    def update(self, shift):
        self.rect.x += shift
        self.animate()
        self.move()
        self.reverse_image()