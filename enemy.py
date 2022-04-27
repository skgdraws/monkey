import pygame
from tiles import AnimatedTile

class Enemy(AnimatedTile):

    def __init__(self, pos, size):
        super().__init__(pos, size, 'images/barrel/normal/roll')

        self.rect.y += size - self.image.get_size()[1]
        self.speed = 1
        self.gravity = 0.3

        hitbox = pygame.Surface((16, 32))
        # self.detection_zone = pygame.Rect(self.rect.x, self.rect.y - 20, self.image.get_size()[0] * 2, self.image.get_size()[1] * 2)
        self.detection_zone = hitbox.get_rect(midbottom = (self.rect.x, self.rect.y + 10))

    def move(self):
        self.rect.x += self.speed
        self.detection_zone.x += self.speed

    def reverse_image(self):
        if self.speed < 0:
            self.image = pygame.transform.flip(self.image, True, False)
            
        
    def reverse(self):
        self.speed *= -1
        
    # def apply_gravity(self):
    #     self.direction.y += self.gravity
    #     self.rect.y += self.direction.y

    def update(self, shift):
        self.rect.x += shift
        self.animate()
        # self.apply_gravity()
        self.move()
        self.reverse_image()