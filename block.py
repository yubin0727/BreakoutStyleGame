import pygame
import sys
import random
import math
import time
from pygame.locals import QUIT

BLACK = (0, 0, 0)
IVORY = (255, 255, 240)
RED = (255, 0, 0)
ORANGE = (255, 140, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
INDIGO = (0, 0, 128)
PURPLE = (162, 35, 236)
PINK = (255, 192, 203)
COLORS = [RED, ORANGE, YELLOW, GREEN, BLUE, INDIGO, PURPLE] # 블록 생성 시 사용
DIFFICULT = ['EASY', 'MEDIUM', 'HARD']
SCREENCOLOR = ['BLACK', 'IVORY']
SCREENSIZE = ['SMALL', 'MEIDUM', 'LARGE']

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
        if(self.rect.centery > sHEIGHT or self.rect.centery < 0):
            self.dir *= -1
        
    def draw(self): # 공 그리기
        pygame.draw.circle(screen, self.color, [self.rect.centerx, self.rect.centery], self.size, 0)
    
    def changeSpeed(self, speed): # 게임 진행 중 속도 조절
        self.speed = speed

class makeR(): # block, paddle 생성 용도
    def __init__(self, color, rect):
        self.color = color
        self.rect = rect
        
    def draw(self): # 사각형 그리기
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 1)
    
class button(): # 시작 메뉴
    def __init__(self, text, loc, total, mode, text_color, fill_color):
        self.text = text
        self.loc = loc
        self.mode = mode
        self.total = total
        self.text_color = text_color
        self.fill_color = fill_color
        font = pygame.font.SysFont("arial", 25)
        self.buttonText = font.render(self.text, True, text_color)
        self.button_rect = self.buttonText.get_rect()
        self.button_rect.centerx = round(sWIDTH / 2)
        self.button_rect.centery = round(sHEIGHT / self.total * self.loc)
        self.click_rect = pygame.Rect(sWIDTH / 6 * 2, self.button_rect.y - 5, sWIDTH / 6 * 2, self.button_rect.height + 10)
        pygame.draw.rect(screen, fill_color, self.click_rect)
        screen.blit(self.buttonText, self.button_rect)                
        
    def click(self):
        mousePos = pygame.mouse.get_pos()
        if self.click_rect.collidepoint(mousePos):
            if pygame.mouse.get_pressed(num_buttons = 3)[0]:
                return self.mode
    
def makeBlock(): # 게임 중 block 추가
    global c, done
    for block in blocks: # 원래 있던 block은 한 줄씩 아래로, 바닥에 닿으면 게임 종료
        block.rect.move_ip(0, sHEIGHT / 16)
        if block.rect.bottom >= sHEIGHT:
            done = True
    for i in range(0, 6): # 새로운 block 생성
        if(random.randint(0, 2) != 1):
            blocks.append(makeR(COLORS[c], pygame.Rect(sWIDTH / 6 * i, 0, sWIDTH / 6, sHEIGHT / 16)))
    c = (c + 6) % 7 
    
def DisplayScore(text_color, text_pos): # 점수 표시
    font = pygame.font.SysFont("arial", 25)
    global score, level
    game_score = font.render(f"Level : {level}  Score : {score}", True, text_color)
    screen.blit(game_score, (0, text_pos))
    
def updateLevel(): # level 상승 
    global score, ball, level, ballspeed, blocktime, mode
    level += 1
    if(ballspeed < 6.5):
        ballspeed += 0.2
        ballspeed = round(ballspeed, 2)
    else:
        ballspeed = 6.5
    ball.changeSpeed(ballspeed)
    if(blocktime > 4):
        blocktime -= 0.3
        blocktime = round(blocktime, 2)
    else:
        blocktime = 4
        
def quitButton(): # X 버튼 또는 ESC -> 종료
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
      
def Game(): # 게임 진행 ~ing
    global blocks, score, remove, level, done, paddlesize, go
    quitButton()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if(paddle.rect.centerx <= - paddlesize / 4): 
            paddle.rect.centerx = - paddlesize / 4
        else:
            paddle.rect.centerx -= 5
    elif keys[pygame.K_RIGHT]:
        if(paddle.rect.centerx >= sWIDTH + paddlesize / 4):
            paddle.rect.centerx = sWIDTH + paddlesize / 4
        else:
            paddle.rect.centerx += 5
    elif keys[pygame.K_ESCAPE]:
        go = True
        done = True
    ball.move()
    if paddle.rect.colliderect(ball.rect): # paddle과 ball 충돌 시
        ball.dir = 270 + int((ball.rect.centerx - paddle.rect.centerx) / paddle.rect.width * 90)
    plen = len(blocks)
    blocks = [x for x in blocks if not x.rect.colliderect(ball.rect)] # 공과 충돌한 블록들 제거 후 남은 블록들
    if(len(blocks) != plen): # 길이가 다르다면 충돌한 블록이 존재한다는 의미
        remove += (plen - len(blocks))
        score += (plen - len(blocks)) * level # 충돌한 블록 수만큼 점수 증가
        ball.dir *= -1 # 공 튕겨나가도록
        if(remove >= 5 * level):
            updateLevel()
        
def initialize(n): # 게임 난이도에 따라...
    global blocks, ball, paddle, score, c, done, ballspeed, paddlesize, blocktime, level, remove, nSize
    if(n == 0):
        ballspeed = 4
        blocktime = 11.5
        paddlesize = int(sWIDTH / 5)
    elif(n == 2):
        ballspeed = 4.8
        blocktime = 8.5
        paddlesize = int(sWIDTH / 7)
    else:
        ballspeed = 4.4
        blocktime = 10
        paddlesize = int(sWIDTH / 6)
        
    blocks = []
    ball = Ball(RED, (sWIDTH - sWIDTH / 70) / 2, sHEIGHT - 15 * (nSize + 1) - sHEIGHT / 40 - sWIDTH / 30, sWIDTH / 70, ballspeed)
    paddle = makeR(YELLOW, pygame.Rect((sWIDTH - paddlesize) / 2, sHEIGHT - 15 * (nSize + 1) - sHEIGHT / 40, paddlesize, sHEIGHT / 40))
    score = 0
    c = 0
    done = False
    level = 1
    remove = 0        
        
pygame.init()
pygame.display.set_caption("BLOCK")
sWIDTH = 700
sHEIGHT = 800
screen = pygame.display.set_mode((sWIDTH, sHEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()
blocks = []
ballspeed = 4.4 # ball 속도
ball = Ball(RED, sWIDTH - sWIDTH / 140, 735, sWIDTH / 70, ballspeed)
paddlesize = sWIDTH / 6 # paddle 크기
paddle = makeR(YELLOW, pygame.Rect(sWIDTH - paddlesize / 2, 750, paddlesize, 20)) 
score = 0 # 점수 계산
c = 0 # 색
done = False
se = False
go = False
blocktime = 4.4 # block 생성 속도
level = 1 # level - 점수 부여
remove = 0 # 제거한 block 수 - 누적
mode = 2 # 1 - easy, 2 - medium, 3 - hard
nDifficult = 1
nColor = 0
nSize = 1

def StartGame(): # 게임 시작 화면 구성
    global done, mode, nDiffiult, se, nColor
    
    screen.fill(SCREENCOLOR[nColor])
    font = pygame.font.SysFont("arial", 50)
    game_name = font.render("Breakout Game", True, ORANGE)
    name_rect = game_name.get_rect()
    name_rect.centerx = round(sWIDTH / 2)
    name_rect.centery = round(sHEIGHT / 8 * 2)
    screen.blit(game_name, name_rect)
    s_start = button("Start", 6, 14, 1, SCREENCOLOR[nColor], SCREENCOLOR[(nColor + 1) % 2])
    s_setting = button("Settings", 8, 14, 2, SCREENCOLOR[nColor], SCREENCOLOR[(nColor + 1) % 2])
    s_exit = button("Exit", 10, 14, 3, SCREENCOLOR[nColor], SCREENCOLOR[(nColor + 1) % 2])
    buttons = []
    buttons.append(s_start)
    buttons.append(s_setting)
    buttons.append(s_exit)
    
    while not done:
        quitButton()
        for i in range(3):
            sbutton = buttons[i]
            mode = sbutton.click()
            if mode:
                time.sleep(0.3)
                if(mode == 1):
                    initialize(nDifficult)
                elif(mode == 2):
                    se = True
                else:
                    pygame.quit()
                    sys.exit()
                done = True
        pygame.display.flip()
        clock.tick(60)

def Menu():
    global se, done, nDifficult, nColor, nSize, sWIDTH, sHEIGHT, screen
   
    screen.fill(SCREENCOLOR[nColor])
    display_difficult = button("- DIFFICULTY -", 3, 17, 0, SCREENCOLOR[(nColor + 1) % 2], SCREENCOLOR[nColor])
    set_difficult = button(DIFFICULT[nDifficult], 4, 17, 1, SCREENCOLOR[nColor], SCREENCOLOR[(nColor + 1) % 2])
    display_color = button("- COLOR -", 6, 17, 0, SCREENCOLOR[(nColor + 1) % 2], SCREENCOLOR[nColor])
    set_color = button(SCREENCOLOR[nColor], 7, 17, 2, SCREENCOLOR[nColor], SCREENCOLOR[(nColor + 1) % 2])
    display_size = button("- SIZE -", 9, 17, 0, SCREENCOLOR[(nColor + 1) % 2], SCREENCOLOR[nColor])
    set_size = button(SCREENSIZE[nSize], 10, 17, 3, SCREENCOLOR[nColor], SCREENCOLOR[(nColor + 1) % 2])
    set_before = button("Before", 13, 17, 4, SCREENCOLOR[nColor], SCREENCOLOR[(nColor + 1) % 2])
    setbuttons = []
    setbuttons.append(set_difficult)
    setbuttons.append(set_color)
    setbuttons.append(set_size)
    setbuttons.append(set_before)
    
    while se:
        quitButton()
        for i in range(4):
            setbutton = setbuttons[i]
            mode = setbutton.click()
            if mode:
                time.sleep(0.2)
                if(mode == 4):
                    se = False
                else:
                    if(mode == 1):
                        nDifficult = (nDifficult + 1) % 3
                        set_difficult = button(DIFFICULT[nDifficult], 4, 17, 1, SCREENCOLOR[nColor], SCREENCOLOR[(nColor + 1) % 2])
                    elif(mode == 2):
                        nColor = (nColor + 1) % 2
                        Menu()
                    elif(mode == 3):
                        nSize = (nSize + 1) % 3
                        if(nSize == 0):
                            sWIDTH = 630
                            sHEIGHT = 720
                        elif(nSize == 1):
                            sWIDTH = 700
                            sHEIGHT = 800
                        else:
                            sWIDTH = 840
                            sHEIGHT = 960
                        screen = pygame.display.set_mode((sWIDTH, sHEIGHT), pygame.RESIZABLE)
                        Menu()
        pygame.display.flip()
        clock.tick(100)
    
    done = False

def main():
    global c, done, blocktime, nSize, go
    done = False
    s = time.time()
    
    for j in range(0, 5):
        for i in range(0, 6):
            if(random.randint(0, 2) != 0):
                blocks.append(makeR(COLORS[c], pygame.Rect(sWIDTH / 6 * i, sHEIGHT / 16 * j, sWIDTH / 6, sHEIGHT / 16)))
        c = (c + 1) % 7
    c = 6
    
    while not done:
        Game()
        e = time.time()
        if((e - s) >= blocktime): 
            s = e
            makeBlock()
        screen.fill(SCREENCOLOR[nColor])
        pygame.draw.line(screen, SCREENCOLOR[(nColor + 1) % 2], [0, sHEIGHT - 15 * (nSize + 1)], [sWIDTH, sHEIGHT - 15 * (nSize + 1)], nSize + 1) 
        DisplayScore(SCREENCOLOR[(nColor + 1) % 2], sHEIGHT - 15 * (nSize + 1))
        ball.draw()
        paddle.draw()
        for block in blocks:
            block.draw()
        pygame.display.flip()
        clock.tick(100)
        if(ball.rect.bottom >= sHEIGHT): # 공 바닥에 닿으면 게임 종료
            done = True
    if not go:
        s = time.time()
        over_time = False
        
        # 2초간 Game Over 표시
        font = pygame.font.SysFont("arial", int(sWIDTH / 14))
        game_over = font.render("Game Over", True, BLACK)
        over_rect = game_over.get_rect()
        over_rect.centerx = round(sWIDTH / 2)
        over_rect.centery = round(sHEIGHT / 2)
        pygame.draw.rect(screen, PINK, pygame.Rect(sWIDTH / 4, over_rect.y - 5, sWIDTH / 2, over_rect.height + 10))
        screen.blit(game_over, over_rect)
        pygame.display.flip()
        
        while not over_time:
            quitButton()
            e = time.time()
            if((e - s) >= 0.5):
                over_time = True
    
    done = False
        
def FinishGame(): # 게임 종료
    global done, score, sWIDTH
    s = time.time()
    score_time = False
    
    while not score_time:
        # 5초간 점수 표시 후 첫 화면으로
        screen.fill(SCREENCOLOR[nColor]) 
        font = pygame.font.SysFont("arial", int(sWIDTH / 14))
        game_score = font.render(f"Score : {score}", True, SCREENCOLOR[(nColor + 1) % 2])
        score_rect = game_score.get_rect()
        score_rect.centerx = round(sWIDTH / 2)
        score_rect.centery = round(sHEIGHT / 3)
        screen.blit(game_score, score_rect)
        pygame.display.flip()
    
        quitButton()
        e = time.time()
        if((e - s) >= 1.5): 
            score_time = True
    
if __name__ == '__main__':
    while not done:
        StartGame()
        if se:
            Menu()
        else:
            main()
            if not go:
                FinishGame()
            go = False