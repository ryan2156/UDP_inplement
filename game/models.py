import pygame
import constants as const

class Window:
    def __init__(self):
        self.width = const.SCREEN_WIDTH
        self.height = const.SCREEN_HEIGHT
        self.surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game")
        self.surface.fill((0, 0, 0))

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
        self.stauts = 1 # 0: 陣亡, 1: 站立, 2: 潛行
        self.radius = const.HIT_BOX
        self.color = color
        self.rect = pygame.Rect(x, y, const.HIT_BOX * 2, const.HIT_BOX * 2)
        
    def draw(self, surface):
        circle_pos = (self.rect.left + self.radius, self.rect.top + self.radius)
        pygame.draw.circle(surface, self.color, circle_pos, self.radius)