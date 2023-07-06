import pygame
from pygame.sprite import Sprite,Group

from game_stats import GameStats
from settings import Settings
from hero import Hero
from actions import Nor_atk, Magic, Skill
import game_function as gf

def run_game():
    pygame.init()
    ai_settings = Settings()
    stats = GameStats()
    screen = pygame.display.set_mode((ai_settings.screen_wid,ai_settings.screen_hgt))
    nor_atk = Nor_atk(ai_settings, screen)
    magic = Magic(ai_settings, screen)
    skill = Skill(ai_settings, screen)
    pygame.display.set_caption("HB_battle")
    heroes = Group()
    gf.generate_hero(ai_settings, screen, heroes)
    while True:
        gf.update_screen(ai_settings, screen, heroes, nor_atk, magic, skill, stats)
        gf.check_events(stats, heroes, nor_atk, magic)
        gf.check_turn(stats)

run_game()