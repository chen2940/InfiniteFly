import random
import pygame, config

import Props
from Baseitem import Baseitem
from Bullet import Bullet
from Music import Music


class Plance(Baseitem):
    def __init__(self, left, top):
        # 保存加载的图片
        self.images = {
            'U': pygame.image.load('img/fj/PlanceU.gif'),
            'D': pygame.image.load('img/fj/PlanceD.gif'),
            'L': pygame.image.load('img/fj/PlanceL.gif'),
            'R': pygame.image.load('img/fj/PlanceR.gif'),
        }
        self.direction = 'L'  # 方向
        self.image = self.images[self.direction]  # 根据图片方向获取图片
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()  # 根据图片获取区域
        self.rect.left, self.rect.top = left, top
        self.speed = 0  # 移动速度
        self.stop = True  # 飞机移动开关
        self.live = 1
        self.OldLeft = self.rect.left
        self.OldTop = self.rect.top

    # 移动
    def move(self):
        self.OldLeft = self.rect.left
        self.OldTop = self.rect.top
        # 判断飞机方向进行移动
        if self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
        elif self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
        elif self.direction == 'D':
            if self.rect.top + self.rect.height < config.SCREEN_HEIGHT:
                self.rect.top += self.speed
        elif self.direction == 'R':
            if self.rect.left + self.rect.height < config.SCREEN_WIDTH:
                self.rect.left += self.speed

    # 射击
    def shot(self):
        return Bullet(self)

    def stay(self):
        self.rect.left = self.OldLeft
        self.rect.top = self.OldTop

    def hitWall(self):
        for wall in config.WallList:
            if pygame.sprite.collide_rect(self, wall):
                self.stay()

    # 展示坦克的方法
    def displayPlance(self):
        # 获取展示对象
        self.image = self.images[self.direction]
        # 调用blit展示
        config.window.blit(self.image, self.rect)


class MyPlance(Plance):
    def __init__(self, left, top, speed, live):
        super(MyPlance, self).__init__(left, top)
        self.speed = speed
        self.live = live

    def myplance_hit_enemyplance(self):
        for enemyPlance in config.enemyList:
            if pygame.sprite.collide_rect(self, enemyPlance):
                self.stay()

    def myplance_hit_bossplance(self):
        for boos in config.bosslist:
            if pygame.sprite.collide_rect(self, boos):
                self.stay()

    def MyPlance_hit_HP(self):
        for HP in config.hppropslist:
            if pygame.sprite.collide_rect(self, HP):
                Props.playmusic()
                self.live += 2
                HP.live = False

    def MyPlance_hit_BU(self):
        for BU in config.bupopslist:
            if pygame.sprite.collide_rect(self, BU):
                Props.playmusic()
                config.BulletCount += 3
                BU.live = False

    def MyPlance_hit_Pr(self):
        for Pr in config.prpropsList:
            if pygame.sprite.collide_rect(self, Pr):
                Props.playmusic()
                config.Point += 2
                Pr.live = False


# 敌方飞机
class EnemyPlance(Plance):
    def __init__(self, left, top, speed):
        super(EnemyPlance, self).__init__(left, top)
        # 加载图片集
        self.images = {
            'U': pygame.image.load('img/fj/ePlanceU.gif'),
            'D': pygame.image.load('img/fj/ePlanceD.gif'),
            'L': pygame.image.load('img/fj/ePlanceL.gif'),
            'R': pygame.image.load('img/fj/ePlanceR.gif'),
        }
        # 随机生成方向
        self.direction = self.randDirection()
        self.image = self.images[self.direction]  # 根据方向获取图片
        self.rect = self.image.get_rect()  # 获取区域
        self.rect.left, self.rect.top = left, top  # 对left和top赋值
        self.speed = speed  # 速度
        self.flag = True  # 飞机移动开关
        self.step = 10  # 敌方飞机步数

    def enemyplance_hit_myplance(self):
        if pygame.sprite.collide_rect(self, config.myplance):
            self.stay()

    def randDirection(self):
        nums = random.randint(1, 4)  # 生成1~4的随机整数
        if nums == 1:
            return "U"
        elif nums == 2:
            return "D"
        elif nums == 3:
            return "L"
        elif nums == 4:
            return "R"

    def randMove(self):  # 飞机的随机方向移动
        if self.step < 0:  # 步数小于0, 随机改变方向
            self.direction = self.randDirection()
            self.step = 50  # 步数复位
        else:
            self.move()
            self.step -= 1

    def shot(self):  # 重写shot方法
        num = random.randint(1, 1000)
        if num < 20 or num > 990:
            return Bullet(self)


class Boss(EnemyPlance):
    def __init__(self, left, top):
        self.images = {
            'U': pygame.image.load('img/fj/bossU.gif'),
            'D': pygame.image.load('img/fj/bossD.gif'),
            'L': pygame.image.load('img/fj/bossL.gif'),
            'R': pygame.image.load('img/fj/bossR.gif'),
        }
        self.direction = self.randDirection()
        self.image = self.images[self.direction]  # 根据方向获取图片
        self.rect = self.image.get_rect()  # 获取区域
        self.rect.left, self.rect.top = left, top  # 对left和top赋值
        self.speed = 5  # 速度
        self.flag = True  # 坦克移动开关
        self.step = 10  # 敌方坦克步数
        self.live = 3

    def shot(self):  # 重写shot方法
        num = random.randint(1, 1000)
        if num < 50 or num > 950:
            return Bullet(self)


###
def createMyPlance(left, top, speed, live):  # 初始化我方飞机
    config.myplance = MyPlance(left, top, speed, live)


def createEnemyPlance(top, left):  # 初始化敌方飞机, 将敌方飞机添加到列表中
    for i in range(config.enemyCount):  # 生成指定敌方飞机数量
        aleft = random.randint(0, left)
        speed = random.randint(1, 2)
        enemy = EnemyPlance(aleft, top, speed)
        config.enemyList.append(enemy)


def createBossPlance(top, left):  # 初始化敌方Boss, 将敌方坦克添加到列表中
    aleft = random.randint(0, left)
    boss = Boss(aleft, top)
    config.bosslist.append(boss)


def bilMyPlance():
    if config.myplance and config.myplance.live:
        config.myplance.displayPlance()  # 展 示我方飞机
        if not config.myplance.stop:
            config.myplance.move()  # 调用飞机移动方法
            config.myplance.hitWall()
            config.myplance.myplance_hit_enemyplance()
            config.myplance.myplance_hit_bossplance()
            config.myplance.MyPlance_hit_HP()
            config.myplance.MyPlance_hit_BU()
            config.myplance.MyPlance_hit_Pr()
    else:
        del config.myplance  # 删除我方飞机
        config.myplance = None


def blitEnemyPlance():
    for enemyPlance in config.enemyList:
        if enemyPlance.live:  # 判断敌方飞机状态
            enemyPlance.displayPlance()
            enemyPlance.randMove()  # 调用子弹移动
            enemyPlance.hitWall()
            if config.myplance and config.myplance.live:
                enemyPlance.enemyplance_hit_myplance()
            if len(config.enemyBulletList) < 2:
                enemyBullet = enemyPlance.shot()  # 敌方飞机射击
                if enemyBullet:  # 判断敌方飞机子弹是否为None
                    config.enemyBulletList.append(enemyBullet)  # 存储敌方飞机子弹
        else:
            config.enemyList.remove(enemyPlance)


def blitBossPlance():
    for boss in config.bosslist:
        if boss.live:
            boss.displayPlance()
            boss.randMove()  # 调用子弹移动
            boss.hitWall()
            if config.myplance and config.myplance.live:
                boss.enemyplance_hit_myplance()
            if len(config.enemyBulletList) < 5:
                boosbullet = boss.shot()  # boss射击
                if boosbullet:  # 判断敌方坦克子弹是否为None
                    config.enemyBulletList.append(boosbullet)  # 存储敌方坦克子弹
        else:
            config.bosslist.remove(boss)
