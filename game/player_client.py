import socket
import json

import sys
import pygame
import eventlet

from models import *
from constants import *

# 連線設定
HOST = 'localhost'
PORT = 5000

# 函數逾時設定
eventlet.monkey_patch()

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create a UDP socket

pygame.init()
game_screen = Window()
clock = pygame.time.Clock()
player_server = Player(50, 50, PLAYER_COLOR_1, BULLET_COLOR_1)
player_client = Player(100, 100, PLAYER_COLOR_2, BULLET_COLOR_2)


def main():
    
    while True:
        game_screen.surface.fill(BACKGROUND_COLOR)
        
        # 處理暫停、關遊戲
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
        
        # 下指令
        player_client.playerCommand()
        
        message = {"type": "command", "command": player_client.command}
        message_data = json.dumps(message).encode("utf-8")
        client.sendto(message_data, (HOST, PORT))
        player_client.resetCommand()
        
        # 收到來自伺服器的回覆
        with eventlet.Timeout(TIMEOUT, False):
            response, addr = client.recvfrom(1024)
            response = json.loads(response.decode("utf-8"))
            if(response["type"] == "status"):
                player_server.player_x = response["player_server"][0]
                player_server.rect.x = player_server.player_x
                
                player_server.player_y = response["player_server"][1]
                player_server.rect.y = player_server.player_y
                
                # print("Server says:", player_server.paint)
                if(response["player_server"][2]):
                    player_server.paint.append(response["player_server"][2])
                
                player_client.player_x = response["player_client"][0]
                player_client.rect.x = player_client.player_x
                
                player_client.player_y = response["player_client"][1]
                player_client.rect.y = player_client.player_y
                
                # print("Client says:", response["player_client"][2])
                if(response["player_client"][2]):
                    player_client.paint.append(response["player_client"][2])
        
        # 將角色的狀態更新
        player_server.draw(game_screen.surface)
        player_client.draw(game_screen.surface)
        # 更新pygame的畫面
        pygame.display.flip()
        
        clock.tick(FRAMN)

if __name__ == "__main__":
    main()