import sys
import time
import pygame

from models import *

pygame.init()
game_screen = Window()

player = Player(50, 50, (255,255,255))

while True:
    # 取得所有的Event
    for event in pygame.event.get():
        # 如果event是QUIT，也就是按右上角的x
        if event.type == pygame.QUIT:
            # 將pygame殺掉
            pygame.quit()
            # 終止程式
            sys.exit()
    player.draw(game_screen.surface)
    # 一直更新pygame的畫面
    pygame.display.update()
pygame.quit()