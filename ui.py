import pygame

class UI:

    def __init__(self, surface):
        
        #setup
        self.display_surf = surface
        #Lives
        self.lives_icon = pygame.image.load('assets/images/ui/life-icon.png').convert_alpha()
        #Score
        self.score_disp = pygame.image.load('assets/images/ui/score.png').convert_alpha()
        self.score_rect = self.score_disp.get_rect(topleft = (20, 30))
        self.font = pygame.font.Font("assets/font/kongtext.ttf", 15)

    def show_lives(self, current):

        for i in range(current):
            
            sprite = self.lives_icon
            sprite_rect = sprite.get_rect(topleft = (20 + 20 * i, 70))
            
            self.display_surf.blit(sprite, sprite_rect)

    def show_score(self, amount):

        self.display_surf.blit(self.score_disp, self.score_rect)
        score_amount_surf = self.font.render(str(amount), False, "#FFFFFF")
        score_amount_rect = score_amount_surf.get_rect(center = (self.score_rect.centerx, self.score_rect.centery + 5))
        self.display_surf.blit(score_amount_surf, score_amount_rect)