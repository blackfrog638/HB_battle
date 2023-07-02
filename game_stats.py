import pygame

class GameStats():
    #明天别忘了搞resetstat
    def __init__(self):
        """set flags and overall datas in this file"""
        self.mouse_down = False
        self.select_menu = [0,0,0,0,0,0,0,0]
        self.turn = 1
        self.select_action = 0 
        self.able_select = [1,1,1,1,0,0,0,0]
        self.has_acted = [0,0,0,0]