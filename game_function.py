import pygame
from settings import Settings
from pygame.sprite import Sprite, Group
from hero import Hero
from game_stats import GameStats
from namelist import DEFAULT_HEROES
import sys

def check_events(stats, heroes):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        #deal with select menu
        elif event.type == pygame.MOUSEBUTTONDOWN:
            stats.mouse_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if stats.mouse_down == True:
                stats.mouse_down == False
                #the mouse is clicked
                mouse_x, mouse_y = pygame.mouse.get_pos()
                clicked_sprite = check_mouse(heroes, mouse_x, mouse_y)
                if clicked_sprite != None:
                    #someone is clicked
                    tag = 4 * (clicked_sprite.team-1) + clicked_sprite.id
                    stats.select_menu[tag] = 1 - stats.select_menu[tag]
                print(stats.select_menu)

        
def update_screen(ai_settings, screen, heroes):
    screen.fill(ai_settings.bg_color)
    for id in range(4):
        hero = Hero(ai_settings, screen, 1, id, DEFAULT_HEROES[id])
        heroes.add(hero)
        hero.blitme()
    for id in range(4):
        hero = Hero(ai_settings, screen, 2, id, DEFAULT_HEROES[4 + id])
        heroes.add(hero)
        hero.blitme()
    #heroes.draw(screen)
    pygame.display.flip()

def check_mouse(group, mouse_x, mouse_y):
    for sprite in group.sprites():
        if sprite.rect.collidepoint(mouse_x, mouse_y):
            return sprite
    return None