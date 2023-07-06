from pygame.sprite import Sprite
import pygame
import pygame.font
from namelist import DATALIST

import settings

class Hero(Sprite):
    """玩家可操控的角色"""
    
    def __init__(self, ai_settings, screen, team, id, name):
        #initiallize part
        super(Hero,self).__init__()
        self.screen = screen
        self.name = name
        self.team = team
        self.id = id
        self.ai_settings = ai_settings
        #set the image mode
        self.image = pygame.image.load('images/heroblock.bmp')
        self.rect = self.image.get_rect()
        #select_frame
        self.select_image = pygame.image.load('images/able_select.bmp')
        self.s_rect = self.select_image.get_rect()

        if id == 0:
            self.rect.left = int(2 * self.rect.width)
            self.rect.centery = ai_settings.screen_hgt/2
        else:
            self.rect.left = int(self.rect.width/2)
            self.rect.centery = (ai_settings.screen_hgt/2) + self.rect.height*(id-2)
        if team == 2:
            self.rect.centerx = ai_settings.screen_wid - self.rect.centerx

        #locate frame
        self.s_rect.center = self.rect.center
        #all the data of the hero
        self.reset_elements()

        #set text
        self.font = pygame.font.SysFont(ai_settings.text_font, 40)

        #person stats
        self.isalive = True

    def reset_elements(self):
        """initialization:
        the concrete data of the heroes varies from name"""
        self.hp = DATALIST[self.name][0]
        self.atk = DATALIST[self.name][1]
        self.dfn = DATALIST[self.name][2]
        self.mp = DATALIST[self.name][3]

    #表示这一段我实在重构不出来了，只能写这么又臭又长的一段，不好意思捏
    def preptext(self):
        """turn the text into images"""
        self.name_image = self.font.render(str(self.name), True, self.ai_settings.text_color, None)
        self.hp_image = self.font.render(str(self.hp), True, self.ai_settings.text_color, None)
        self.atk_image = self.font.render(str(self.atk), True, self.ai_settings.text_color, None)
        self.dfn_image = self.font.render(str(self.dfn), True, self.ai_settings.text_color, None)
        self.mp_image = self.font.render(str(self.mp), True, self.ai_settings.text_color, None)
        #set locations
        self.name_image_rect = self.name_image.get_rect()
        self.hp_image_rect = self.hp_image.get_rect()
        self.atk_image_rect = self.atk_image.get_rect()
        self.dfn_image_rect = self.dfn_image.get_rect()
        self.mp_image_rect = self.mp_image.get_rect()

        self.name_image_rect.centerx = self.rect.centerx
        self.hp_image_rect.centerx = self.rect.centerx
        self.atk_image_rect.centerx = self.rect.centerx
        self.dfn_image_rect.centerx = self.rect.centerx
        self.mp_image_rect.centerx = self.rect.centerx

        self.name_image_rect.top = self.rect.top + 15
        self.hp_image_rect.top = self.name_image_rect.bottom + 5
        self.atk_image_rect.top = self.hp_image_rect.bottom + 5
        self.dfn_image_rect.top = self.atk_image_rect.bottom + 5
        self.mp_image_rect.top = self.dfn_image_rect.bottom + 5
        
    def blitme(self, enabled):
        self.preptext()
        """draw the heroblock"""
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.name_image, self.name_image_rect)
        self.screen.blit(self.hp_image, self.hp_image_rect)
        self.screen.blit(self.atk_image, self.atk_image_rect)
        self.screen.blit(self.dfn_image, self.dfn_image_rect)
        self.screen.blit(self.mp_image, self.mp_image_rect)
        
        if enabled == 1:
            self.screen.blit(self.select_image,self.s_rect)
