import pygame
import time
import random
import sys
# initializing the game
pygame.init()

def quitgame():
    pygame.quit()
    sys.exit()

# size of the display window
display_width = 800
display_height = 600
button_w = 160
button_h = 60
# to change the speed of the blocks
speed = 7

# setting up the game window size
gameDisplay = pygame.display.set_mode((display_width, display_height))

# Audio files
car_crash_sound = pygame.mixer.Sound("media/car_crash.wav")
car_start_sound = pygame.mixer.Sound("media/car_start.wav")
pygame.mixer.music.load("media/game_music.wav")

# defining colours
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 200, 0)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
yellow = (246, 235, 14)
pause = False

car_width = 73
# setting up the caption of the window
pygame.display.set_caption('Highway Havoc')

clock = pygame.time.Clock()

aiCarImg = pygame.image.load('media/ai_car.png')
carImg = pygame.image.load('media/hCar.png')

def unpause():
    global pause
    pause = False
    pygame.mixer.music.unpause()


def paused():
    pygame.mixer.music.pause()
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
        gameDisplay.fill(white)
        button('RESUME', display_width / 2 - button_w / 2, display_height / 2, button_w, button_h, green, bright_green, unpause)
        button('QUIT', display_width / 2 - button_w / 2, display_height / 2 + 3 * button_h / 2, button_w, button_h, red, bright_red,
               gameintro)
        message('Game Paused', 64, black, (display_width / 2, display_height / 4))
        pygame.display.update()
        clock.tick(15)

def button(text, x, y, w, h, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pygame.draw.rect(gameDisplay, active_color, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, inactive_color, (x, y, w, h))
    message(text, 22, white, (x + w / 2, y + h / 2))

# to show the position of car
def car(x, y):
    gameDisplay.blit(carImg, (x, y))


# to show the position of aicar
def aiCar(aiX, aiY):
    gameDisplay.blit(aiCarImg, (aiX, aiY))

def message(text, textSize, textColor, textCenterPos):
    textFont = pygame.font.Font("freesansbold.ttf", textSize)
    textSurf = textFont.render(text, True, textColor)
    textRect = textSurf.get_rect()
    textRect.center = textCenterPos
    gameDisplay.blit(textSurf, textRect)
#
def things_doged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Human : " + str(count), True, black)
    gameDisplay.blit(text, (0, 0))


def ai_things_doged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("AI : " + str(count), True, black)
    gameDisplay.blit(text, (100, 0))


def text_objects(text, font):
    # true parameter is for anti aliasing
    TextSurf = font.render(text, True, black)
    return TextSurf, TextSurf.get_rect()


# to show blocks on the screen
def things(thingx, thingy, thingh, thingw, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingh, thingw])

#yellow point blocks
def yellow_b(thingx, thingy, thingh, thingw, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingh, thingw])

#to show red blocks
def r_block(thingx, thingy, thingh, thingw, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingh, thingw])

# to display a message to screen
def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()

    #  we want the message to show for only about 2 sec
    time.sleep(2)
    # re referencing the game loop if the user does not want to quit the game
    game_loop()


# when you crashed into a block
def crash():
    #message_display("You Crashed")
    message('You Loss AI WIN!', 48, bright_red, (display_width / 2, display_height / 4))
    pygame.mixer.Sound.play(car_crash_sound)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
        button('PLAY AGAIN', display_width / 2 - button_w / 2, display_height / 2, button_w, button_h, green, bright_green, game_loop)
        button('MAIN MENU', display_width / 2 - button_w / 2, display_height / 2 + 3 * button_h / 2, button_w, button_h, red,
               bright_red, gameintro)
        pygame.display.update()
        clock.tick(15)


# play the game
def game_loop():
    pygame.mixer.music.play(-1)
    global pause
    x = display_width * 0.45
    y = display_height * 0.80
    aiX = display_width * 0.20
    aiY = display_height * 0.80
    x_change = 0
    aiX_change = 0
    thing_startx = random.randrange(0, display_width)
    r_block_x = random.randrange(0, display_width)
    r_block_y = -800
    r_width = 100
    r_height = 50
    yellow_b_y = -2000
    yellow_b_x = random.randrange(0, display_width)
    y_width = r_width/2
    y_height = r_height/3
    thing_starty = -600
    thing_speed = speed
    thing_width = 100
    thing_height = 100
    doged = 0
    aiDoged = 0
    # initially we are not crashed
    gameExit = False

    while not gameExit:
        
        # this creates a list of events per frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # exiting the game if the user does not to play any more
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
        x += x_change
        gameDisplay.fill(green)


        
        things(thing_startx, thing_starty, thing_width, thing_height, black)
        r_block(r_block_x, r_block_y, r_width, r_height, red)
        yellow_b(yellow_b_x, yellow_b_y, y_width, y_height, yellow)
        thing_starty += thing_speed
        r_block_y += (speed*1.2)
        yellow_b_y += (speed*1.4)
        things_doged(doged)
        ai_things_doged(aiDoged)
        car(x, y)

        if x > display_width - car_width or x < 0:
            crash()
        # by this we know that the block is off the screen
        if thing_starty > display_height:
            if doged % 10 == 0:
                thing_speed = thing_speed + 1
            doged = doged + 1

        if y < thing_starty + thing_height:
            print("y cross over")
            if x > thing_startx and x < thing_startx + thing_width or x + car_width > thing_startx and x + car_width < thing_startx + thing_width:
                print('x cross over')
                crash()

        #crash with red block
        if y < r_block_y + r_height:
            #print("y cross over")
            if x > r_block_x and x < r_block_x + r_width or x + car_width > r_block_x and x + car_width < r_block_x + r_width:
                #print('x cross over')
                doged=doged-2
                r_block_y = -2000
                r_block_x = random.randrange(0 , display_width)
        #yellow points
        if y < yellow_b_y + y_height:
            
            if x > yellow_b_x and x < yellow_b_x + y_width or x + car_width > yellow_b_x and x + car_width < yellow_b_x + y_width:
                #print('x cross over')
                doged=doged+5
                yellow_b_y = -3000
                yellow_b_x = random.randrange(0 , display_width)
            


        # AI_Part
        print('thing start: ', thing_startx)
        print('thing end: ', thing_startx + thing_width)
        print('car : ', aiX)
        if aiX > thing_startx - 100:
            if aiX < thing_startx + thing_width + 100:
                if thing_startx - 100 > 800 - 100 - thing_startx - thing_width:
                    aiX_change -= 5
                else:
                    aiX_change += 5
            else:
                aiX_change = 0
        else:
            aiX_change = 0

        aiX += aiX_change
        # gameDisplay.fill(white)

        
        ai_things_doged(aiDoged)
        aiCar(aiX, aiY)

        if aiX > display_width - car_width or aiX < 0:
            crash()
            pygame.quit()
            # python   quit
            quit()

        # by this we know that the block is off the screen
        if thing_starty > display_height:
            # so that the user gets a moment when the new block comes in
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0, display_width)
            thing_width = random.randrange(100, 150)
            aiDoged = aiDoged + 1 # ai_things_doged(aiDoged)
        
        #ai with red block
        if aiY < r_block_y + r_height:
            #print("y cross over")
            if aiX > r_block_x and aiX < r_block_x + r_width or aiX + car_width > r_block_x and aiX + car_width < r_block_x + r_width:
                #print('x cross over')
                aiDoged = aiDoged - 2
                r_block_y = -2000
                r_block_x = random.randrange(0 , display_width)

        #points for ai
        if aiY < yellow_b_y + y_height:
            
            if aiX > yellow_b_x and aiX < yellow_b_x + y_width or aiX + car_width > yellow_b_x and aiX + car_width < yellow_b_x + y_width:
                #print('x cross over')
                aiDoged = aiDoged+5
                yellow_b_y = -3000
                yellow_b_x = random.randrange(0 , display_width)   

        # red or yellow block pass without being catched
        if yellow_b_y > display_height:
            yellow_b_y = -3000
            yellow_b_x = random.randrange(0 , display_width) 
        elif r_block_y > display_height:
            r_block_y = -2000
            r_block_x = random.randrange(0 , display_width)

        if aiY < thing_starty + thing_height:
            # print('y cross over')
            if aiX > thing_startx and aiX < thing_startx + thing_width or aiX + car_width > thing_startx and aiX + car_width < thing_startx + thing_width:
                # print('x cross over')
                print('game over')
                crash()
                pygame.quit()
                # python   quit
                quit()
        pygame.display.update()

        # this takes frames per second as input
        clock.tick(60)

# Intro Screen
def gameintro():
    pygame.mixer.music.play(-1)
    gameDisplay.fill(white)
    pygame.time.delay(2000)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
        gameDisplay.fill(white)

        button('PLAY', display_width / 2 - button_w / 2, display_height / 2, button_w, button_h, green, bright_green,game_loop)
        button('QUIT', display_width / 2 - button_w / 2, display_height / 2 + 3 * button_h / 2, button_w, button_h, red, bright_red,
               quitgame)

        message('Highway Havoc!', 72, black, (display_width / 2, display_height / 4))
        pygame.display.update()
        clock.tick(15)

# Load Screen
def loading():
    pygame.mixer.Sound.play(car_start_sound)
    gameDisplay.fill(white)
    message('LOADING', 42, black, (display_width / 2, display_height / 2))
    x = display_width / 5
    endx = 4 * x
    y = 2 * display_height / 3
    while x <= endx:
        x += 15
        pygame.draw.rect(gameDisplay, red, (x, y, 15, 5))
        pygame.display.update()
        clock.tick(10)
    # running game loop
    gameintro()

# pygame quits
#pygame.quit()
# python quit
#quit()
# Start Game
loading()

