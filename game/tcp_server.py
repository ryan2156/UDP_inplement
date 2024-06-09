import socket
import time
import pygame
from models import *
import eventlet
import sys


def accept_clients(server_socket, num_clients=1):
    """
    接受指定數量的客戶端連接
    """
    clients = []

    print(f"伺服器啟動，等待玩家連線...")

    while len(clients) < num_clients:
        server_socket.settimeout(0.01)
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            client, addr = server_socket.accept()
            if client not in clients:
                clients.append(client)
                print(f"玩家 {client} 已連線")
        except:
            pass
    return clients


def notify_clients_start(server_socket, clients, delay=5):
    """
    通知所有客戶端遊戲開始時間
    """
    start_time = time.time() + delay  # 設置開始時間
    for client in clients:
        client.send(f"start_at:{start_time}".encode())

    print("所有玩家已連線，遊戲即將開始於", start_time)
    return start_time


def wait_for_clients_ready(server_socket, clients):
    """
    等待所有客戶端確認準備好
    """
    ready_clients = []
    while len(ready_clients) < len(clients):
        for client in clients:
            data = client.recv(1024)
            if data == b"ready" and client not in ready_clients:
                ready_clients.append(client)
                print(f"玩家 {client} 準備好了")

    print("所有玩家已準備，遊戲開始！")


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


host = "127.0.0.1"
port = 12345
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(5)

# 遊戲初始化
pygame.init()
game_screen = Window()
clock = pygame.time.Clock()
player_server = Player(50, 50, PLAYER_COLOR_1, BULLET_COLOR_1)
player_client = Player(100, 100, PLAYER_COLOR_2, BULLET_COLOR_2)


# 設置字體大小
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)
# 繪製等待畫面
game_screen.surface.fill((0, 0, 0))  # 填充背景為黑色
text = font.render("等待伺服器開始遊戲...", True, (255, 255, 255))  # 創建等待文字
game_screen.surface.blit(text, (100, 250))  # 將文字繪製到屏幕上
pygame.display.flip()  # 更新屏幕顯示

clients = accept_clients(server_socket)  # 接受客戶端連接
start_time = notify_clients_start(server_socket, clients)  # 通知客戶端遊戲開始時間
wait_for_clients_ready(server_socket, clients)  # 等待所有客戶端準備好

# 等待遊戲開始
wait_for_game_start(game_screen.surface, font, start_time)

while True:

    game_screen.surface.fill(BACKGROUND_COLOR)

    # 從client 取得事件
    with eventlet.Timeout(TIMEOUT, False):
        for client in clients:
            data = client.recv(1024)
            print(data)
            # 將 bytes 資料轉為字串
            data_str = data.decode("utf-8")
            # 分割字串，根據每個獨立的 JSON 物件
            json_strings = [json_str for json_str in data_str.split("}{")]
            # 修復分割後的字串，使其成為有效的 JSON
            if len(json_strings) > 1:
                json_strings[0] += "}"
            data = json.loads(json_strings[0])
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
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
    # 移動
    player_server.playerMove(remote=0)

    # 開火
    bullet_server = player_server.playerFire(remote=0)

    # client
    bullet_client = [None, None]
    try:
        player_client.playerMove(remote=1, keys=client_command["wasd"])
        # print(client_command["mouse"])
        fire = [client_command["firing"], client_command["mouse"]]

        bullet_client = player_client.playerFire(remote=1, keys=fire)

        # print(f"Client says: {client_command}")
    except:
        # print("fail")
        pass

    # 回傳角色狀態
    status = {
        "type": "status",
        "player_server": [
            player_server.player_x,
            player_server.player_y,
            bullet_server,
        ],
        "player_client": [
            player_client.player_x,
            player_client.player_y,
            bullet_client,
        ],
    }

    status_data = json.dumps(status).encode("utf-8")
    try:
        for client in clients:
            client.send(status_data)
    except:
        pass
    # 更新狀態
    player_server.drawBullet(game_screen.surface)
    player_client.drawBullet(game_screen.surface)
    player_server.drawPlayer(game_screen.surface)
    player_client.drawPlayer(game_screen.surface)
    # for i in range(len(player_client.paint)):
    #     print(player_client.paint[i])
    # print("...................")
    # 一直更新pygame的畫面
    pygame.display.flip()

    clock.tick(FRAMN)
