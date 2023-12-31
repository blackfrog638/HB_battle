import pygame
from settings import Settings
from pygame.sprite import Sprite, Group
from hero import Hero
from game_stats import GameStats
from extra_aid import TurnFlag
from namelist import DEFAULT_HEROES, SKILL_SELECTION
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
        if heroes.sprites()[id].isalive:
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
        if stats.is_choosing == False:
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
            if stats.select_action == 3 and stats.able_select[tag] == 1 and stats.has_acted[tag % 4] == 0:
                #check skill part
                if stats.turn == 1:
                    if stats.half_cost1 == 0 and stats.mp1 >= 3:
                        stats.mp1 -= 3
                        skill(stats, heroes, tag)
                    if stats.half_cost1 != 0 and stats.mp1 >= 6:
                        stats.mp1 -= 6
                        skill(stats, heroes, tag)
                else:
                    if stats.half_cost2 == 0 and stats.mp2 >= 3:
                        stats.mp1 -= 3
                        skill(stats, heroes, tag)
                    if stats.half_cost2 != 0 and stats.mp2 >= 6:
                        stats.mp2 -= 6
                        skill(stats, heroes, tag)
        else:
            #开始在skill部分选人
            if len(SKILL_SELECTION[heroes.sprites()[stats.on_skill].name]) != 0:
                if check_legal(SKILL_SELECTION[heroes.sprites()[stats.on_skill].name][stats.skill_period], heroes.sprites()[stats.on_skill], clicked_sprite):
                    stats.personlist.append(tag)
                    stats.skill_period += 1
                 #检查是否已经选满可以结束
            if stats.skill_period == len(SKILL_SELECTION[heroes.sprites()[stats.on_skill].name]):
                deal_with_skills(heroes, stats)
                #重新归零
                stats.has_acted[stats.on_skill % 4] = 1
                stats.is_choosing = False
                stats.personlist = []
                stats.on_skill = -1
                stats.skill_period = 0

def check_turn(stats, heroes):
    cnt = 0
    #cnt:现存本队存活人数
    for i in range(0,8):
        if heroes.sprites()[i].hp <= 0:
            heroes.sprites()[i].isalive = False
            stats.able_select[i] = -1
        else:
            if (i < 4  and stats.turn == 1) or (i >= 4 and stats.turn == 2):
                cnt += 1
    if sum(stats.has_acted) == cnt:
        stats.turn = 3 - stats.turn
        stats.half_cost1 -= 1
        stats.half_cost2 -= 1
        for i in range(0,4):
            stats.has_acted[i] = 0
            #被嘲讽的角色失去操作机会
            if heroes.sprites()[i + (stats.turn-1) * 4].taunt:
                stats.has_acted[i] = 1
                heroes.sprites()[i + (stats.turn-1) * 4].taunt = False
        for i in range(0,4):
            stats.able_select[(stats.turn - 1)*4 + i] = 1
        for i in range(0,8):
            heroes.sprites()[i].shield -= 1
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
        if heroes.sprites()[tag].shield <= 0:
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

def check_legal(limit, subject, hero):
    if limit == 'a teammate':
        return subject.team == hero.team
    if limit == 'an enemy':
        return subject.team != hero.team
    if limit == 'a dead person':
        return (not hero.isalive)
    
def deal_with_skills(heroes, stats):
    """fixing"""
    target_sprite = heroes.sprites()[stats.on_skill]
    if target_sprite.name == 'bzf':
        heroes.sprites()[stats.on_skill].atk += 1
        heroes.sprites()[stats.on_skill].hp -= 4
    if target_sprite.name == 'lby':
        heroes.sprites()[stats.personlist[0]].shield = 2
    if target_sprite.name == 'bcd':
        if stats.turn == 1:
            stats.mp2 -= 9
            if stats.mp2 < 0:
                stats.mp2 = 0
        if stats.turn == 2:
            stats.mp1 -= 9
            if stats.mp1 < 0:
                stats.mp1 = 0
    if target_sprite.name == 'lal':
        stats.has_acted[stats.personlist[0]] = 0
        stats.able_select[stats.personlist[0]] = 1
    if target_sprite.name == 'syy':
        heroes.sprites()[stats.on_skill].hp -= (heroes.sprites()[stats.personlist[0]].atk - heroes.sprites()[stats.on_skill].dfn-1)
        heroes.sprites()[stats.personlist[0]].taunt = True
    if target_sprite.name == 'czr':
        heroes.sprites()[stats.personlist[0]].hp -= (target_sprite.atk + 1 - heroes.sprites()[stats.personlist[0]].dfn)
        heroes.sprites()[stats.personlist[1]].hp -= (target_sprite.atk + 1 - heroes.sprites()[stats.personlist[1]].dfn)
    if target_sprite.name == 'zs':
        if stats.turn == 1:
            stats.half_cost1 = 2
        if stats.turn == 2:
            stats.half_cost2 = 2
    if target_sprite.name == 'hj':
        heroes.sprites()[stats.on_skill].hp += 5

def skill(stats, heroes, tag):
    stats.on_skill = tag
    stats.is_choosing = True
    stats.personlist = []
    for i in range(0,8):
        stats.select_menu[i] = 0

    if len(SKILL_SELECTION[heroes.sprites()[tag].name]) == 0:
        deal_with_skills(heroes, stats)
        #重新归零
        stats.has_acted[tag % 4] = 1
        stats.is_choosing = False
        stats.personlist = []
        stats.on_skill = -1
        stats.skill_period = 0