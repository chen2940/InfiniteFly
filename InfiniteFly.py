# 导入模块
import random

import pygame, time, Bullet, Explode, Plance, Wall, config

import Props
from Music import Music


def read():
    with open('img/max.txt', 'r') as file:
        maxMark = file.read()
    return int(maxMark)


def save():
    file = open('mark.txt', 'a')
    file.write(
        f'于{config.t.tm_year}年{config.t.tm_mon}月{config.t.tm_mday}日{config.t.tm_hour}：{config.t.tm_min},游玩成绩为：{config.Point}\n')
    if read() < config.Point:
        fileMAXw = open("img/max.txt", 'w')
        fileMAXw.write(str(config.Point))


class MainGame():
    def __init__(self):
        pass

    # 开始游戏
    def startGame(self):
        pygame.display.init()  # 加载主窗口
        config.window = pygame.display.set_mode([config.SCREEN_WIDTH, config.SCREEN_HEIGHT])  # 设置窗口大小并显示
        Plance.createMyPlance(350, 160, config.MySpeed, config.MyLive)
        # 窗口标题设置
        pygame.display.set_caption("无限飞行" + config.version)
        while True:
            time.sleep(0.02)
            if config.HOME:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        # 退出游戏
                        self.endGame()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.endGame()
                        elif event.key == pygame.K_SPACE:
                            config.START = True
                            config.HOME = False
                        elif event.key == pygame.K_F1:
                            config.HELP = True
                            config.START = False
                            config.HOME = False
                config.window.blit(config.hbackground, (0, 0))
                config.window.blit(
                    self.getTextSuface("按空格键开始游戏", 20, pygame.Color(0, 0, 255)),
                    (330, 350))
                config.window.blit(
                    self.getTextSuface("按F1键查看帮助", 20, pygame.Color(0, 0, 255)),
                    (340, 380))
                pygame.display.update()
            if config.HELP:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        # 退出游戏
                        self.endGame()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.endGame()
                        elif event.key == pygame.K_SPACE:
                            config.START = True
                            config.HELP = False
                pygame.draw.rect(config.window, [0, 0, 0], [0, 0, config.SCREEN_WIDTH, config.SCREEN_HEIGHT], 0)
                config.window.blit(pygame.image.load("img/help.bmp"), (0, 0))
                pygame.display.update()
            if config.START:
                if len(config.WallList) == 0:
                    Wall.createWall(145, 100, 6)
                    Wall.createWall(145, 300, 5)  # 初始化墙壁
                if len(config.enemyList) == 0 and config.enemy:
                    if not config.bosslist:
                        Plance.createEnemyPlance(50, 600)  # 初始化敌方飞机
                        Plance.createEnemyPlance(350, 600)
                        config.BOSS = True
                        config.enemy = False
                if len(config.bosslist) == 0 and config.BOSS :
                    if len(config.enemyList) == 2:
                        Plance.createBossPlance(210, 600)
                        config.enemy = True
                        config.BOSS = False

                config.window.blit(config.background, (0, 0))
                Props.createHPprops()
                Props.createBUprops()
                Props.createPr()
                Props.bilHPprops()
                Props.bilBUprops()
                Props.bilprprops()
                # # 颜色填充
                # config.window.fill(background)
                # 获取事件
                self.getEvent()
                # 绘制文字
                config.window.blit(
                    self.getTextSuface('敌方飞机剩余数量%d' % len(config.enemyList), 16, config.TEXT_COLOR),
                    (10, 10))
                config.window.blit(
                    self.getTextSuface(config.version, 16, config.TEXT_COLOR),
                    (750, 470))
                config.window.blit(
                    self.getTextSuface("X%d" % config.myplance.live, 16, config.TEXT_COLOR),
                    (70, 470))
                # config.window.blit(
                #     self.getTextSuface("X%d" % config.BulletCount, 16, config.TEXT_COLOR),
                #     (70, 430))
                config.window.blit(
                    self.getTextSuface("得分：%d" % config.Point, 20, config.TEXT_COLOR),
                    (420, 10))
                config.window.blit(
                    self.getTextSuface("最高峰分：%d" % read(), 20, config.TEXT_COLOR),
                    (600, 10))
                Plance.bilMyPlance()  #展示我方飞机
                Plance.blitEnemyPlance()  # 展示敌方飞机
                Plance.blitBossPlance()
                Bullet.blitMyBullet()  # 我方飞机子弹
                Bullet.blitEnemyBullet()  # 展示敌方子弹
                Explode.blitExplode()  # 爆炸效果展示
                Wall.blitWall()  # 展示墙壁
                self.StateModel()
                if not config.myplance or not config.myplance.live:
                    config.END = True
                    config.START = False
                pygame.display.update()
            elif config.END:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        # 退出游戏
                        self.endGame()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.endGame()
                self.GameOver()
                pygame.display.update()

    def GameOver(self):
        config.END = True
        config.START = False
        config.O_COLOR = pygame.Color(255, 0, 0)
        config.window.blit(config.ebackground, (0, 0))
        # pygame.draw.rect(config.window, [0, 0, 0], [0, 0, config.SCREEN_WIDTH, config.SCREEN_HEIGHT], 0)
        if config.BulletCount == 0 and len(config.enemyList) > 0:
            config.window.blit(self.getTextSuface("阿？没子弹啦", 20, config.O_COLOR), (325, 230))
        config.window.blit(self.getTextSuface("Game Over", 50, config.O_COLOR), (250, 150))
        config.window.blit(self.getTextSuface("得分：%d" % config.Point, 20, config.O_COLOR), (350, 200))

    # 结束游戏
    def endGame(self):
        save()
        print('游戏结束')
        exit()  # 退出游戏

    # 文字显示
    def getTextSuface(self, text, size, color):
        pygame.font.init()  # 字体初始化
        font = pygame.font.Font('img/msyh.ttc', size)
        # 绘制文字信息
        textSurface = font.render(text, True, color)
        return textSurface

    def StateModel(self):
        for i in range(0, config.BulletCount):
            config.window.blit(pygame.image.load("img/BUc.bmp"), (30 + (i * 25), 425))
        for i in range(0, config.myplance.live):
            config.window.blit(pygame.image.load("img/HPc.bmp"), (30 + (i * 25), 465))

    # 事件获取
    def getEvent(self):
        # 获取所有事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # 退出游戏
                self.endGame()
            # 键盘按键
            if event.type == pygame.KEYDOWN:
                # 上、下、左、右键的判断
                if event.key == pygame.K_LEFT:
                    config.myplance.direction = 'L'
                    config.myplance.stop = False
                elif event.key == pygame.K_RIGHT:
                    config.myplance.direction = 'R'
                    config.myplance.stop = False
                elif event.key == pygame.K_UP:
                    config.myplance.direction = 'U'
                    config.myplance.stop = False
                elif event.key == pygame.K_DOWN:
                    config.myplance.direction = 'D'
                    config.myplance.stop = False
                elif event.key == pygame.K_ESCAPE:
                    self.endGame()
                elif event.key == pygame.K_SPACE:
                    if len(config.myBulletList) < config.BulletCount:  # 可以同时发射子弹数量的上限
                        config.BulletCount -= 1
                        myBullet = Bullet.Bullet(config.myplance)
                        config.myBulletList.append(myBullet)
                        music = Music('img/fire.wav')
                        music.play()
            # 松开键盘, 飞机停止移动
            if event.type == pygame.KEYUP:
                # 只有松开上、下、左、右键时坦克才停止, 松开空格键坦克不停止
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    if config.myplance and config.myplance.live:
                        config.myplance.stop = True


if __name__ == '__main__':
    MainGame().startGame()
