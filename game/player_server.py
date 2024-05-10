import socket
import json

import sys
import pygame
import eventlet
eventlet.monkey_patch()

from models import *
from constants import *

# 連線設定
HOST = 'localhost'
PORT = 5000
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create a UDP socket
server.bind((HOST, PORT))  # Bind the socket to the host and port

# 遊戲初始化
pygame.init()
game_screen = Window()
clock = pygame.time.Clock()
player_server = Player(50, 50, PLAYER_COLOR_1)
player_client = Player(100, 100, PLAYER_COLOR_2)

def main():
    while True:
        game_screen.surface.fill(BACKGROUND_COLOR)
        
        
        # # 從client 取得事件
        with eventlet.Timeout(TIMEOUT, False):
            data, addr = server.recvfrom(1024)
            data = json.loads(data.decode("utf-8"))
            client_command = data["command"]
        
        
        # 取得所有的Event
        for event in pygame.event.get():
            # 如果event是QUIT，也就是按右上角的x
            if event.type == pygame.QUIT:
                # 將pygame殺掉
                pygame.quit()
                # 終止程式
                sys.exit()
            # 離開
            elif(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
        
        # # 移動
        player_server.playerMove(remote = 0)
        try:
            player_client.playerMove(remote = 1, keys = data["command"]["wasd"])
            print(f"Client says: {client_command}")
        except:
            pass
        

        # 回傳角色狀態
        status = {
            "type": "status",
            "player_server": [player_server.player_x, player_server.player_y],
            "player_client": [player_client.player_x, player_client.player_y],
        }
        
        status_data = json.dumps(status).encode("utf-8")
        try:
            server.sendto(status_data, addr)
        except:
            pass
        # 更新狀態
        player_server.draw(game_screen.surface)
        player_client.draw(game_screen.surface)
        # 一直更新pygame的畫面
        
        pygame.display.flip()
        
        clock.tick(FRAMN)

if __name__ == "__main__":
    main()