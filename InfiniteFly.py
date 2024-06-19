# 导入模块
import pygame, time, Bullet, Explode, Plance, Wall, config
from Music import Music


# 坦克类
class MainGame:

    def __init__(self):
        pass

    # 开始游戏
    def startGame(self):
        pygame.display.init()  # 加载主窗口
        config.window = pygame.display.set_mode([config.SCREEN_WIDTH, config.SCREEN_HEIGHT])  # 设置窗口大小并显示
        Plance.createMyPlance(280, 210)
        background = pygame.image.load("img/back.gif")
        # 窗口标题设置
        pygame.display.set_caption("无限飞行" + config.version)
        while True:
            while config.RUN:
                time.sleep(0.02)
                if len(config.WallList) == 0:
                    Wall.createWall(145, 100, 6)
                    Wall.createWall(145, 300, 5)  # 初始化墙壁
                if len(config.enemyList) == 0:
                    Plance.createEnemyPlance(50, 600)  # 初始化敌方飞机
                    Plance.createEnemyPlance(350, 600)
                config.window.blit(background, (0, 0))
                # # 颜色填充
                # config.window.fill(background)
                # 获取事件
                self.getEvent()
                # 绘制文字
                config.window.blit(
                    self.getTextSuface('敌方坦克剩余数量%d' % len(config.enemyList), 16, config.TEXT_COLOR),
                    (10, 10))
                config.window.blit(
                    self.getTextSuface(config.version, 16, config.TEXT_COLOR),
                    (750, 470))
                config.window.blit(
                    self.getTextSuface("剩余生命：%d"%config.myplance.live, 16, config.TEXT_COLOR),
                    (50, 470))
                if config.myplance and config.myplance.live:
                    config.myplance.displayPlance()  # 展 示我方坦克
                else:
                    del config.myplance  # 删除我方坦克
                    config.myplance = None
                Plance.blitEnemyPlance()  # 展示敌方坦克
                Bullet.blitMyBullet()  # 我方坦克子弹
                Bullet.blitEnemyBullet()  # 展示敌方子弹
                Explode.blitExplode()  # 爆炸效果展示
                Wall.blitWall()  # 展示墙壁
                if config.myplance and config.myplance.live:
                    if not config.myplance.stop:
                        config.myplance.move()  # 调用坦克移动方法
                        config.myplance.hitWall()
                        config.myplance.myplance_hit_enemyplance()
                self.GameOver()
                pygame.display.update()
            while not config.RUN:
                self.GameOver()
                self.getEvent()
                pygame.display.update()

    def GameOver(self):
        if not config.myplance:
            if not config.myplance:
                config.O_COLOR = pygame.Color(255, 0, 0)
            pygame.draw.rect(config.window, [0, 0, 0], [0, 0, config.SCREEN_WIDTH, config.SCREEN_HEIGHT], 0)
            config.window.blit(self.getTextSuface("Game Over", 50, config.O_COLOR), (300, 150))
            config.window.blit(self.getTextSuface("击杀数量：%d" % config.hitTank, 20, config.O_COLOR), (350, 200))
            config.RUN = False

    # 结束游戏
    def endGame(self):
        print('游戏结束')
        exit()  # 退出游戏

    # 文字显示
    def getTextSuface(self, text, size, color):
        pygame.font.init()  # 字体初始化
        font = pygame.font.SysFont('kaiti', size)
        # 绘制文字信息
        textSurface = font.render(text, True, color)
        return textSurface

    # 事件获取
    def getEvent(self):
        # 获取所有事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # 退出游戏
                self.endGame()
            # 键盘按键
            if event.type == pygame.KEYDOWN:
                if not config.myplance:  # 当我方坦克不存在时, 按下Esc键重生
                    if event.key == pygame.K_p:
                        Plance.createMyPlance()
                if config.myplance and config.myplance.live:
                    # 上、下、左、右键的判断
                    if event.key == pygame.K_LEFT:
                        config.myplance.direction = 'L'
                        config.myplance.stop = False
                        print('左键,')
                    elif event.key == pygame.K_RIGHT:
                        config.myplance.direction = 'R'
                        config.myplance.stop = False
                        print('右键,')
                    elif event.key == pygame.K_UP:
                        config.myplance.direction = 'U'
                        config.myplance.stop = False
                        print('上键,')
                    elif event.key == pygame.K_DOWN:
                        config.myplance.direction = 'D'
                        config.myplance.stop = False
                        print('下键, ')
                    elif event.key == pygame.K_ESCAPE:
                        self.endGame()
                    elif event.key == pygame.K_SPACE:
                        print('发射子弹')
                        if len(config.myBulletList) < 3:  # 可以同时发射子弹数量的上限
                            myBullet = Bullet.Bullet(config.myplance)
                            config.myBulletList.append(myBullet)
                            music = Music('img/fire.wav')
                            music.play()
            # 松开键盘, 坦克停止移动
            if event.type == pygame.KEYUP:
                # 只有松开上、下、左、右键时坦克才停止, 松开空格键坦克不停止
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    if config.myplance and config.myplance.live:
                        config.myplance.stop = True


if __name__ == '__main__':
    MainGame().startGame()
