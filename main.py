import pygame
import time
import cv2
import random

random.seed(time.time())

FULLSCREEN = 1 # 1- for final


TITLE = "Snake Ladder"

running = True

GRID_WIDTH  = 6
GRID_HEIGHT = 6
GAME_SIZE = GRID_WIDTH*GRID_HEIGHT

dice_images = []

board_image               = pygame.image.load("images/board.png")
pawn_image                = pygame.image.load("images/pawn.png")
logo_image                = pygame.image.load("images/logo.png")

dice_images.append(pygame.image.load("images/dice_1.png"))
dice_images.append(pygame.image.load("images/dice_2.png"))
dice_images.append(pygame.image.load("images/dice_3.png"))
dice_images.append(pygame.image.load("images/dice_4.png"))
dice_images.append(pygame.image.load("images/dice_5.png"))
dice_images.append(pygame.image.load("images/dice_6.png"))

dice_1_image = dice_images[0]
dice_2_image = dice_images[0]




#pawn_image = pygame.transform.scale(image, (new_width, new_height))

WIDTH, HEIGHT = board_image.get_width() , board_image.get_height() #800,600 # if not full screen

pygame.init()

if FULLSCREEN == 1:
    infoObject = pygame.display.Info()
    WIDTH, HEIGHT = (infoObject.current_w, infoObject.current_h)
    screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
    aspect_ratio = board_image.get_height() / board_image.get_width()
    board_image = pygame.transform.scale(board_image, (int(HEIGHT*aspect_ratio), HEIGHT))
else:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
    
clock = pygame.time.Clock()
pygame.display.set_caption(TITLE)

pawn_x = 50
pawn_y = 50

grid_size = board_image.get_width()/GRID_WIDTH


x_offset_dice1 = int(board_image.get_width() * 1.2)
y_offset_dice1 = int(board_image.get_height() * 0.75)

x_offset_dice2 = int(x_offset_dice1 + (dice_1_image.get_width() * 2))
y_offset_dice2 = int(board_image.get_height() * 0.75)


x_offset_logo = int(board_image.get_width()*1.2)
y_offset_logo = int(HEIGHT*0.05)

x_offset_score = int(board_image.get_width()*1.2)
y_offset_score = int(board_image.get_height() * 0.40)


color = (255,0,0)




snakes = [  [16,2],
            [25,12],
            [34,22],
            [20,5],
            [31,20]
            ]
ladders= [  [6,18],
            [11,14],
            [15,22],
            [21,28],
            [23,35]
         ]

def setPawnPos(grid_num):
    global pawn_x,pawn_y
    
    #if(not(grid_num <=6 or (grid_num >=13 and grid_num <=18) or(grid_num >=25 and grid_num <=30))):
     #   grid_num = grid_num-6
    if(grid_num >= 7 and grid_num <= 12):
        change = grid_num - 7
        grid_num = 12 - change
    if(grid_num >= 19 and grid_num <= 24):
        change = grid_num - 19
        grid_num = 24 - change
    if(grid_num >= 31 and grid_num <= 36):
        change = grid_num - 31
        grid_num = 36 - change
    grid_num = grid_num - 1 # start index from 0
    
    
    pawn_x =             int((grid_num%GRID_WIDTH)*grid_size) + int(grid_size/2)- int(pawn_image.get_width()/2)
    pawn_y = HEIGHT -   (int(int(grid_num/GRID_WIDTH)*grid_size) + int(grid_size/2))
    #print(pawn_x)
    #print(pawn_y)

snakeAttack = 0
ladderClimb = 0




def scanforSnakesAndLadders(pos):
    global snakes, ladders,snakeAttack,ladderClimb
    for snake in snakes:
        if(pos == snake[0]):
            snakeAttack = 1
            print("Snake")
            pos = snake[1]
    for ladder in ladders:
        if(pos == ladder[0]):
            ladderClimb = 1
            print("Ladder")
            pos = ladder[1]
    return pos
    


setPawnPos(12)

position = 1   
new_position = 0

new_pos_counter_max = 300
new_pos_counter = 0

cnt = 0 

dice1 = 0
dice2 = 0


random.randint(2, 12)
print(int(time.time()*1000))


changePwanAt = int(time.time()*1000) + 2000 # 2 seconds

def updateTimer():
    global changePwanAt
    changePwanAt = int(time.time()*1000) + 500 # 2 seconds
    
game_exceed = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                #position = position + random.randint(2, 4)
                #if(position >= 36):
                 #   position = 1
                print("Enter key pressed!")
                dice1 = random.randint(1,6)
                dice2 = random.randint(1,6)
                new_position = position + dice1 + dice2 #scanforSnakesAndLadders(position + random.randint(2, 4))
                dice_1_image = dice_images[dice1-1]
                dice_2_image = dice_images[dice2-1]
                if(new_position > GAME_SIZE ):
                    game_exceed = 1
        

    if(new_position > position):
        if ladderClimb == 1:
            if(changePwanAt < int(time.time()*1000)):
                updateTimer()
                position = new_position 
                ladderClimb = 0
                print("new position:"+str(new_position) + "--"+str(position))
        else:
            if(changePwanAt < int(time.time()*1000)):
                updateTimer()
                position = position + 1
                print("new position:"+str(new_position) + "--"+str(position))
    elif(new_position == position):
        if(new_position == GAME_SIZE):
            print("WWWWWWWWWIIIIIIIINNNNNNNNNNNN!!!")
            new_position = 1
            position = 1
        elif(game_exceed == 1):
            game_exceed = 0
            print("Failed!!!")
            new_position = 1
            position = 1
        else:
            new_position = scanforSnakesAndLadders(position)
    else:#eaten by snake
        if snakeAttack == 1:
            if(changePwanAt < int(time.time()*1000)):
                updateTimer()
                position = new_position 
                ladderClimb = 0
                print("new position:"+str(new_position) + "--"+str(position))
    setPawnPos(position)
    

    
    screen.blit(board_image, (0, 0))
    screen.blit(pawn_image, (pawn_x, pawn_y))
    screen.blit(logo_image, (x_offset_logo,y_offset_logo))
    
    screen.blit(dice_1_image, (x_offset_dice1,y_offset_dice1))
    screen.blit(dice_2_image, (x_offset_dice2,y_offset_dice2))
    
    #pygame.draw.rect(screen, color, pygame.Rect(x_offset_dice, y_offset_dice, 60, 60))
    #pygame.draw.rect(screen, color, pygame.Rect(x_offset_logo, y_offset_logo, 60, 60))
    pygame.draw.rect(screen, color, pygame.Rect(x_offset_score, y_offset_score,  logo_image.get_width(),60))
    
    
    pygame.display.flip()

    pygame.display.update()
    
    clock.tick(60)
    