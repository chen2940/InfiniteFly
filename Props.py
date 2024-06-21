import random, time, pygame, config

import Plance
from Baseitem import Baseitem


class Props(Baseitem):
    def __init__(self, left, top):
        self.image = pygame.image.load("img/props.bmp")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = left, top
        self.live = True

    def displayhpprops(self):
        if self.live:
            self.image = pygame.image.load("img/hp.bmp")
            config.window.blit(self.image, self.rect)

    def displaybuprops(self):
        if self.live:
            self.image = pygame.image.load("img/bullet.bmp")
            config.window.blit(self.image, self.rect)

    def displayprprops(self):
        if self.live:
            self.image = pygame.image.load("img/pr.bmp")
            config.window.blit(self.image, self.rect)


class HPprops(Props):
    def __init__(self, left, top):
        super().__init__(left, top)


class BUprops(Props):
    def __init__(self, left, top):
        super().__init__(left, top)


class Pr(Props):
    def __init__(self, lefy, top, left):
        super().__init__(left, top)


def createHPprops():
    if len(config.hppropslist) == 0 and config.myplance.live == config.Ra:
        aleft = random.randint(0, 750)
        atop = random.randint(350, 450)
        hp = Props(aleft, atop)
        config.hppropslist.append(hp)


def createBUprops():
    if len(config.bupopslist) == 0 and config.BulletCount == config.Ra:
        aleft = random.randint(0, 750)
        atop = random.randint(50, 200)
        bu = Props(aleft, atop)
        config.bupopslist.append(bu)


def createPr():
    if len(config.prpropsList) == 0:
        if config.myplance.live == config.Ra and config.BulletCount == config.Ra:
            aleft = random.randint(0, 750)
            atop = random.randint(50, 200)
            pr = Props(aleft, atop)
            config.prpropsList.append(pr)


def bilHPprops():
    for hp in config.hppropslist:
        if hp.live:
            hp.displayhpprops()
        else:
            config.hppropslist.remove(hp)


def bilBUprops():
    for hp in config.bupopslist:
        if hp.live:
            hp.displaybuprops()
        else:
            config.bupopslist.remove(hp)

def bilprprops():
    for pr in config.prpropsList:
        if pr.live:
            pr.displayprprops()
        else:
            config.prpropsList.remove(pr)

