import pygame
from game_data import levels
from support import import_folder

class Node(pygame.sprite.Sprite):

    def __init__(self, pos, status, icon_speed, path):
        super().__init__()

        self.image = pygame.image.load(path)
        if status == 'unlock':
            self.status = 'available'

        else:
            self.image.fill('#111111')
            self.status = 'locked'

        self.rect = self.image.get_rect(center = pos)
        self.detection_zone = pygame.Rect(self.rect.centerx-(icon_speed/2), self.rect.centery-(icon_speed/2), icon_speed, icon_speed)

    def animate(self):
        pass

class Icon(pygame.sprite.Sprite):

    def __init__(self, pos, player_name):
        super().__init__()
        self.pos = pos

        self.player_name = player_name
        self.animation = import_folder(f"images/{player_name}/run")
        self.frame_index = 0
        self.animationSpeed = 0.15
        self.image = self.animation[0]
        self.rect = self.image.get_rect(center = pos)

    def animate(self):
        # Looping the animation
        self.frame_index += self.animationSpeed

        if self.frame_index >= len(self.animation):
            self.frame_index = 0

        self.image = self.animation[int(self.frame_index)]

    def update(self):
        self.animate()
        self.rect.center = self.pos

class Overworld:

    def __init__(self, start_level, max_level, surface, create_level, player_name):
        
        #Setting up the surface to be displayed
        self.display = surface

        #Level Logic
        self.max_level = max_level
        self.current_level = start_level
        self.create_level = create_level
        self.player_name = player_name

        #movement logic
        self.move_direction = pygame.math.Vector2(0,0)
        self.speed = 3.5
        self.moving = False

        #Sprites for the name stuff
        self.setup_nodes()
        self.setup_icon()

        # Time
        self.startTime = pygame.time.get_ticks()
        self.allowInput = False
        self.timerLength = 300

    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()

        for index, node_data in enumerate(levels.values()):

            if index <= self.max_level:
                node_sprite = Node(node_data['node_pos'], "unlock", self.speed, node_data['node_icon'])
                self.nodes.add(node_sprite)

            else:
                node_sprite = Node(node_data['node_pos'], "lock", self.speed, node_data['node_icon'])
                self.nodes.add(node_sprite)

    def draw_paths(self):
        if self.max_level != 0:
            points = [node["node_pos"] for index, node in enumerate(levels.values()) if index <= self.max_level]
            pygame.draw.lines(self.display, "dark red", False, points, 6)

    def setup_icon(self):
        self.icon = pygame.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center, self.player_name)
        self.icon.add(icon_sprite)

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.moving and self.allowInput:
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                if self.current_level < self.max_level:
                    self.move_direction = self.get_movement_data('up')
                    self.current_level += 1
                    self.moving = True
                
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                if self.current_level > 0:
                    self.move_direction = self.get_movement_data('down')
                    self.current_level -= 1
                    self.moving = True

            elif keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
                self.create_level(self.current_level)

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

    def input_timer(self):

        if not self.allowInput:
            currentTime = pygame.time.get_ticks()
            if currentTime - self.startTime >= self.timerLength:
                self.allowInput = True

    def run(self):
        self.input_timer()
        self.input()
        self.update_icon_pos()
        self.icon.update()
        self.draw_paths()
        self.nodes.draw(self.display)
        self.icon.draw(self.display)
