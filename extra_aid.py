import pygame
from pygame.sprite import Sprite
import pygame.font

class TurnFlag(Sprite):
    def __init__(self, ai_settings, screen, stats, team):
        super(TurnFlag, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.screen_rect = screen.get_rect()
        self.stats = stats
        self.team = team

        #font part
        self.font = pygame.font.SysFont(None, 60)
        self.text_color = (30, 30, 30)

    def preptext(self):
        self.text = ''
        if self.team == 1:
            self.text = str(self.stats.mp1)
        if self.team == 2:
            self.text = str(self.stats.mp2)
        self.txt_image = self.font.render(self.text, True, self.text_color, None)
        self.txt_image_rect = self.txt_image.get_rect()

    def blitme(self):
        self.image = 0
        self.rect = 0
        #image rect
        if self.team == 1:
            if self.stats.turn == 1:
                self.image = pygame.image.load('images/team11.bmp')
            else:
                self.image = pygame.image.load('images/team12.bmp')
            self.rect = self.image.get_rect()
            self.rect.right = self.screen_rect.centerx - 40
        else:
            if self.stats.turn == 2:
                self.image = pygame.image.load('images/team21.bmp')
            else:
                self.image = pygame.image.load('images/team22.bmp')
            self.rect = self.image.get_rect()
            self.rect.left = self.screen_rect.centerx + 40
        self.rect.top = self.rect.height / 4

        #text rect
        self.preptext()
        if self.team == 1:
            self.txt_image_rect.right = self.rect.right - 20 
        else:
            self.txt_image_rect.left = self.rect.left + 20
        self.txt_image_rect.centery = self.rect.centery

        self.screen.blit(self.image,self.rect)
        self.screen.blit(self.txt_image, self.txt_image_rect)