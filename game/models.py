import pygame
from constants import *
import random
import math


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
    def __init__(self, x, y, color) -> None:
        self.player_x = x
        self.player_y = y
        self.player_vx = 0
        self.player_vy = 0
        self.stauts = 1  # 0: 陣亡, 1: 站立, 2: 潛行
        self.radius = HIT_BOX
        self.color = color
        self.rect = pygame.Rect(x, y, HIT_BOX * 2, HIT_BOX * 2)
        self.paint = []  # 墨水位置
        self.bullet = BULLET

    def draw(self, surface):
        circle_pos = (self.rect.left + self.radius, self.rect.top + self.radius)
        pygame.draw.circle(surface, self.color, circle_pos, self.radius)
        if self.paint:
            pygame.draw.circle(surface, self.color, self.paint, self.radius)

    def playerMove(self, key):
        if key[pygame.K_w]:
            self.player_vy -= PLAYER_SPEED
        if key[pygame.K_s]:
            self.player_vy += PLAYER_SPEED
        if key[pygame.K_d]:
            self.player_vx += PLAYER_SPEED
        if key[pygame.K_a]:
            self.player_vx -= PLAYER_SPEED

        self.player_x += self.player_vx
        self.player_y += self.player_vy

        self.rect.x = self.player_x - self.radius  # 更新 rect 的 x 坐标
        self.rect.y = self.player_y - self.radius  # 更新 rect 的 y 坐标

        self.player_vx = 0
        self.player_vy = 0

    def playerFire(self, key):
        if key[pygame.K_SPACE]:
            mouse_x, mouse_y = pygame.mouse.get_pos()  # 獲取滑鼠位置
            rotate = math.atan2(self.player_y - mouse_y, self.player_x - mouse_x)
            R = random.randrange(0, 200)
            angle = random.uniform(-math.radians(30), math.radians(30))
            self.paint = [
                self.player_x - math.cos(rotate + angle) * R,
                self.player_y - math.sin(rotate + angle) * R,
            ]
            random.randrange(0, 200)
            print(
                # mouse_x,
                # mouse_y,
                rotate,
                # self.paint[0],
                # self.paint[1],
                math.cos(rotate),
                math.sin(rotate),
            )
