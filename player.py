import pygame
from support import import_folder

class Player(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        
        #imports the sprites
        self.char_name = "skg"
        self.import_character_assets()
        self.frame_index = 0
        self.animationSpeed = 0.15
        
        #Setting up the Character
        self.state = 'idle'
        self.image = self.animations["idle"][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos) 

        #Player Movement
        self.facing_right = True
        self.isGrounded = False
        self.onCeiling = False
        self.onRight = False
        self.onLeft = False
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 1
        self.gravity = 0.3
        self.jump_height = -8
        # self.jump_height = -4

    def import_character_assets(self):
        char_path = f'images/{self.char_name}/'
        self.animations = {'idle': [], 'run': [], 'jump': [], "hammer_idle": [], "hammer_run": [], "climb": []}

        for animation in self.animations.keys():
            full_path = char_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.state]

        # Looping the animation
        self.frame_index += self.animationSpeed

        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image

        #Setting the Rect
        if self.isGrounded and self.onRight:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        
        elif self.isGrounded and self.onLeft:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)

        elif self.isGrounded:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)

        elif self.onCeiling and self.onRight:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        
        elif self.onCeiling and self.onLeft:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)

        elif self.onCeiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)

        # else:
        #     self.rect = self.image.get_rect(center = self.rect.midtop)


    def get_input(self):
        keys = pygame.key.get_pressed()    #We get all the possible inputs

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True

        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False

        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] & self.isGrounded:
            self.jump()

    def get_state(self):

        # if self.direction.y < 0 or self.direction.y > 0.9:
        if not self.isGrounded:
            self.state = "jump"

        else:
            if self.direction.x != 0:
                self.state = "run"
        
            else:
                self.state = "idle"

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_height

    def update(self):
        self.animate()
        self.get_state()
        self.get_input()
