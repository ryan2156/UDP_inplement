import socket
import json

import sys
import pygame

from models import *
from constants import *

# 連線設定
HOST = 'localhost'
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create a UDP socket

pygame.init()
game_screen = Window()
clock = pygame.time.Clock()
player = Player(50, 50, PLAYER_COLOR)

def main():
    while True:
        game_screen.surface.fill(BACKGROUND_COLOR)
        # 取得所有的Event
        for event in pygame.event.get():
            # 如果event是QUIT，也就是按右上角的x
            if event.type == pygame.QUIT:
                # 將pygame殺掉
                pygame.quit()
                # 終止程式
                sys.exit()
            # 移動
            elif(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
        player.playerCommand()
        
        message = {"type": "command", "command": player.command}
        message_data = json.dumps(message).encode("utf-8")
        client.sendto(message_data, (HOST, PORT))
        player.resetCommand()
        
        player.draw(game_screen.surface)
        # 一直更新pygame的畫面
        
        pygame.display.flip()
        
        clock.tick(1)

if __name__ == "__main__":
    main()