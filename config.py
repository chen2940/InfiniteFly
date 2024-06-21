import random
import time

import pygame

t = time.localtime()
version = "V3.0rc5"
RUN = True
SCREEN_WIDTH = 800  # 宽度
SCREEN_HEIGHT = 500  # 高度
BG_COLOR = pygame.Color(0, 0, 0)  # 颜色
TEXT_COLOR = pygame.Color(255, 0, 0)  # 字体颜色
O_COLOR = pygame.Color(255, 255, 255)
scaled_width = 60
scaled_height = 60
Point = 0
background = pygame.image.load("img/back.gif")
hbackground = pygame.image.load("img/home.jpg")
ebackground = pygame.image.load("img/end.jpg")
HOME = True
HELP = False
START = False
END = False
MySpeed = 7
MyLive = 5
enemy = True
BOSS = False

window = None
myplance = None
enemyList = []  # 敌方飞机列表
enemyCount = 5  # 敌方飞机数量
bosslist = []
myBulletList = []  # 我方飞机子弹列表
enemyBulletList = []  # 敌方飞机子弹列表
bossBulletList = []
explodeList = []  # 爆炸效果列表
WallList = []  # 墙壁列表
BulletCount = 6
hppropslist = []
bupopslist = []
prpropsList = []
HPCount = 0
BUCount = 0
Ra = random.randint(1, 3)
