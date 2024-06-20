import pygame

version = "V2.0"
RUN = True
SCREEN_WIDTH = 800  # 宽度
SCREEN_HEIGHT = 500  # 高度
BG_COLOR = pygame.Color(0, 0, 0)  # 颜色
TEXT_COLOR = pygame.Color(255, 0, 0)  # 字体颜色
O_COLOR = pygame.Color(255, 255, 255)
scaled_width = 60
scaled_height = 60

window = None
myplance = None
enemyList = []  # 敌方飞机列表
enemyCount = 5  # 敌方飞机数量
myBulletList = []  # 我方飞机子弹列表
enemyBulletList = []  # 敌方飞机子弹列表
explodeList = []  # 爆炸效果列表
WallList = []  # 墙壁列表
hitTank = 0
