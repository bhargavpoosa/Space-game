import pygame
import random
import math
from pygame import mixer
#Intialization
pygame.init()
#creating screen
screen=pygame.display.set_mode((800,600))
#creating caption and icon
pygame.display.set_caption('SpaceInvaders')
icon=pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)
# Uploading Background
background=pygame.image.load('backgroundimg.png')
#Background music
mixer.music.load('background.wav')
mixer.music.play(-1)
#player
playerImg=pygame.image.load('space-invaders.png')
playerX=370
playerY=480
playerX_change=0
#Enemy
enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]

#bullet
bulletImg=pygame.image.load('bullet.png')
bulletX=0
bulletY=480
bulletY_change=10
bullet_state='ready'

#Freeze power
freezeImg=pygame.image.load('ice.png')
freezeX=random.randint(0,768)
freezeY=0
freezeY_change=4
freeze_state='active'
#number of enemies
num_enemies=6
for i in range(num_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(4)
    enemyY_change.append(40)

b=[]
#score font
score_value=0
font=pygame.font.Font('freesansbold.ttf',32)

#Gameover font
over_font=pygame.font.Font('freesansbold.ttf',64)

#Score function
def show_score():
    score=font.render("Score: "+str(score_value),True,(255,255,255))
    screen.blit(score,(10,10))

def freeze(x,y):
    global freeze_state
    freeze_state='inactive'
    screen.blit(freezeImg,(x,y))
#player function
def player(x,y):
    screen.blit(playerImg,(x,y))

#enemy function
def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

#Gameover function
def game_over():
    over=over_font.render("GAME OVER",True,(255,0,0))
    screen.blit(over,(200,250))

#Fire Bullet
def fire_bullet(x,y):
    global bullet_state
    bullet_state='fire'
    screen.blit(bulletImg,(x+16,y+10))

def freeze_power(freezeX,freezeY,playerX,playerY):
    dist=math.sqrt(math.pow(freezeX-playerX,2)+math.pow(freezeY-playerY,2))
    if dist<27:
        return True
    return False
#Checking collision
def is_collision(bulletX,bulletY,enemyX,enemyY):
    distance=math.sqrt(math.pow(bulletX-enemyX,2)+math.pow(bulletY-enemyY,2))
    if distance<27:
        return True
    return False

#flag=0
#count=0
running=True
while running==True:
    #Background color
    screen.fill((0,0,0))
    #Adding background image
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                playerX_change=-5
            if event.key==pygame.K_RIGHT:
                playerX_change=5
            if event.key==pygame.K_SPACE:
                if bullet_state=='ready':
                    bulletX=playerX
                    #Adding bullet Sound
                    bullet_sound=mixer.Sound('laser.wav')
                    bullet_sound.play()
                    fire_bullet(bulletX,bulletY)

        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                playerX_change=0

    #Enemy Movement
    for i in range(num_enemies):
        if enemyY[i]>=450:
            for j in range(num_enemies):
                enemyY[j]=2000
            game_over()
            break
#      if freeze_power(freezeX,freezeY,playerX,playerY):
#            count=1
#            for j in range(num_enemies):
#                enemyX_change[j]=0
#            freeze_state='active'
#            freezeY=0
#            freezeX=random.randint(0,768)
#        if flag==2 and count:
#            flag=0
#            count=0
#            for j in range(num_enemies):
#                enemyX_change[4]
        enemyX[i]+=enemyX_change[i]
        if enemyX[i]>=736:
            enemyX_change[i]=-4
            enemyY[i]+=enemyY_change[i]
        elif enemyX[i]<=0:
            enemyX_change[i]=4
            enemyY[i]+=enemyY_change[i]
        collision=is_collision(bulletX,bulletY,enemyX[i],enemyY[i])
        if collision:
    #        if count:
    #            flag+=1
    #            print('flag'+str(flag))
            bullet_state='ready'
            bulletY=480
            collision_sound=mixer.Sound('explosion.wav')
            collision_sound.play()
            score_value+=1
            if score_value%5==0:
                if freeze_state=='active':
                    freeze(freezeX,freezeY)
            enemyX[i]=random.randint(0,736)
            enemyY[i]=random.randint(50,150)
        enemy(enemyX[i],enemyY[i],i)

    #Player Movement
    if playerX>=736:
        playerX=736
    if playerX<=0:
        playerX=0

    if bulletY<=0:
        bullet_state='ready'
        bulletY=480
    if bullet_state=='fire':
        fire_bullet(bulletX,bulletY)
        bulletY-=bulletY_change

    playerX+=playerX_change
    player(playerX,playerY)

    if freeze_state=='inactive':
        freezeY+=freezeY_change
        freeze(freezeX,freezeY)
    if freezeY>=600:
        freeze_state='active'
        freezeY=0
        freezeX=random.randint(0,768)

    show_score()
    pygame.display.update()
