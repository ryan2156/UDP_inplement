import socket  # 用於網絡通信
import time  # 用於計時和倒計時
import pygame  # 用於圖形界面
import eventlet
from models import *
import sys


def connect_to_server(client_socket, server_host, server_port):
    """
    與伺服器建立連接並等待開始時間
    """
    client_socket.connect((server_host, server_port))
    client_socket.send(b"connect")
    print("等待伺服器開始遊戲...")

    while True:
        data = client_socket.recv(4096)
        if data.startswith(b"start_at:"):
            start_time = float(data.split(b":")[1])
            print("遊戲將於", start_time, "開始")

            # 通知伺服器已準備好
            client_socket.send(b"ready")
            return start_time


def wait_for_game_start(screen, font, start_time):
    """
    繪製倒計時畫面並等待遊戲開始
    """
    while time.time() < start_time:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # 繪製倒計時畫面
        screen.fill((0, 0, 0))  # 填充背景為黑色
        countdown = int(start_time - time.time())  # 計算剩餘時間
        countdown_text = font.render(
            f"遊戲將於 {countdown} 秒後開始", True, (255, 255, 255)
        )  # 創建倒計時文字
        screen.blit(countdown_text, (100, 250))  # 將文字繪製到屏幕上
        pygame.display.flip()  # 更新屏幕顯示
        time.sleep(0.1)  # 休眠0.1秒

    print("遊戲開始！")


def game_loop(screen, small_font):
    """
    遊戲進行中的主循環
    """
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # 遊戲開始後的畫面
        screen.fill((0, 0, 0))  # 填充背景為黑色
        game_text = small_font.render(
            "遊戲進行中...", True, (255, 255, 255)
        )  # 創建遊戲進行中的文字
        screen.blit(game_text, (350, 300))  # 將文字繪製到屏幕上
        pygame.display.flip()  # 更新屏幕顯示
        time.sleep(0.1)  # 休眠0.1秒


server_host = "127.0.0.1"
server_port = 12345
# 函數逾時設定
eventlet.monkey_patch()
# 創建一個UDP客戶端socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

pygame.init()
game_screen = Window()
clock = pygame.time.Clock()
player_server = Player(50, 50, PLAYER_COLOR_1, BULLET_COLOR_1)
player_client = Player(100, 100, PLAYER_COLOR_2, BULLET_COLOR_2)
# 設置窗口標題
pygame.display.set_caption("等待開始")
# 設置字體大小
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# 與伺服器建立連接並獲取開始時間
start_time = connect_to_server(client_socket, server_host, server_port)

# 繪製等待畫面
game_screen.surface.fill((0, 0, 0))  # 填充背景為黑色
text = font.render("等待伺服器開始遊戲...", True, (255, 255, 255))  # 創建等待文字
game_screen.surface.blit(text, (100, 250))  # 將文字繪製到屏幕上
pygame.display.flip()  # 更新屏幕顯示

# 等待遊戲開始
wait_for_game_start(game_screen.surface, font, start_time)

while True:
    start = time.time()
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
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # 下指令
    player_client.playerCommand()

    message = {"type": "command", "command": player_client.command}
    message_data = json.dumps(message).encode("utf-8")
    client_socket.send(message_data)
    player_client.resetCommand()

    # 收到來自伺服器的回覆
    with eventlet.Timeout(TIMEOUT, False):
        response = client_socket.recv(1024)
        print(response)
        response = json.loads(response.decode("utf-8"))
        if response["type"] == "status":
            player_server.player_x = response["player_server"][0]
            player_server.rect.x = player_server.player_x

            player_server.player_y = response["player_server"][1]
            player_server.rect.y = player_server.player_y

            # print("Server says:", player_server.paint)
            if response["player_server"][2]:
                player_server.paint.append(response["player_server"][2])

            player_client.player_x = response["player_client"][0]
            player_client.rect.x = player_client.player_x

            player_client.player_y = response["player_client"][1]
            player_client.rect.y = player_client.player_y

            # print("Client says:", response["player_client"][2])
            if response["player_client"][2]:
                player_client.paint.append(response["player_client"][2])

    # 將角色的狀態更新
    player_client.drawBullet(game_screen.surface)
    player_server.drawBullet(game_screen.surface)
    player_client.drawPlayer(game_screen.surface)
    player_server.drawPlayer(game_screen.surface)
    # for i in range(len(player_client.paint)):
    #     print(player_client.paint[i])
    # print("...................")
    # 更新pygame的畫面
    pygame.display.flip()

    clock.tick(FRAMN)
