import pygame
from pygame.sprite import Sprite

class TurnFlag(Sprite):
    def __init__(self, screen, ai_settings, stats):
        super(TurnFlag, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        self.image = pygame.image.load("images/turn.bmp")
        self.rect = self.image.get_rect()
        self.locate(stats)
        
    def locate(self,stats):
        self.rect.top = self.rect.height/8
        if stats.turn == 1:
            self.rect.right = (self.ai_settings.screen_wid/2) - self.rect.width
        else:
            self.rect.left = (self.ai_settings.screen_wid/2) + self.rect.width
    
    def blitme(self, stats):
        self.locate(stats)
        self.screen.blit(self.image,self.rect)