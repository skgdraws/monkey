import pygame
from game_data import levels

class Node(pygame.sprite.Sprite):

    def __init__(self, pos, status, icon_speed):
        super().__init__()

        self.image = pygame.Surface((100,25))

        if status == 'unlock':
            self.image.fill('dark blue')

        else:
            self.image.fill('dark red')

        self.rect = self.image.get_rect(center = pos)

        self.detection_zone = pygame.Rect(self.rect.centerx-(icon_speed/2), self.rect.centery-(icon_speed/2), icon_speed, icon_speed)

class Icon(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.pos = pos

        self.image = pygame.Surface((16,16))
        self.image.fill('gold')
        self.rect = self.image.get_rect(center = pos)

    def update(self):
        self.rect.center = self.pos

class Overworld:

    def __init__(self, start_level, max_level, surface, create_level):
        
        #Setting up the surface to be displayed
        self.display = surface

        #Level Logic
        self.max_level = max_level
        self.current_level = start_level
        self.create_level = create_level

        #movement logic
        self.move_direction = pygame.math.Vector2(0,0)
        self.speed = 3.5
        self.moving = False

        #Sprites for the name stuff
        self.setup_nodes()
        self.setup_icon()

    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()

        for index, node_data in enumerate(levels.values()):

            if index <= self.max_level:
                node_sprite = Node(node_data['node_pos'], "unlock", self.speed)
                self.nodes.add(node_sprite)

            else:
                node_sprite = Node(node_data['node_pos'], "lock", self.speed)
                self.nodes.add(node_sprite)

    def draw_paths(self):
        points = [node["node_pos"] for index, node in enumerate(levels.values()) if index <= self.max_level]
        pygame.draw.lines(self.display, "dark blue", False, points, 6)

    def setup_icon(self):
        self.icon = pygame.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.moving:
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                if self.current_level < self.max_level:
                    self.move_direction = self.get_movement_data('up')
                    print(self.move_direction)
                    self.current_level += 1
                    self.moving = True
                
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                if self.current_level > 0:
                    self.move_direction = self.get_movement_data('down')
                    print(self.move_direction)
                    self.current_level -= 1
                    self.moving = True

            elif keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
                self.create_level(self.current_level)

        # Old imput
        # if keys[pygame.K_w] or keys[pygame.K_UP]:
        #     if self.current_level < self.max_level:
        #         self.current_level += 1
            
        # elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
        #     if self.current_level > 0:
        #         self.current_level -= 1

    def get_movement_data(self, dir_icon):

        if dir_icon == 'up':
            start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level+1].rect.center)
            return (end - start).normalize()
        
        if dir_icon == 'down':
            start = pygame.math.Vector2(self.nodes.sprites()[self.current_level-1].rect.center)
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
            finalVector = (start - end)
            return finalVector.normalize()

    def update_icon_pos(self):
        # self.icon.sprite.rect.center = self.nodes.sprites()[self.current_level].rect.center
        if self.moving and self.move_direction:
            self.icon.sprite.pos += self.move_direction * self.speed
            target = self.nodes.sprites()[self.current_level]

            if target.detection_zone.collidepoint(self.icon.sprite.pos):
                self.moving = False
                self.move_direction = pygame.math.Vector2(0,0)

    def run(self):
        self.input()
        self.update_icon_pos()
        self.icon.update()
        self.draw_paths()
        self.nodes.draw(self.display)
        self.icon.draw(self.display)
