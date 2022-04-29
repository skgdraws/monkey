import pygame
from enemy import Enemy
from tiles import Saved, StaticTile, Tile
from settings import tile_size, screen_height, screen_width
from player import Player
from game_data import levels
from support import import_csv_layout, import_cut_graphics

class Level:
    def __init__(self, curLevel, surface, create_overworld, update_score, update_lives, player_name):
        
        #Sets up the Levels
        self.display_surface = surface
        self.world_shift = 2

        #Audio
        self.win_sound = pygame.mixer.Sound("audio/sfx/win.wav")
        self.win_sound.set_volume(0.6)
        self.hit_sound = pygame.mixer.Sound("audio/sfx/hurt.wav")
        self.hit_sound.set_volume(0.6)

        #Overworld connection
        self.create_overworld = create_overworld
        self.current_level = curLevel
        level_data = levels[self.current_level]
        self.new_maxLevel = level_data['unlock']

        #UI
        self.update_score = update_score
        self.update_lives = update_lives

        #Player
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.player_name = player_name
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        # Sets up terrain
        terrain_layout = import_csv_layout(level_data['ground'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'ground')
        
        oil_layout = import_csv_layout(level_data['decor'])
        self.oil_sprites = self.create_tile_group(oil_layout, 'decor')

        #Sets up Enemies
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')

        #Sets up Constraints
        constraints_layout = import_csv_layout(level_data['constraints'])
        self.constraints_sprites = self.create_tile_group(constraints_layout, 'constraints')

    def create_tile_group(self, layout, sprite_name):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                
                if val != "-1":
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if sprite_name == 'ground':
                        terrain_tile_list = import_cut_graphics('images/tiles/ground1.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile((x,y), tile_size, tile_surface)

                    if sprite_name == 'decor':
                        oil_tile_list = import_cut_graphics('images/tiles/decor.png')
                        tile_surface = oil_tile_list[int(val)]
                        sprite = StaticTile((x,y), tile_size, tile_surface)
                    
                    if sprite_name == 'enemies':
                        sprite = Enemy((x, y), tile_size)

                    if sprite_name == 'constraints':
                        sprite = Tile((x, y), tile_size)

                    sprite_group.add(sprite)

        return sprite_group

    def player_setup(self, layout):

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                
                x = col_index * tile_size
                y = row_index * tile_size
                
                if val == "0":
                    sprite = Player((x,y), self.player_name)
                    self.player.add(sprite)

                if val == "1":

                    if self.player_name == 'skg':
                        saved_sprite = pygame.image.load('images/m00n/idle/m00n-idle.png')
                    else:
                        saved_sprite = pygame.image.load('images/skg/idle/skg-idle.png')

                    sprite = Saved((x, y - 2), tile_size, saved_sprite)
                    self.update_score(500)
                    self.goal.add(sprite)

    def enemy_fall_reverse(self):
        for enemy in self.enemy_sprites.sprites():

            if pygame.sprite.spritecollide(enemy,self.constraints_sprites,False):
                enemy.reverse()	

    def horizontal_movement_collision(self):
        player = self.player.sprite

        #sets the movement of the playable character
        player.rect.x += player.direction.x * player.speed

        for sprite in self.terrain_sprites.sprites():

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

        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:  # Checks collision on the bottom of the player
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.isGrounded = True
                    player.gotPoints = False

                elif player.direction.y < 0:  # Checks collision on the top of the player
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.onCeiling = True

            if player.isGrounded and player.direction.y < 0 or player.direction.y > 1:
                player.isGrounded = False

            if player.onCeiling and player.direction.y > 0:
                player.onCeiling = False

    def check_death(self):
        if self.player.sprite.rect.top > screen_height or self.player.sprite.died:
            self.update_lives(-1)
            self.create_overworld(self.current_level, 0, self.player_name)

    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.win_sound.play()
            self.create_overworld(self.current_level, self.new_maxLevel, self.player_name)

    def check_enemy_collisions(self):
        
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite, self.enemy_sprites, False)
        
        for enemy in self.enemy_sprites:
            
            if enemy.detection_zone.collidepoint(self.player.sprite.rect.center) and not self.player.sprite.gotPoints and not self.player.sprite.isGrounded:
                self.update_score(100)
                self.player.sprite.gotPoints = True

        if enemy_collisions:
            for enemy in enemy_collisions:
                self.player.sprite.died = True
                self.hit_sound.play()


    def scroll_x(self):

        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < 150 and direction_x < 0:
            self.world_shift = 2
            player.speed = 0
        
        elif player_x > 300 and direction_x > 0:
            self.world_shift = -2
            player.speed = 0

        else:
            self.world_shift = 0
            player.speed = 2  

    def run(self):
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        self.oil_sprites.update(self.world_shift)
        self.oil_sprites.draw(self.display_surface)

        self.constraints_sprites.update(self.world_shift)
        self.enemy_sprites.update(self.world_shift)
        self.enemy_fall_reverse()
        self.enemy_sprites.draw(self.display_surface)

        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)
        
        self.scroll_x()
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)

        self.check_enemy_collisions()

        self.check_death()
        self.check_win()
