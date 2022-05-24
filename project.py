import math #ใช้คำนวณทางคณิตศาสตร์เก็บแต้ม
import random #ใช้สุ่มตำแหน่งของตัวที่ถูกยิง
import sqlite3 #ใช้module db
import pygame
#from pygame import mixer

#pygame
pygame.init() #initialize การเริ่มต้นกำลังจะเขียนแล้ว
con = sqlite3.connect(r"project.db") #สร้างตัวแปรเรียกใช้module sqlite3 ในวงเล็บต้องใส่ที่อยู่ไฟล์db และใส่rเพราะให้มันreadทุกตัวไล่มา

   #screen
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #คำสั่งตั้งขนาดจอแสดงผล
#Background
background = pygame.image.load('wall (1).png') #เปลี่ยนภาพพื้นหลัง
background_intro = pygame.image.load('intro wall (7).png') #เปลี่ยนภาพพื้นหลัง

# Sound
#mixer.music.load("love.mp3") #เสียงเพลงประกอบ
#mixer.music.play() #คำสั่งเล่นเพลง

# Caption and Icon
pygame.display.set_caption("Sky Attack") #ใส่ชื่อเกมส์
icon = pygame.image.load('penguin.png') #ใส่ไอคอน
pygame.display.set_icon(icon) #เปลี่ยนไอคอนเกมส์ให้เป็นตามที่เราตั้งไว้

# Player
playerImg = pygame.image.load('teacher.png') #ไอคอนยาน
playerX = 350 #ตำแหน่งจุดเริ่มต้นของยานแกนx
playerY = 500 #ตำแหน่งจุดเริ่มต้นของยานแกนy
playerX_change = 0 #ความเร็วของการเคลื่อนที่ยานไปชนขอบในตอนเริ่มต้นเลขเยอะเคลื่อนที่เร็ว (พิมลบ เลขน้อย จะเคลื่อนที่ไปทางซ้ายช้าๆ)

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 8 #จำนวนตัวเลขของenemy
enemyVelocity = [3,3,3,3,3,3,3,3] #ความเร็วของenemy
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
    enemyImg.append(pygame.image.load(enemyPic[i])) #รูปenemy
    enemyX.append(random.randint(0, 736)) #แรนดอมการเกิดของenemyในช่วงแกนx 0-736
    enemyY.append(random.randint(150, 150)) #แรนดอมการเกิดของenemyในช่วงแกนy 50-150
    enemyX_change.append(2) #เคลื่อนที่ตามแนวแกนxทีละ4pixel
    enemyY_change.append(20) #การเคลือนที่ลงมาในแต่ละครั้งเมื่อชนขอบเกมส์ในแนวแกนy (เลขเยอะเคลื่อนลงมาเยอะ)

# Bullet
bulletImg = pygame.image.load('a-plus-test-result-of-school (1).png') #รูปกระสุน
bulletX = 400 #ค่าเป็น0เพราะกระสุนไม่เคลื่อนที่ในเเนวเเกนx (เชื่อมกับplayer ตามบรรทัดที่119)
bulletY = 480 #ตำเเหน่งกระสุนในเเนวเเกนY (เชื่อมกับplayer ตามบรรทัด119)
bulletY_change = 15 #ความเร็วของกระสุนที่ยิงในแนวแกนy ยิ่งเลขน้อยยิ่งช้า
bullet_state = "ready"

# Score

score_value = 0 #scoreเริ่มต้น=0
font = pygame.font.Font('freesansbold.ttf', 32) #fontของscore

textX = 10 #ตำแหน่งของscore
textY = 10 #ตำแหน่งของscore

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64) #fontของgameover

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


#คำสั่ง blit เป็นคำสั่งให้เเสดงผล

def show_score(x, y): #score&usernameที่เเสดงผลมุมซ้ายบน
    score2 = font.render("Username : " + username , True, (0, 76, 153))
    score = font.render("Score : " + str(score_value), True, (0, 76, 153))
    screen.blit(score2, (10,10)) #biltคำสั่งแสดงผล
    screen.blit(score, (10,50))

def game_over_text():
    global savescore
    if savescore == 1 :
        savescore = 0
        cmd2 = f"""INSERT INTO scoregame(score,username)
         VALUES ("{score_value}","{username}")"""
        # สร้างตัวแปรมาเก็บคำสั่ง ในvaluesคือข้อมูลที่เรารอรับจากusersจะเอาไปใส่แต่ละคอลัม
        con.execute(cmd2)  # สามารถรันคำสั่งในวงเล็บนี้ได้
        con.commit()  # บันทึกค่าล่าสุดหลังแก้ไข
    over_text = over_font.render("GAME OVER", True, (255, 255, 255)) #ตัวหนังสือGAMEOVER
    screen.blit(over_text, (200,70)) #เเสดงผลGAME OVERตามตำเเหน่ง
    over_text = over_font.render("TOP 5", True,(0, 0, 0)) #ตัวหนังสือTOP5
    screen.blit(over_text, (300, 150)) #เเสดงผลTOP5ตามตำเเหน่ง

    #scoreboard TOP5
    cmd = """SELECT * FROM scoregame WHERE username!='' ORDER BY score DESC LIMIT 5 """ #ดึงข้อมูลมาจากdb
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
    scoreboard_text1 = over_scoreboard.render("No.1 SCORE "+str(scoreboard[0][2])+" --> "+str(scoreboard[0][1]), True,(0, 0, 0)) #scoreboard0 ช่องที่2(score)+ช่องที่ 1(ชื่อ)
    screen.blit(scoreboard_text1, (200, 220)) #ตำเเหน่งที่เเสดง
    scoreboard_text2 = over_scoreboard.render("No.2 SCORE " + str(scoreboard[1][2]) + " --> " + str(scoreboard[1][1]), True,(0, 0, 0)) #scoreboard1 ช่องที่2(score)+ช่องที่ 1(ชื่อ)
    screen.blit(scoreboard_text2, (200, 270)) #ตำเเหน่งที่เเสดง
    scoreboard_text3 = over_scoreboard.render("No.3 SCORE " + str(scoreboard[2][2]) + " --> " + str(scoreboard[2][1]), True,(0, 0, 0)) #scoreboard2 ช่องที่2(score)+ช่องที่ 1(ชื่อ)
    screen.blit(scoreboard_text3, (200, 320)) #ตำเเหน่งที่เเสดง
    scoreboard_text4 = over_scoreboard.render("No.4 SCORE " + str(scoreboard[3][2]) + " --> " + str(scoreboard[3][1]), True,(0, 0, 0)) #scoreboard3 ช่องที่2(score)+ช่องที่ 1(ชื่อ)
    screen.blit(scoreboard_text4, (200, 370)) #ตำเเหน่งที่เเสดง
    scoreboard_text5 = over_scoreboard.render("No.5 SCORE " + str(scoreboard[4][2]) + " --> " + str(scoreboard[4][1]), True,(0, 0, 0)) #scoreboard4 ช่องที่2(score)+ช่องที่ 1(ชื่อ)
    screen.blit(scoreboard_text5, (200, 420)) #ตำเเหน่งที่เเสดง


def player(x, y):
    screen.blit(playerImg, (x, y)) #เเสดงตำเเหน่งplayer(ยาน) ค่าx,yตามบรรทัด30 31 และ170


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y)) #แสดงภาพenemy


def heart_bullet(x, y):
    global bullet_state #ประกาศตัวแปร
    bullet_state = "GradeA"  # ให้มันเชื่อมกับกระสุน
    screen.blit(bulletImg, (x + 16, y + 10)) #แสดงตำแหน่งที่ปล่อยกระสุนออกมา (ถ้าไม่+ตำเเหน่งกระสุนจะไม่ออกมาจากตรงกลางของยานอวกาศ)

def isCollision(enemyX, enemyY, bulletX, bulletY): #ตรวจสอบการชนกัน
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2))) #ตามสูตรหาระยะห่างระหว่างจุดสองจุด
    if distance < 50: #ยิ่งเลขเยอะยิงโดนง่ายขึ้น
        return True #ยิ่งแล้วตาย
    else:
        return False #ยิงแล้วไม่ตายเพราะไกลเกิน25


# Game Loop
inputbox = InputBox(15,250,100,300,70)
running = True #while true คือการรันโดยไม่มีที่สิ้นสุดเพราะมันtrueตลอด แต่เราไม่ได้อยากให้มันรันตลอดเลยต้องใส่ running = true (trueคือบอกว่าจะให้มีการวิ่ง runningคือการบอกให้เกมส์เริ่มเดินตลอดเวลาจนกว่าจะ...)
while running:
    screen.fill((255,255,255))
    # Background Image
    screen.blit(background, (0, 0))  # แสดงbackgroundที่เรานำเข้ามา
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
        for event in pygame.event.get(): #คำสั่งเช็คเหตุการณ์ที่อยู่ในเกมส์ว่ามีอะไรบ้าง
            if event.type == pygame.QUIT: #ฟังก์ชันในการปิด คือถ้ากดปุ่มปิดโปรแกรมของเราก็จะหยุดทันทีfalse
                running = False #เปลี่ยนเป็นfalse ก็คือจบเกมส์
        ## ---------------------------------------------Baimon------------------------------------------------------------------
            # if keystroke is pressed check whether its right or left (หากกดเเป้นพิมพ์ตรวจสอบว่าขวาหรือซ้าย)
            if event.type == pygame.KEYDOWN: #เมื่อกดเเป้น
                if event.key == pygame.K_LEFT: #เมื่อกดปุ่มซ้าย playerX_change = -5
                    playerX_change = -2
                if event.key == pygame.K_RIGHT: #กดปุ่มขวา playerX_change = 5
                    playerX_change = 2
                if event.key == pygame.K_SPACE: #เมื่อกดspacebar
                    if bullet_state == "ready": #เชื่อมกับBullet Movement บรรทัด162
                        #bulletSound = mixer.Sound("laser.wav")  # เสียงยิง
                        #bulletSound.play()  # เรียกใช้เสียง
                        # รับพิกัด x ปัจจุบันของยานอวกาศ เพื่อระบุที่อยู่ของกระสุน
                        bulletX = playerX #ที่อยู่กระสุน=ที่อยู่ยาน
                        heart_bullet(bulletX, bulletY) #ใช้ฟังก์ชันfire_bullet
                if event.key == pygame.K_DOWN : #ปิดเสียง
                    pygame.mixer.music.pause()
                if event.key == pygame.K_UP : #เปิดเสียง
                    pygame.mixer.music.unpause()

            if event.type == pygame.KEYUP: #เมื่อปล่อยเเป้นลูกศรซ้ายขวา
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0 #ไม่มีการเปลี่ยนเเปลง

        playerX += playerX_change #การเคลื่อนที่ยานแนวแกนx กำหนดให้อยู่ภายในขอบของเกมส์
        if playerX <= 0:
            playerX = 0
        elif playerX >= 750:
            playerX = 750
        ## ---------------------------------------------Baimon------------------------------------------------------------------
        #การเคลื่อนที่ของศัตรู
        for i in range(num_of_enemies):
            # Game Over
            if enemyY[i] > 440: #ถ้าenemy เคลื่อนที่เกิน440ในแนวแกนy จะเรียกใช้ฟังก์ชันgame_over_text
                for j in range(num_of_enemies):
                    if i <=4 :
                        enemyY[j] = 600 #enemyเคลื่อนที่ตามแกนyยาว600จะgame over ถ้าตั้งต่ำกว่านี้เกมส์จะoverแต่enemy จะไม่หายไปแล้วเล่นเกมส์ต่อได้
                game_over_text()
                break
            # การเคลื่อนที่ของศัตรู
            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = enemyVelocity[i] #ความเร็วในการเคลื่อนที่ของenemy เมื่อชนขอบ0
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736: #ความเร็วในการเคลื่อนที่ของenemy เมื่อชนขอบ736
                enemyX_change[i] = -enemyVelocity[i]
                enemyY[i] += enemyY_change[i]
    ### ---------------------------------------------Baimon------------------------------------------------------------------
            # Collision การชนกันของกระสุนและศัตรู
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                if i <=4  : #i 0-4 เป็นตัวenemyปกติ
                    score_value += 1
                    enemyVelocity[i] += 0.8 #เพิ่มความเร็วมาทุกครั้งที่ยิง
                    # การสั่งให้สุ่มenemy ถ้าไม่มีจะไม่มีการสุ่มตัวให่มมาและตัวเก่าก็จะไม่หายไปแต่scoreจะเพิ่มขึ้นปกติ
                    enemyX[i] = random.randint(0, 736)
                    enemyY[i] = random.randint(50, 150)
                else : #ตัวenemyลดคะเเนน
                    score_value -= 1
                    enemyVelocity[i] += 0.2 #เพิ่มความเร็วมาทุกครั้งที่ยิง
                    # การสั่งให้สุ่มenemy ถ้าไม่มีจะไม่มีการสุ่มตัวให่มมาและตัวเก่าก็จะไม่หายไปแต่scoreจะเพิ่มขึ้นปกติ
                    enemyX[i] = random.randint(0, 736)
                    enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i) #เรียกใช้ฟังก์ชันenemyเพื่อให้แสดงenemy ถ้าไม่เรียกจะไม่แสดงenemyแต่ยังสามารถสุ่มยิงได้โดยที่scoreก็ยังเพิ่มขึ้นได้

        #Bullet Movement การเคลื่อนที่ของกระสุน
        if bulletY <= 0: #เมื่อกระสุนเคลื่อนที่ไปถึงตำแหน่ง0 จะกลับมาปล่อยที่ 480
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "GradeA":
            heart_bullet(bulletX, bulletY)
            bulletY -= bulletY_change #BulletYเคลื่อนที่ไปข้างบนโดยลบกับค่าของ bulletY_change
        player(playerX, playerY) #กำหนดตำเเหน่งplayer
        show_score(textX, textY) #กำหนดตำเเหน่งscore
        pygame.display.update()  #ทำให้สีพื้นหลังที่เปลี่ยนเป็นสีล่าสุด