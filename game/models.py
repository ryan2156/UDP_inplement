import pygame
from constants import *
import random
import math
import json


class Window:
    def __init__(self):
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game")
        self.surface.fill(BACKGROUND_COLOR)


class Wall:
    def __init__(self, x, y, length, direct):
        self.wall_x = x
        self.wall_y = y
        self.length = length
        self.direct = direct
        self.color = (255, 255, 255)  # white


class Player:
    def __init__(self, x, y, color, bullet_color) -> None:
        self.player_x = x
        self.player_y = y
        self.player_vx = 0
        self.player_vy = 0
        self.stauts = 1  # 0: 陣亡, 1: 站立, 2: 潛行
        self.radius = HIT_BOX
        self.color = color
        self.bullet_color = bullet_color
        self.rect = pygame.Rect(x, y, HIT_BOX * 2, HIT_BOX * 2)
        self.command = {"wasd": [0, 0, 0, 0], "firing": 0, "mouse": [None, None]}
        self.paint = []  # [X, Y, width, height]
        self.bullet = []
        self.bullet_size = BULLET_SIZE

    def drawBullet(self, surface):
        for bullet in self.paint:
            pygame.draw.rect(surface, self.bullet_color, bullet, 0)

    def drawPlayer(self, surface):
        circle_pos = (self.rect.left + self.radius, self.rect.top + self.radius)
        pygame.draw.circle(surface, self.color, circle_pos, self.radius)

    def playerMove(self, remote, keys=[]):

        # server
        if not remote:
            key = pygame.key.get_pressed()
            if key[pygame.K_w]:
                self.player_vy -= PLAYER_SPEED
            if key[pygame.K_s]:
                self.player_vy += PLAYER_SPEED
            if key[pygame.K_d]:
                self.player_vx += PLAYER_SPEED
            if key[pygame.K_a]:
                self.player_vx -= PLAYER_SPEED
        # client
        else:
            if keys[0]:
                self.player_vy -= PLAYER_SPEED
            if keys[1]:
                self.player_vx -= PLAYER_SPEED
            if keys[2]:
                self.player_vy += PLAYER_SPEED
            if keys[3]:
                self.player_vx += PLAYER_SPEED

        self.player_x += self.player_vx
        self.player_y += self.player_vy

        self.rect.x = self.player_x - self.radius  # 更新 rect 的 x 坐标
        self.rect.y = self.player_y - self.radius  # 更新 rect 的 y 坐标

        self.player_vx = 0
        self.player_vy = 0

    # 下指令：移動、開火
    def playerCommand(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_w]:
            self.command["wasd"][0] = 1
        if key[pygame.K_a]:
            self.command["wasd"][1] = 1
        if key[pygame.K_s]:
            self.command["wasd"][2] = 1
        if key[pygame.K_d]:
            self.command["wasd"][3] = 1

        if key[pygame.K_SPACE]:
            self.command["firing"] = 1
            mouse = pygame.mouse.get_pos()
            self.command["mouse"] = mouse

    def resetCommand(self):
        for i in range(len(self.command["wasd"])):
            self.command["wasd"][i] = 0
        self.command["firing"] = 0
        self.command["mouse"] = [None, None]

    def playerFire(self, remote, keys=[0, [None, None]]):
        # server
        if not remote:
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                mouse_x, mouse_y = pygame.mouse.get_pos()  # 獲取滑鼠位置

                player_mouse_angle = math.atan2(
                    self.player_y - mouse_y, self.player_x - mouse_x
                )  # 玩家與滑鼠夾角
                for i in range(BULLET_SIZE):  # 一次空白多個子彈
                    r = random.randrange(0, MAX_DISTANCE)  # 隨機距離
                    max_angle = math.radians(MAX_ANGLE)  # 隨機角度(扇形的最大角度)
                    angle = random.uniform(
                        player_mouse_angle - max_angle / 2,
                        player_mouse_angle + max_angle / 2,
                    )
                    distance = random.uniform(0, r)  # 隨機距離(增加內層機率)
                    paint = [
                        round(
                            self.player_x - math.cos(angle) * distance, -1
                        ),  # x位置四捨五入到10位
                        round(
                            self.player_y - math.sin(angle) * distance, -1
                        ),  # y位置四捨五入到10位
                        RECT_LENGTH,  # 正方形長
                        RECT_WIDTH,  # 正方形寬
                    ]
                    if paint not in self.paint:
                        self.bullet.append(paint)
                    return paint[:]
        # client
        else:
            if keys[0]:
                mouse_x, mouse_y = keys[1]
                player_mouse_angle = math.atan2(
                    self.player_y - mouse_y, self.player_x - mouse_x
                )  # 玩家與滑鼠夾角
                for i in range(BULLET_SIZE):  # 一次空白多個子彈
                    r = random.randrange(0, MAX_DISTANCE)  # 隨機距離
                    max_angle = math.radians(MAX_ANGLE)  # 隨機角度(扇形的最大角度)
                    angle = random.uniform(
                        player_mouse_angle - max_angle / 2,
                        player_mouse_angle + max_angle / 2,
                    )
                    distance = random.uniform(0, r)  # 隨機距離(增加內層機率)
                    paint = [
                        round(
                            self.player_x - math.cos(angle) * distance, -1
                        ),  # x位置四捨五入到10位
                        round(
                            self.player_y - math.sin(angle) * distance, -1
                        ),  # y位置四捨五入到10位
                        RECT_LENGTH,  # 正方形長
                        RECT_WIDTH,  # 正方形寬
                    ]
                    if paint not in self.paint:
                        self.bullet.append(paint)
                    return paint[:]

    def waitWindow(self, surface):
        font = pygame.font.SysFont("simhei", 24)
        text = font.render("Hello", True, (0, 0, 255), (255, 255, 255))
        surface.blit(text, (320, 240))


class SR:
    def segmentation(data_dict):
        # 將 dict 轉換為 JSON 字符串
        json_str = json.dumps(data_dict)
        # 定義每個封包的大小（以字符為單位）
        packet_size = len(data_dict) / 5 + 1
        # 將 JSON 字符串分割成小封包
        packets = [
            json_str[i : i + packet_size] for i in range(0, len(json_str), packet_size)
        ]
        # 打印每個封包
        for i, packet in enumerate(packets):
            print(f"Packet {i+1}: {packet}")
        # 如果需要將封包重新組合成完整的 JSON 字符串

    def recvDate(packets):
        reconstructed_json_str = "".join(packets)
        # 將 JSON 字符串轉回 dict
        reconstructed_dict = json.loads(reconstructed_json_str)
        print("\nReconstructed Dictionary:")
        print(reconstructed_dict)
        return reconstructed_dict
