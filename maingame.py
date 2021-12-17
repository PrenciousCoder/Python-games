import pygame # Pygame module
import os # To access OS functions such as load and path join
import sys # To access functions of FONT and SOUND
pygame.font.init() # initialization for font
pygame.mixer.init() # initialization for sound

WIDTH, HEIGHT=900,500 # width and height of game window
WIN =pygame.display.set_mode((WIDTH, HEIGHT)) # TO display game window
pygame.display.set_caption("First game") # name of the game window

#Colors needed for the game
WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
YELLOW=(255,255,0)

#setting middle border, FPS,and velocity of spaceship and bullets
BORDER=pygame.Rect(WIDTH//2,0,10,HEIGHT)
FPS=60
BULLET_VEL=10
VEL=5
SPACESHIP_WIDTH,SPACESHIP_HEIGHT=55,40
MAX_BULLETS=10

#FONT and SOUND set
HEALTH_FONT=pygame.font.SysFont('comicsans',40)
WINNER_FONT=pygame.font.SysFont('comicsans',100)
BULLET_HIT_SOUND=pygame.mixer.Sound(os.path.join('/Volumes/Dev T7/vscode/projects/Pythonvscode/Python Modules/Pygamemodule/PygameForBeginners-main/Assets/Grenade+1.mp3'))
BULLET_FIRE_SOUND=pygame.mixer.Sound(os.path.join('/Volumes/Dev T7/vscode/projects/Pythonvscode/Python Modules/Pygamemodule/PygameForBeginners-main/Assets/Gun+Silencer.mp3'))

#Initializing spaceship HIT event
YELLOW_HIT=pygame.USEREVENT+1
RED_HIT=pygame.USEREVENT+2

#joining path for spaceship image and setting orientation of the image
YELLOW_SPACESHIP_IMAGE=pygame.image.load(os.path.join('/Volumes/Dev T7/vscode/projects/Pythonvscode/Python Modules/Pygamemodule/PygameForBeginners-main/Assets/spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),90)
RED_SPACESHIP_IMAGE=pygame.image.load(os.path.join('/Volumes/Dev T7/vscode/projects/Pythonvscode/Python Modules/Pygamemodule/PygameForBeginners-main/Assets/spaceship_red.png'))
RED_SPACESHIP=pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),270)

#Background image path
SPACE=pygame.transform.scale(pygame.image.load(os.path.join('/Volumes/Dev T7/vscode/projects/Pythonvscode/Python Modules/Pygamemodule/PygameForBeginners-main/Assets/space.png')),(WIDTH,HEIGHT))


#Draw function used to handle every display during the game
def draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health): #CORRECT
    WIN.blit(SPACE,(0,0)) #BLIT is used to display the images
    pygame.draw.rect(WIN,BLACK,BORDER)
    #display of health of both players
    red_health_text=HEALTH_FONT.render("Health: "+str(red_health),1,WHITE)
    yellow_health_text=HEALTH_FONT.render("Health "+str(yellow_health),1,WHITE)
    WIN.blit(red_health_text,(WIDTH - red_health_text.get_width()-10,10))
    WIN.blit(yellow_health_text,(10,10))

    #Display of the spaceships
    WIN.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))
    WIN.blit(RED_SPACESHIP,(red.x,red.y))


    #drawing bullets on the screen
    for bullet in red_bullets:
        pygame.draw.rect(WIN,RED,bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN,YELLOW,bullet)

    #Changes on display wont show until the display is updated  SO UPDATE DISPLAY IN EVERY LOOP
    pygame.display.update()

#FUNCTION TO HANDLE MOVEMENT OF THE YELLOW SHIP
def yellow_handle_movement(keys_pressed,yellow): # CORRECT
    if keys_pressed[pygame.K_a] and yellow.x-VEL>0: #left
            yellow.x-=VEL
    if keys_pressed[pygame.K_d] and yellow.x+VEL+yellow.width<BORDER.x: #Right
            yellow.x+=VEL
    if keys_pressed[pygame.K_w] and yellow.y-VEL>0: #UP
            yellow.y-=VEL
    if keys_pressed[pygame.K_s] and yellow.y+VEL+yellow.height<HEIGHT-20: #DOWN
            yellow.y+=VEL
        
#FUNCTION TO HANDLE MOVEMENT OF RED SHIP
def red_handle_movement(keys_pressed,red): #CORRECT
    if keys_pressed[pygame.K_LEFT] and red.x-VEL>BORDER.x+BORDER.width: #left
            red.x-=VEL
    if keys_pressed[pygame.K_RIGHT] and red.x+VEL+red.width<WIDTH: #Right
            red.x+=VEL
    if keys_pressed[pygame.K_UP] and red.y-VEL>0: #UP
            red.y-=VEL
    if keys_pressed[pygame.K_DOWN] and red.y+VEL+red.height<HEIGHT-20: #DOWN
            red.y+=VEL

#FUNCTION TO HANDLE BULLET MOVEMENTS
def handle_bullets(yellow_bullets,red_bullets,yellow,red):  #CORRECT
    for bullet in yellow_bullets:
        bullet.x +=BULLET_VEL #X MOVEMENT OF THE BULLETS
        if red.colliderect(bullet): #WHAT TO DO WHEN BULLETS COLLIDE WITH OPPONENTS SHIP
            pygame.event.post(pygame.event.Event(RED_HIT)) #CALL RED HIT EVENT FROM ABOVE
            yellow_bullets.remove(bullet) # REMOVE THE BULLET FROM THE SCREEN
        elif bullet.x>WIDTH: #WHEN BULLET CROSSES THE BORDERS OF THE SCREEN
            yellow_bullets.remove(bullet)


    for bullet in red_bullets:
        bullet.x -=BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x<0:
            red_bullets.remove(bullet)

#FUNCTION TO DRAW WINNER TEXT
def draw_winner(text):
    draw_text=WINNER_FONT.render(text,1,WHITE) #RENDER WINNER TEXT FONT
    WIN.blit(draw_text,(WIDTH/2-draw_text.get_width()/2,HEIGHT/2-draw_text.get_height()/2))
    pygame.display.update()#UPDATING THE DISPLAY
    pygame.time.delay(5000)#TIME TO DISPLAY THE TEXT IN MILI SECONDS





#MAIN FUNCTION WHICH CALLS ALL THE OTHER FUNCTIONS AND HANDLES EVERY ASPECT OF THE GAME
def main(): #correct
    red =pygame.Rect(700,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    yellow =pygame.Rect(100,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)

    #bullets=[]
    red_bullets=[]
    yellow_bullets=[]

    red_health=10
    yellow_health=10


    clock=pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run =False
                pygame.quit()

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LSHIFT and len(yellow_bullets)<MAX_BULLETS:
                    bullet=pygame.Rect(yellow.x+yellow.width,yellow.y+yellow.height//2-2,10,5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()


                if event.key==pygame.K_RSHIFT and len(red_bullets)<MAX_BULLETS:
                    bullet=pygame.Rect(red.x,red.y+red.height//2-2,10,5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()


            if event.type==RED_HIT:
                red_health-=1
                BULLET_HIT_SOUND.play()
            if event.type==YELLOW_HIT:
                yellow_health-=1
                BULLET_HIT_SOUND.play()


        winner_text=""
        if red_health<=0:
            winner_text="YELLOW WINS!!"

        if yellow_health<=0:
            winner_text="RED WINS!!"

        if winner_text!="":
            draw_winner(winner_text)
            break


        keys_pressed=pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed,yellow)
        red_handle_movement(keys_pressed,red)

        handle_bullets(yellow_bullets,red_bullets,yellow,red)
       

        draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health)

        
    
    main()
if __name__=="__main__":
    main()

