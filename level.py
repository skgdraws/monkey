import pygame
from tiles import Ladder, Tile
from settings import tile_size, screen_height, screen_width
from player import Player
from game_data import levels

class Level:
    def __init__(self, level_data, surface):
        
        #Sets up the Levels
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0
        self.currentX = 0

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.ladders = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        for row_index, row in enumerate(layout):    #Checks every row of the level Data
            
            for col_index, cell in enumerate(row):  #Checks the columns in the "matrix"
                x = col_index * tile_size
                y = row_index * tile_size

                if cell == 'X':
                    tile = Tile((x,y), tile_size)
                    self.tiles.add(tile)
                
                if cell == 'H':
                    ladder = Ladder((x,y), tile_size)
                    self.ladders.add(ladder)

                if cell == 'P':     #Checks for the Player Position
                    player_sprite = Player((x,y))
                    self.player.add(player_sprite)

    def horizontal_movement_collision(self):
        player = self.player.sprite

        #sets the movement of the playable character
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:  # Checks collision on the left side of the player
                    player.rect.left = sprite.rect.right
                    player.onLeft = True
                    self.currentX = player.rect.left

                elif player.direction.x > 0:  # Checks collision on the right side of the player
                    player.rect.right = sprite.rect.left
                    player.onRight = True
                    self.currentX = player.rect.right

            if player.onLeft and (player.rect.left < self.currentX or player.direction.x >= 0):
                player.onLeft = False

            if player.onRight and (player.rect.right > self.currentX or player.direction.x <= 0):
                player.onReft = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:  # Checks collision on the bottom of the player
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.isGrounded = True

                elif player.direction.y < 0:  # Checks collision on the top of the player
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.onCeiling = True

            if player.isGrounded and player.direction.y < 0 or player.direction.y > 1:
                player.isGrounded = False

            if player.onCeiling and player.direction.y > 0:
                player.onCeiling = False

        for sprite in self.ladders.sprites():
            if sprite.rect.colliderect(player.rect):
                pass

    def run(self):
        #Level Tiles
        self.tiles.draw(self.display_surface)
        self.ladders.draw(self.display_surface)
        #Player 
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)

class test_level:
    def __init__(self, curlevel, surface, create_overworld):
        
        #Level Setup
        self.surface = surface
        self.curLevel = curlevel
        self.create_overworld = create_overworld

        level_data = levels[curlevel]
        level_content = level_data['content']
        self.new_max_level = level_data['unlock']

        self.font = pygame.font.Font('font/W95FA.otf', 15)
        self.text_surf = self.font.render(level_content, True, 'White')
        self.text_rect = self.text_surf.get_rect(center = (screen_width/2, screen_height/2))

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            self.create_overworld(self.curLevel, self.new_max_level)

        elif keys[pygame.K_RETURN]:
            self.create_overworld(self.curLevel, 0)

    def run(self):
        self.input()
        self.surface.blit(self.text_surf, self.text_rect)