import pygame
from tiles import Ladder, Tile
from settings import tile_size
from player import Player

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

    def run(self):
        #Level Tiles
        self.tiles.draw(self.display_surface)
        self.ladders.draw(self.display_surface)
        #Player 
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)