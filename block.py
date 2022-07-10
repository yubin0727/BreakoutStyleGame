# -*- coding: utf-8 -*-

import pygame
import sys
import random
import math
from pygame.locals import QUIT, KEYDOWN, K_LEFT, K_RIGHT

sWIDTH = 700
sHEIGHT = 800
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 140, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
INDIGO = (0, 0, 128)
PURPLE = (162, 35, 236)


class Ball(): # 공 생성, 움직임 조절
    def __init__(self, color, ball_x, ball_y, size, speed):
        self.color = color
        self.rect = pygame.Rect(ball_x, ball_y, size, size)
        self.size = size
        self.speed = speed
        self.dir = random.randint(30, 150) + 180
        
    def move(self): # 공 움직임, 벽과 충돌했을 때 방향 조절
        dx = math.cos(math.radians(self.dir))
        dy = math.sin(math.radians(self.dir))
        self.rect.centerx = self.rect.centerx + dx * self.speed
        self.rect.centery = self.rect.centery + dy * self.speed
        if(self.rect.centerx > sWIDTH or self.rect.centerx < 0):
            self.dir = 180 - self.dir
        if(self.rect.centery > sHEIGHT or self.rect.centery < 0): # 조건 수정
            self.dir *= -1
        
    def draw(self): # 공 그리기
        pygame.draw.circle(screen, self.color, [self.rect.centerx, self.rect.centery], self.size, 0)
    
    def changeSpeed(self, speed): #나중에 속도 조절
        self.speed = speed

class Block(): # block, paddle 생성 용도
    def __init__(self, color, rect):
        self.color = color
        self.rect = rect
        
    def draw(self): # 사각형 그리기
        pygame.draw.rect(screen, self.color, self.rect)
      
def Game(): # 게임 진행 ~ing
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN: # 키보드 누를 때마다 paddle 이동
            # 계속 누르고 있어도 움직이도록 바꾸기 - get_pressed()
            if event.key == K_LEFT: # <- 키보드 입력 : paddle 왼쪽으로 이동
                if(paddle.rect.centerx <= 20): 
                    paddle.rect.centerx = 20
                else:
                    paddle.rect.centerx -= 10
            elif event.key == K_RIGHT: # -> 키보드 입력 : paddle 오른쪽으로 이동
                if(paddle.rect.centerx >= sWIDTH - 20):
                    paddle.rect.centerx = sWIDTH - 20
                else:
                    paddle.rect.centerx += 10
    ball.move()
    if paddle.rect.colliderect(ball.rect):
        ball.dir = random.randint(30, 150) + 180
    
    
# 블록과 공 충돌했을 때 -> 블록 없어지고, 공은 튕기도록
    
pygame.init()
pygame.display.set_caption("BLOCK")
screen = pygame.display.set_mode((sWIDTH, sHEIGHT))
clock = pygame.time.Clock()
blocks = []
ball = Ball(RED, 345, 735, 10, 5)
paddle = Block(YELLOW, pygame.Rect(310, 750, 200, 20)) # 사이즈 줄이기 200 -> ?

def main():
    done = False

    while not done:
        Game()
        screen.fill(BLACK) # 이거 안하면 화면에 누적되어 표시됨
        pygame.draw.line(screen, WHITE, [0, 770], [700, 770], 2) 
        ball.draw()
        paddle.draw()
        pygame.display.flip()
        clock.tick(100)
        
if __name__ == '__main__':
    main()