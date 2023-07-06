import pygame
from settings import Settings
from pygame.sprite import Sprite, Group
from hero import Hero
from game_stats import GameStats
from extra_aid import TurnFlag
from namelist import DEFAULT_HEROES
import sys

def check_events(stats, heroes, nor_atk, magic, skill):
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
                    for i in range(0,8):
                        stats.select_menu[i] = 0
                if magic.rect.collidepoint(mouse_x, mouse_y):
                    stats.select_action = 2
                    for i in range(0,8):
                        stats.select_menu[i] = 0
                if skill.rect.collidepoint(mouse_x, mouse_y):
                    stats.select_action = 3
                    for i in range(0,8):
                        stats.select_menu[i] = 0
                
def generate_hero(ai_settings, screen, heroes):
    for id in range(4):
        hero = Hero(ai_settings, screen, 1, id, DEFAULT_HEROES[id])
        heroes.add(hero)
    for id in range(4):
        hero = Hero(ai_settings, screen, 2, id, DEFAULT_HEROES[4 + id])
        heroes.add(hero)
        
def update_screen(ai_settings, screen, heroes, nor_atk, magic, skill, stats):
    screen.fill(ai_settings.bg_color)
    for id in range(8):   
        heroes.sprites()[id].blitme(stats.select_menu[id])
    nor_atk.blitme()
    magic.blitme()
    skill.blitme()
    drawFlag(ai_settings, screen, stats)
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
        if stats.select_action == 1 and stats.able_select[tag] == 1:
            #可以被选择
            normalAttack(heroes, stats, tag)
        if stats.select_action == 2 and stats.able_select[tag] == 1:
            if stats.has_acted[tag%4] == 0:
                if stats.turn == 1:
                    stats.mp1 += clicked_sprite.mp
                    stats.able_select[tag] = 0
                    stats.has_acted[tag%4] = 1
                if stats.turn == 2:
                    stats.mp2 += clicked_sprite.mp
                    stats.able_select[tag] = 0
                    stats.has_acted[tag%4] = 1
        if stats.select_action == 3 and stats.able_select[tag] == 1:
            #check skill part
            ask_for_selection()

def check_turn(stats, heroes):
    cnt = 0
    for i in range(0,8):
        if heroes.sprites()[i].hp <= 0:
            heroes.sprites()[i].isalive = False
            stats.able_select[i] = -1
        else:
            if (i < 4  and stats.turn == 1) or (i >= 4 and stats.turn == 2):
                cnt += 1
    if sum(stats.has_acted) == cnt:
        stats.turn = 3 - stats.turn
        for i in range(0,4):
            stats.has_acted[i] = 0
        for i in range(0,4):
            stats.able_select[(stats.turn - 1)*4 + i] = 1
        for i in range(0,8):
            stats.select_menu[i] = 0

def normalAttack(heroes, stats, tag):
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

def drawFlag(ai_settings, screen, stats):
    flag1 = TurnFlag(ai_settings, screen, stats, 1)
    flag2 = TurnFlag(ai_settings, screen, stats, 2)
    flag1.blitme()
    flag2.blitme()

def ask_for_selection():
    """find a selection"""