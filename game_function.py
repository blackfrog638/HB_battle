import pygame
from settings import Settings
from pygame.sprite import Sprite, Group
from hero import Hero
from game_stats import GameStats
from namelist import DEFAULT_HEROES
import sys

def check_events(stats, heroes, nor_atk):
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
                set_herolist(heroes, mouse_x, mouse_y, stats)
                if nor_atk.rect.collidepoint(mouse_x, mouse_y):
                    stats.select_action = 1
                
def generate_hero(ai_settings, screen, heroes):
    for id in range(4):
        hero = Hero(ai_settings, screen, 1, id, DEFAULT_HEROES[id])
        heroes.add(hero)
    for id in range(4):
        hero = Hero(ai_settings, screen, 2, id, DEFAULT_HEROES[4 + id])
        heroes.add(hero)
        
def update_screen(ai_settings, screen, heroes, nor_atk):
    screen.fill(ai_settings.bg_color)
    for id in range(8):   
        heroes.sprites()[id].blitme()
    nor_atk.blitme()
    #heroes.draw(screen)
    pygame.display.flip()

def check_mouse(group, mouse_x, mouse_y):
    for sprite in group.sprites():
        if sprite.rect.collidepoint(mouse_x, mouse_y):
            return sprite
    return None

def set_herolist(heroes, mouse_x, mouse_y, stats):
    clicked_sprite = check_mouse(heroes, mouse_x, mouse_y)
    if clicked_sprite != None:
        #someone is clicked
        tag = 4 * (clicked_sprite.team-1) + clicked_sprite.id
        if stats.select_action == 1:
            if stats.able_select[tag] == 1:   
                #可以被选择
                if stats.turn * 4 - tag > 0 and stats.turn * 4 - tag <= 4 and stats.has_acted[tag%4] == 0:
                    #是自己队伍的
                    if stats.turn == 1:
                        for i in range(4,8):
                            stats.able_select[i] = 1
                        for i in range(0,4):
                            if i != tag:
                                stats.select_menu[i] = 0
                    else:
                        for i in range(0,4):
                            stats.able_select[i] = 1
                        for i in range(4,8):
                            if i != tag:
                                stats.select_menu[i] = 0
                    stats.select_menu[tag] = 1 - stats.select_menu[tag]
                else:
                    if stats.turn == 1:
                        obj = 0
                        for i in range(0,4):
                            if stats.select_menu[i] == 1:
                                obj = i
                        heroes.sprites()[tag].hp -= (heroes.sprites()[obj].atk) - (heroes.sprites()[tag].dfn)
                        
                        stats.has_acted[obj % 4] = 1
                        stats.able_select[obj] = 0
                        for i in range(0,8):
                            stats.select_menu[i] = 0
                        for i in range(4,8):
                            stats.able_select[i] = 0
                    else:
                        obj = 0
                        for i in range(4,8):
                            if stats.select_menu[i] == 1:
                                obj = i
                        heroes.sprites()[tag].hp -= (heroes.sprites()[obj].atk) - (heroes.sprites()[tag].dfn)
                        
                        stats.has_acted[obj % 4] = 1
                        stats.able_select[obj] = 0
                        for i in range(0,8):
                            stats.select_menu[i] = 0
                        for i in range(0,4):
                            stats.able_select[i] = 0

                
        print(stats.select_menu)

def check_turn(stats):
    if sum(stats.has_acted) == 4:
        stats.turn = 3 - stats.turn
        for i in range(0,4):
            stats.has_acted[i] = 0
        for i in range(0,4):
            stats.able_select[(stats.turn - 1)*4 + i] = 1