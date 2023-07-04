import pygame
from pygame import sprite

class Nor_atk():
    """a buttom to control normal atk"""
    def __init__(self, ai_settings, screen):
        self.screen = screen
        self.ai_settings = ai_settings
        self.screen_rect = screen.get_rect()
        self.image = pygame.image.load('images/normal_atk.bmp')
        #set location
        self.rect = self.image.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery - self.rect.height * 1.5

    def blitme(self):
        """draw the button"""
        self.screen.blit(self.image, self.rect)
        
class Magic():
    def __init__(self, ai_settings, screen):
        self.screen = screen
        self.ai_settings = ai_settings
        self.screen_rect = screen.get_rect()
        self.image = pygame.image.load('images/magic.bmp')
        #set location
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center

    def blitme(self):
        """draw the button"""
        self.screen.blit(self.image, self.rect)