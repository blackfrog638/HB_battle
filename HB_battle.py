import pygame
from pygame.sprite import Sprite,Group

from game_stats import GameStats
from settings import Settings
from hero import Hero
from actions import Nor_atk
import game_function as gf

def run_game():
    pygame.init()
    ai_settings = Settings()
    stats = GameStats()
    screen = pygame.display.set_mode((ai_settings.screen_wid,ai_settings.screen_hgt))
    nor_atk = Nor_atk(ai_settings, screen)
    pygame.display.set_caption("HB_battle")

    while True:
        heroes = Group()
        gf.update_screen(ai_settings, screen, heroes, nor_atk)
        gf.check_events(stats, heroes)
        
run_game()