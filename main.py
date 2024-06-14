import pygame
import time
import cv2
import random
from paho.mqtt import client as mqtt
import math

random.seed(time.time())

FULLSCREEN = 1 # 1- for final


TITLE = "Snake Ladder"

running = True

GRID_WIDTH  = 6
GRID_HEIGHT = 6
GAME_SIZE = GRID_WIDTH*GRID_HEIGHT

dice_images = []

back_image                = pygame.image.load("images/background.jpg")
board_image               = pygame.image.load("images/board.png")
pawn_image                = pygame.image.load("images/pawn.png")
logo_image                = pygame.image.load("images/logo.png")
win_image                 = pygame.image.load("images/win.png")
lost_image                = pygame.image.load("images/lost.png")


dice_images.append(pygame.image.load("images/dice_0.png"))
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


broker_address = 'broker.hivemq.com'
broker_port = 1883
topic1 = "Dice/1"
topic2 = "Dice/2"

client_id = f'python-mqtt-{random.randint(0, 1000)}'

dice1 = 0
dice2 = 0

def on_message(client, userdata, message):
    global dice1,dice2,dice_1_image,dice_2_image
    print(f"Message received on topic {message.topic}: {message.payload.decode()}")
    if(message.topic == "Dice/1"):
        msg = str(message.payload.decode())
        if(msg == "Top"):
            dice1 = 1
        if(msg == "Bottom"):
            dice1 = 2
        if(msg == "Right"):
            dice1 = 3
        if(msg == "Left"):
            dice1 = 4
        if(msg == "Back"):
            dice1 = 5
        if(msg == "Front"):
            dice1 = 6
        if(dice1 != 0):
            dice_1_image = dice_images[dice1]
                
    if(message.topic == "Dice/2"):
        msg = str(message.payload.decode())
        if(msg == "Top"):
            dice2 = 1
        if(msg == "Bottom"):
            dice2 = 2
        if(msg == "Right"):
            dice2 = 3
        if(msg == "Left"):
            dice2 = 4
        if(msg == "Back"):
            dice2 = 5
        if(msg == "Front"):
            dice2 = 6
        if(dice2 != 0):
            dice_2_image = dice_images[dice2]


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
        # Subscribe to the topics
        client.subscribe(topic1)
        client.subscribe(topic2)
    else:
        print(f"Connect failed with code {rc}")

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print(f"Unexpected disconnection. Reconnecting in 5 seconds. Code: {rc}")
        time.sleep(5)
        try:
            client.reconnect()
        except:
            print("Reconnection failed. Trying again in 5 seconds.")
            time.sleep(5)
            on_disconnect(client, userdata, rc)
client = mqtt.Client()

# Attach the on_message callback function
client.on_message = on_message
client.on_connect = on_connect
client.on_disconnect = on_disconnect

# Connect to the MQTT broker
client.connect(broker_address, broker_port)


# Start the MQTT client
client.loop_start()

MAX_THROWS = 4

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

snakeAttack = 0
ladderClimb = 0

score_data = ["1", "2", "3", "You have " + str(MAX_THROWS) +" Throws" ]
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
font = pygame.font.Font(None, 45)
scoreboard_width = 500
scoreboard_height = 350

position = 0   
new_position = 0
new_pos_counter_max = 300
new_pos_counter = 0
cnt = 0 


def getCordinates(grid_num):
    if(grid_num >= 7 and grid_num <= 12):
        change = grid_num - 7
        grid_num = 12 - change
    if(grid_num >= 19 and grid_num <= 24):
        change = grid_num - 19
        grid_num = 24 - change
    if(grid_num >= 31 and grid_num <= 36):
        change = grid_num - 31
        grid_num = 36 - change
    if grid_num != 0:
        grid_num = grid_num - 1 # start index from 0
    
    
    x_ =             int((grid_num%GRID_WIDTH)*grid_size) + int(grid_size/2)- int(pawn_image.get_width()/2)
    y_ = HEIGHT -   (int(int(grid_num/GRID_WIDTH)*grid_size) + int(grid_size/2))
    return x_,y_

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
    if grid_num != 0:
        grid_num = grid_num - 1 # start index from 0
    
    
    pawn_x =             int((grid_num%GRID_WIDTH)*grid_size) + int(grid_size/2)- int(pawn_image.get_width()/2)
    pawn_y = HEIGHT -   (int(int(grid_num/GRID_WIDTH)*grid_size) + int(grid_size/2))
    #print(pawn_x)
    #print(pawn_y)

def scanforSnakesAndLadders(pos):
    global snakes, ladders,snakeAttack,ladderClimb
    for snake in snakes:
        if(pos == snake[0]):
            snakeAttack = 1
            print("Snake")
            score_data[2] = "Snake Bite :-("
            pos = snake[1]
    for ladder in ladders:
        if(pos == ladder[0]):
            ladderClimb = 1
            print("Ladder")
            score_data[2] = "Got Ladder :-)"
            pos = ladder[1]
    return pos
    
def draw_scoreboard(screen, x, y, width, height, scores):
    # Draw border
    pygame.draw.rect(screen, black, (x, y, width, height), 3)

    # Draw background
    pygame.draw.rect(screen, white, (x + 3, y + 3, width - 6, height - 6))
    total_text_height = len(scores) * font.get_linesize()

    start_y = y + (height - total_text_height) // 2

    # Draw each row of scores
    for i, score in enumerate(scores):
        text_surface = font.render(score, True, black)
        text_rect = text_surface.get_rect(center=(x + width // 2, start_y + i * font.get_linesize() + font.get_linesize() // 2))
        screen.blit(text_surface, text_rect)

setPawnPos(0)

random.randint(2, 12)
print(int(time.time()*1000))


changePwanAt = int(time.time()*1000) + 2000 # 2 seconds

    
game_exceed = 0

throws = 0
score_data[2] = "Throw Dice.."
game_own = 0

GAME_START_         = 0     
GAME_RUNNING_       = 1
GAME_SNAKE_BITE_    = 2
GAME_LADDER_CLIMB_  = 3
GAME_LOST_          = 4
GAME_WIN_           = 5

gameState = GAME_RUNNING_

showWinImage  = 0
showLostImage = 0
showStartImage = 0

exitwinstateAt = 0
exitloststateAt = 0
exitstartstateAt = int(time.time()) + 2
PWAN_MOVEMENT = 600 #in ms

x1 = 0
y1 = 0
x2 = 0
y2 = 0
speed = 5
dx=0
dy=0
distance =0
steps = 0

x_step = 0
y_step = 0

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print("Enter key pressed!")
                #dice1 = 3
                #dice2 = 3
                new_position = position +  dice1 + dice2

                score_data[3] = "new position:"+str(new_position) + "--"+str(position)
                throws = throws + 1
                if(throws < MAX_THROWS):
                    score_data[2] = "Throw Dice. You Have " + str(MAX_THROWS - throws) + " Throws"
                else:
                    score_data[2] = "You Have no Throws"


    clock = pygame.time.Clock()
    if gameState == GAME_START_:
        if(exitstartstateAt >= int(time.time())):
            position = 0
            new_position = 0
            showStartImage = 1
            throws = 0
            score_data[3] = "new position:"+str(new_position) + "--"+str(position)
            score_data[2] = "Remaing Throws .. " +str(MAX_THROWS - throws)
        else:
            showStartImage = 0
            gameState = GAME_RUNNING_
            print("going to running")

    elif gameState == GAME_RUNNING_:
        setPawnPos(position)

        #if throws == MAX_THROWS and new_position != GAME_SIZE:
        #    exitloststateAt = int(time.time()) + 2
        #    print("going to game lost")
        #    gameState = GAME_LOST_

        if snakeAttack == 1:
            print("going to snake bite")
            x2,y2 = getCordinates(new_position)
            x1 = pawn_x
            y1 = pawn_y
            
            dx = x2 - x1
            dy = y2 - y1
            
            distance = math.sqrt(dx**2 + dy**2)
            steps = int(distance/speed)
            if(steps == 0):
                steps = 1
            x_step = (dx / steps)
            y_step = (dy / steps)
            
            gameState = GAME_SNAKE_BITE_
        elif ladderClimb == 1:
            print("going to Ladder Climb")
            x2,y2 = getCordinates(new_position)
            x1 = pawn_x
            y1 = pawn_y
            
            dx = x2 - x1
            dy = y2 - y1
            
            distance = math.sqrt(dx**2 + dy**2)
            steps = int(distance/speed)
            if(steps == 0):
                steps = 1
            x_step = (dx / steps)
            y_step = (dy / steps)
            

            gameState = GAME_LADDER_CLIMB_
        else:
            if(new_position > position):
                if(changePwanAt < int(time.time()*1000)):
                    changePwanAt = int(time.time()*1000) + PWAN_MOVEMENT # next move after this time 
                    position = position + 1
                    print(position)
                    if(new_position == position): # reached targeted grid
                        if new_position == GAME_SIZE:
                            print("going to Win")
                            exitwinstateAt = int(time.time()) + 5
                            gameState = GAME_WIN_
                        else:
                            new_position = scanforSnakesAndLadders(position)

            elif(new_position < position): # do not come here
                pass
            else:
                if throws == MAX_THROWS and position != GAME_SIZE:
                    exitloststateAt = int(time.time()) + 2
                    print("going to game lost")
                    gameState = GAME_LOST_

    elif gameState == GAME_SNAKE_BITE_:
        snakeAttack = 0
        pawn_x += x_step
        pawn_y += y_step
       # print( "pawn_x:" + str(pawn_x) + "  pawn_y:" + str(pawn_y) + " "+ str(x_step)+ " "+str(y_step))
        if (dx == 0 and abs(pawn_y - y2) < abs(y_step)) or (dy == 0 and abs(pawn_x - x2) < abs(x_step)) or (abs(pawn_x - x2) < abs(x_step) and abs(pawn_y - y2) < abs(y_step)):
            pawn_x = x2
            pawn_y = y2
            position = new_position
            gameState = GAME_RUNNING_
        #position = new_position
        #gameState = GAME_RUNNING_
        
    elif gameState == GAME_LADDER_CLIMB_:
        ladderClimb = 0
        pawn_x += x_step
        pawn_y += y_step
       # print( "pawn_x:" + str(pawn_x) + "  pawn_y:" + str(pawn_y) + " "+ str(x_step)+ " "+str(y_step))
        if (dx == 0 and abs(pawn_y - y2) < abs(y_step)) or (dy == 0 and abs(pawn_x - x2) < abs(x_step)) or (abs(pawn_x - x2) < abs(x_step) and abs(pawn_y - y2) < abs(y_step)):
            pawn_x = x2
            pawn_y = y2
            position = new_position
            gameState = GAME_RUNNING_

        #position = new_position
        #gameState = GAME_RUNNING_
        
    elif gameState == GAME_LOST_:
        setPawnPos(new_position)
        if(exitloststateAt >= int(time.time())):
            showLostImage = 1
        else:
            showLostImage = 0
            exitstartstateAt = int(time.time()) + 2
            gameState = GAME_START_
        pass
    elif gameState == GAME_WIN_:
        setPawnPos(position)
        if(exitwinstateAt >= int(time.time())):
            showWinImage = 1
        else:
            showWinImage = 0
            exitstartstateAt = int(time.time()) + 2
            gameState = GAME_START_

    else:
        pass

    
    # common updates
    

    image_rect = back_image.get_rect()
    image_rect.center = (WIDTH // 2, HEIGHT // 2)
    screen.blit(back_image, image_rect)

    screen.blit(board_image, (0, 0))
    screen.blit(pawn_image, (pawn_x, pawn_y))
    screen.blit(logo_image, (x_offset_logo,y_offset_logo))
    
    screen.blit(dice_1_image, (x_offset_dice1,y_offset_dice1))
    screen.blit(dice_2_image, (x_offset_dice2,y_offset_dice2))
    
    score_data[0] = "Dice1 :" + str(dice1) + "  Dice2 :" + str(dice2)
    score_data[1] = "You are at " + str(position)

    draw_scoreboard(screen, x_offset_score, y_offset_score, scoreboard_width, scoreboard_height, score_data)

    if showWinImage == 1 :
        image_rect = win_image.get_rect()
        image_rect.center = (WIDTH // 2, HEIGHT // 2)
        screen.blit(win_image, image_rect)    

    if showLostImage == 1:    
        image_rect = lost_image.get_rect()
        image_rect.center = (WIDTH // 2, HEIGHT // 2)
        screen.blit(lost_image, image_rect)    
    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)

   
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print("Enter key pressed!")
                new_position = position + dice1 + dice2 #scanforSnakesAndLadders(position + random.randint(2, 4))
                score_data[2] = "Throw Dice.."
                throws = throws + 1
                score_data[3] = "Remaing Throws .. " +str(MAX_THROWS-throws)
                if(throws == MAX_THROWS):
                    throws = 0
                    print("Game END..")
                    score_data[3] = "Game END.."
                    game_exceed = 1
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
            new_position = 0
            position = 0
            game_exceed =  0
            throws =  0
            score_data[3] = " You've WON the GAME "

        elif(game_exceed == 1):
            game_exceed = 0
            print("Failed!!!")
            new_position = 0
            position = 0
            score_data[3] =  "You have "+str(MAX_THROWS)+" Throws" 
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


    #pygame.draw.rect(screen, color, pygame.Rect(x_offset_score, y_offset_score,  logo_image.get_width(),60))
    score_data[0] = "Dice1 :" + str(dice1) + "  Dice2 :" + str(dice2)
    score_data[1] = "You are at " + str(position)

    draw_scoreboard(screen, x_offset_score, y_offset_score, scoreboard_width, scoreboard_height, score_data)
    
    
    pygame.display.flip()

    pygame.display.update()
    
    clock.tick(60)
    