import random
import time

import pygame, config

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

class HPprops(Props):
    def __init__(self, left, top):
        super().__init__(left, top)



class BUprops(Props):
    def __init__(self, left, top):
        super().__init__(left, top)



def createHPprops():
    aleft = random.randint(0, 800)
    atop = random.randint(350, 450)
    hp = Props(aleft, atop)
    config.hppropslist.append(hp)


def createBUprops():
    aleft = random.randint(0, 800)
    atop = random.randint(50, 200)
    bu = Props(aleft, atop)
    config.bupopslist.append(bu)


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
