import pygame
from constants import *

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
        self.color = (255,255,255) # white 
        
class Player:
    def __init__(self, x, y, color) -> None:
        self.player_x = x
        self.player_y = y
        self.player_vx = 0
        self.player_vy = 0
        self.stauts = 1 # 0: 陣亡, 1: 站立, 2: 潛行
        self.radius = HIT_BOX
        self.color = color
        self.rect = pygame.Rect(x, y, HIT_BOX * 2, HIT_BOX * 2)
        
    def draw(self, surface):
        circle_pos = (self.rect.left + self.radius, self.rect.top + self.radius)
        pygame.draw.circle(surface, self.color, circle_pos, self.radius)
    def playerMove(self, key: int):
        if(key == pygame.K_w):
            self.player_vy -= PLAYER_SPEED
        if(key == pygame.K_s):
            self.player_vy += PLAYER_SPEED
        if(key == pygame.K_d):
            self.player_vx += PLAYER_SPEED
        if(key == pygame.K_a):
            self.player_vx -= PLAYER_SPEED
        
        self.player_x += self.player_vx
        self.player_y += self.player_vy
        
        self.rect.x = self.player_x  # 更新 rect 的 x 坐标
        self.rect.y = self.player_y  # 更新 rect 的 y 坐标
        
        self.player_vx = 0
        self.player_vy = 0
        print(self.player_x, self.player_y)
        
        