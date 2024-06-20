import random
import pygame, config
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
        self.speed = 5  # 移动速度
        self.stop = True  # 飞机移动开关
        self.live = 5
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
    def __init__(self, left, top):
        super(MyPlance, self).__init__(left, top)

    def myplance_hit_enemyplance(self):
        for enemyPlance in config.enemyList:
            if pygame.sprite.collide_rect(self, enemyPlance):
                self.stay()

    def MyPlance_hit_HP(self):
        for HP in config.hppropslist:
            if pygame.sprite.collide_rect(self, HP):
                self.live += 1
                HP.live = False
                self.stay()
    def MyPlance_hit_BU(self):
        for BU in config.bupopslist:
            if pygame.sprite.collide_rect(self, BU):
                self.live += 1
                BU.live = False
                self.stay()


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


###
def createMyPlance(left, top):  # 初始化我方飞机
    config.myplance = MyPlance(left, top)
    music = Music('img/start.wav')  # 创建音乐对象
    music.play()  # 播放音乐


def createEnemyPlance(top, left):  # 初始化敌方飞机, 将敌方飞机添加到列表中
    for i in range(config.enemyCount):  # 生成指定敌方飞机数量
        aleft = random.randint(0, left)
        speed = random.randint(1, 4)
        enemy = EnemyPlance(aleft, top, speed)
        config.enemyList.append(enemy)

def bilMyPlance():
    if config.myplance and config.myplance.live:
        if not config.myplance.stop:
            config.myplance.move()  # 调用飞机移动方法
            config.myplance.hitWall()
            config.myplance.myplance_hit_enemyplance()
            config.myplance.MyPlance_hit_HP()
            config.myplance.MyPlance_hit_BU()

def blitEnemyPlance():
    if config.myplance and config.myplance.live:
        config.myplance.displayPlance()  # 展 示我方飞机
    else:
        del config.myplance  # 删除我方飞机
        config.myplance = None
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
