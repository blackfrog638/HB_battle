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

        #队内修正
        self.mp1 = 0
        self.mp2 = 0
        self.half_cost1 = -1
        self.half_cost2 = -1

        #skills
        self.skill_period = 0
        #技能选到第几个人
        self.is_choosing = False
        #是否正在选人（技能）
        self.on_skill = -1
        #正在使用技能的人下标
        self.personlist = []   