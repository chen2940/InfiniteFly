import pygame, config

from Music import Music


class Explode():
    def __init__(self, Plance):
        self.rect = Plance.rect
        self.images = [
            pygame.image.load('img/blast0.gif'),
            pygame.image.load('img/blast1.gif'),
            pygame.image.load('img/blast2.gif'),
            pygame.image.load('img/blast3.gif'),
            pygame.image.load('img/blast4.gif'),
        ]
        self.step = 0
        self.image = self.images[self.step]
        self.live = True

    # 爆炸效果
    def displayExplode(self):
        if self.step < len(self.images):
            self.image = self.images[self.step]
            self.step += 1
            config.window.blit(self.image, self.rect)  # 添加到主窗口
        else:
            self.live = False
            self.step = 0


def blitExplode():
    for expolde in config.explodeList:
        music = Music("img/music/fire-magic-6947.mp3")
        music.play()
        if expolde.live:
            expolde.displayExplode()
        else:
            config.explodeList.remove(expolde)
