import math 
import random 
import sqlite3 
import pygame
from pygame import mixer

#pygame
pygame.init() 
con = sqlite3.connect(r"project.db") 

   #screen
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
#Background
background = pygame.image.load('wall (1).png') 
background_intro = pygame.image.load('intro wall (7).png') 

# Sound
mixer.music.load("love.mp3") 
mixer.music.play() 

# Caption and Icon
pygame.display.set_caption("Sky Attack") 
icon = pygame.image.load('penguin.png') 
pygame.display.set_icon(icon) 

# Player
playerImg = pygame.image.load('teacher.png') 
playerX = 350  
playerY = 500
playerX_change = 0 

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 8 
enemyVelocity = [3,3,3,3,3,3,3,3] 
enemyPic = {
    0 : 'baimon2.png',
    1 : 'anutep.png',
    2 : 'noona.png',
    3 : 'nuknik.png',
    4 : 'neena.png',
    5 : 'meteorite(ลดคะเเนน).png',
    6 : 'meteorite(ลดคะเเนน).png',
    7 : 'meteorite(ลดคะเเนน).png'
    }
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load(enemyPic[i]))
    enemyX.append(random.randint(0, 736)) 
    enemyY.append(random.randint(150, 150)) 
    enemyX_change.append(2) 
    enemyY_change.append(20) 

# Bullet
bulletImg = pygame.image.load('a-plus-test-result-of-school (1).png') 
bulletX = 400 
bulletY = 480 
bulletY_change = 15 
bullet_state = "ready"

# Score

score_value = 0 
font = pygame.font.Font('freesansbold.ttf', 32) 

textX = 10 
textY = 10 

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64) 

# scoreboard
over_scoreboard = pygame.font.Font('freesansbold.ttf', 32)
scoreboard = [['','',''],['','',''],['','',''],['','',''],['','','']]
savescore = 1

# USERNAME
intro = 1
username = ''

active_color = pygame.Color('dodgerblue2')
inactive_color = pygame.Color('white')

textAlignLeft = 0
textAlignRight = 1
textAlignCenter = 2
textAlignBlock = 3



def drawText(surface, text, color, rect, font, align=textAlignLeft, aa=False, bkg=None):
    lineSpacing = -2
    spaceWidth, fontHeight = font.size(" ")[0], font.size("Tg")[1]

    listOfWords = text.split(" ")
    if bkg:
        imageList = [font.render(word, 1, color, bkg) for word in listOfWords]
        for image in imageList: image.set_colorkey(bkg)
    else:
        imageList = [font.render(word, aa, color) for word in listOfWords]

    maxLen = rect[2]
    lineLenList = [0]
    lineList = [[]]
    for image in imageList:
        width = image.get_width()
        lineLen = lineLenList[-1] + len(lineList[-1]) * spaceWidth + width
        if len(lineList[-1]) == 0 or lineLen <= maxLen:
            lineLenList[-1] += width
            lineList[-1].append(image)
        else:
            lineLenList.append(width)
            lineList.append([image])

    lineBottom = rect[1]
    lastLine = 0
    for lineLen, lineImages in zip(lineLenList, lineList):
        lineLeft = rect[0]
        if align == textAlignRight:
            lineLeft += + rect[2] - lineLen - spaceWidth * (len(lineImages) - 1)
        elif align == textAlignCenter:
            lineLeft += (rect[2] - lineLen - spaceWidth * (len(lineImages) - 1)) // 2
        elif align == textAlignBlock and len(lineImages) > 1:
            spaceWidth = (rect[2] - lineLen) // (len(lineImages) - 1)
        if lineBottom + fontHeight > rect[1] + rect[3]:
            break
        lastLine += 1
        for i, image in enumerate(lineImages):
            x, y = lineLeft + i * spaceWidth, lineBottom
            surface.blit(image, (round(x), y))
            lineLeft += image.get_width()
        lineBottom += fontHeight + lineSpacing

    if lastLine < len(lineList):
        drawWords = sum([len(lineList[i]) for i in range(lastLine)])
        remainingText = ""
        for text in listOfWords[drawWords:]: remainingText += text + " "
        return remainingText
    return ""


class InputBox():
    def __init__(self, max_len, x, y, width, height, text=''):
        self.color = inactive_color
        self.len = max_len
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.text_surf = font.render(text, True, self.color)
        self.active = False


    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active

        self.color = active_color if self.active else inactive_color

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    global intro
                    intro = 0
                    print(intro)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                    global username
                    username = self.text

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 1)
        drawTextRect = self.rect.inflate(-5, -5)
        drawText(screen, self.text, self.color, drawTextRect, font, textAlignLeft, True)

    def update(self):
        pass


def show_score(x, y): 
    score2 = font.render("Username : " + username , True, (0, 76, 153))
    score = font.render("Score : " + str(score_value), True, (0, 76, 153))
    screen.blit(score2, (10,10)) 
    screen.blit(score, (10,50))

def game_over_text():
    global savescore
    if savescore == 1 :
        savescore = 0
        cmd2 = f"""INSERT INTO scoregame(score,username)
         VALUES ("{score_value}","{username}")"""
        con.execute(cmd2) 
        con.commit() 
    over_text = over_font.render("GAME OVER", True, (255, 255, 255)) 
    screen.blit(over_text, (200,70)) 
    over_text = over_font.render("TOP 5", True,(0, 0, 0)) 
    screen.blit(over_text, (300, 150)) 

    #scoreboard TOP5
    cmd = """SELECT * FROM scoregame WHERE username!='' ORDER BY score DESC LIMIT 5 """ 
    loop = 1
    rows = con.execute(cmd)
    for rows in con.execute(cmd):
        if loop == 1 :
            scoreboard[0]=[rows[0],rows[1],rows[2]]
        if loop == 2 :
            scoreboard[1]=[rows[0],rows[1],rows[2]]
        if loop == 3 :
            scoreboard[2]=[rows[0],rows[1],rows[2]]
        if loop == 4 :
            scoreboard[3]=[rows[0],rows[1],rows[2]]
        if loop == 5 :
            scoreboard[4]=[rows[0],rows[1],rows[2]]
        loop=loop+1
    scoreboard_text1 = over_scoreboard.render("No.1 SCORE "+str(scoreboard[0][2])+" --> "+str(scoreboard[0][1]), True,(0, 0, 0)) 
    screen.blit(scoreboard_text1, (200, 220)) 
    scoreboard_text2 = over_scoreboard.render("No.2 SCORE " + str(scoreboard[1][2]) + " --> " + str(scoreboard[1][1]), True,(0, 0, 0)) 
    screen.blit(scoreboard_text2, (200, 270)) 
    scoreboard_text3 = over_scoreboard.render("No.3 SCORE " + str(scoreboard[2][2]) + " --> " + str(scoreboard[2][1]), True,(0, 0, 0)) 
    screen.blit(scoreboard_text3, (200, 320)) 
    scoreboard_text4 = over_scoreboard.render("No.4 SCORE " + str(scoreboard[3][2]) + " --> " + str(scoreboard[3][1]), True,(0, 0, 0)) 
    screen.blit(scoreboard_text4, (200, 370)) 
    scoreboard_text5 = over_scoreboard.render("No.5 SCORE " + str(scoreboard[4][2]) + " --> " + str(scoreboard[4][1]), True,(0, 0, 0)) 
    screen.blit(scoreboard_text5, (200, 420)) 


def player(x, y):
    screen.blit(playerImg, (x, y)) 


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def heart_bullet(x, y):
    global bullet_state 
    bullet_state = "GradeA"  
    screen.blit(bulletImg, (x + 16, y + 10)) 

def isCollision(enemyX, enemyY, bulletX, bulletY): 
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 50: 
        return True 
    else:
        return False 


# Game Loop
inputbox = InputBox(15,250,100,300,70)
running = True 
while running:
    screen.fill((255,255,255))
    # Background Image
    screen.blit(background, (0, 0))  
    if intro == 1:
        screen.blit(background_intro, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            inputbox.event_handler(event)

        inputbox.update()
        inputbox.draw(screen)
        pygame.display.update()
        pygame.time.Clock().tick(60)


    if intro == 0:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                running = False 
                game_over_text()
            # if keystroke is pressed check whether its right or left
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_LEFT: 
                    playerX_change = -2
                if event.key == pygame.K_RIGHT: 
                    playerX_change = 2
                if event.key == pygame.K_SPACE: 
                    if bullet_state == "ready": 
                        bulletSound = mixer.Sound("laser.wav")  
                        bulletSound.play()  
                        bulletX = playerX 
                        heart_bullet(bulletX, bulletY) 
                if event.key == pygame.K_DOWN : #ปิดเสียง
                    pygame.mixer.music.pause()
                if event.key == pygame.K_UP : #เปิดเสียง
                    pygame.mixer.music.unpause()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0 

        playerX += playerX_change 
        if playerX <= 0:
            playerX = 0
        elif playerX >= 750:
            playerX = 750
       
        #การเคลื่อนที่ของศัตรู
        for i in range(num_of_enemies):
            # Game Over
            if enemyY[i] > 440: 
                for j in range(num_of_enemies):
                    if i <=4 :
                        enemyY[j] = 600 
                game_over_text()
                break
            # การเคลื่อนที่ของศัตรู
            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = enemyVelocity[i] 
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736: 
                enemyX_change[i] = -enemyVelocity[i]
                enemyY[i] += enemyY_change[i]

            # Collision การชนกันของกระสุนและศัตรู
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                if i <=4  : 
                    score_value += 1
                    enemyVelocity[i] += 0.8 
                    enemyX[i] = random.randint(0, 736)
                    enemyY[i] = random.randint(50, 150)
                else : 
                    score_value -= 1
                    enemyVelocity[i] += 0.2 
                    enemyX[i] = random.randint(0, 736)
                    enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i) 

        #Bullet Movement การเคลื่อนที่ของกระสุน
        if bulletY <= 0: 
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "GradeA":
            heart_bullet(bulletX, bulletY)
            bulletY -= bulletY_change 
        player(playerX, playerY) 
        show_score(textX, textY) 
        pygame.display.update()  
