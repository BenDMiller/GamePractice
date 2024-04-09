import pygame, sys, time, random, math, os

#Initiate Pygame----------------------------------------------------------------

pygame.init()

#Set Up Display-----------------------------------------------------------------

display_width = 1000
display_height = 800
HW, HH = display_width/2, display_height/2

gameDisplay = pygame.display.set_mode((display_width, display_height),pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
pygame.display.set_caption('Farlands')
pygame.display.set_icon(pygame.image.load('Images/GameIcon.bmp'))

#Clock--------------------------------------------------------------------------

clock = pygame.time.Clock()
FPS = 30



#Colors           R   G   B   --------------------------------------------------
black       =   (  0,  0,  0)
white       =   (255,255,255)
red         =   (200,  0,  0)
green       =   (  0,200,  0)
blue        =   (  0,  0,200)
bright_red  =   (255,  0,  0)
bright_green=   (  0,255,  0)
bright_blue =   (  0,  0,255)

#Various Variables--------------------------------------------------------------

title_width = 800
title_height = 200
mainmenubutton_width = 350
mainmenubutton_height= 60
charview_width = 190
charview_height = 340
viewbase_width = 300
viewbase_height = 150
arrowbutton_width = 60
arrowbutton_height = 60
customizebar_height = 150
customizebar_length = 1000
customizebutton_size = 120

#Fonts--------------------------------------------------------------------------

basic_font = pygame.font.Font('freesansbold.ttf', 30)

#Images-------------------------------------------------------------------------

gametitle = pygame.image.load('Images/Title.bmp').convert_alpha()

#Button Images--------------------------------------------------------------
mainmenubuttoniaImg = pygame.image.load('Images/ButtonBackgroundia.bmp').convert_alpha()
mainmenubuttonaImg = pygame.image.load('Images/ButtonBackgrounda.bmp').convert_alpha()
leftarrowia = pygame.image.load('Images/LeftArrowButtonia.bmp').convert_alpha()
leftarrowa = pygame.image.load('Images/LeftArrowButtona.bmp').convert_alpha()
rightarrowia = pygame.image.load('Images/RightArrowButtonia.bmp').convert_alpha()
rightarrowa = pygame.image.load('Images/RightArrowButtona.bmp').convert_alpha()
customizeracebutton = pygame.image.load('Images/CustomizeRaceButton.bmp').convert_alpha()
customizesavebutton = pygame.image.load('Images/CustomizeSaveButton.bmp').convert_alpha()
customizehairbutton = pygame.image.load('Images/CustomizeHairButton.bmp').convert_alpha()
customizefacebutton = pygame.image.load('Images/CustomizeFaceButton.bmp').convert_alpha()
customizeshirtbutton = pygame.image.load('Images/CustomizeShirtButton.bmp').convert_alpha()
customizepantsbutton = pygame.image.load('Images/CustomizePantsButton.bmp').convert_alpha()

    #Tutorial/Spritesheet Images------------------------------------------------

grasstile = pygame.image.load('Images/grasstile.bmp').convert_alpha()
spritesheet = pygame.image.load('Images/link2_spritesheet.bmp').convert_alpha()

    #Character Images-----------------------------------------------------------
        #Human------------------------------------------------------------------
humancharImg = pygame.image.load('Images/HumanBase.bmp').convert_alpha()
humancharviewImg = pygame.image.load('Images/HumanBaseView.bmp').convert_alpha()
humanshirt1Img = pygame.image.load('Images/HumanShirt1.bmp').convert_alpha()
humanshirt2Img = pygame.image.load('Images/HumanShirt2.bmp').convert_alpha()

    #Other Images---------------------------------------------------------------
viewbaseImg = pygame.image.load('Images/ViewBase.bmp').convert_alpha()
barbackground = pygame.image.load('Images/CharacterCustomizationBarBackground.bmp').convert_alpha()
arrow = pygame.image.load('Images/Arrow.bmp').convert_alpha()

#Spritesheet Class--------------------------------------------------------------

class spritesheet:
    def __init__(self, filename, cols, rows):
        
        self.sheet = pygame.image.load(filename).convert_alpha()
        
        self.cols = cols
        self.rows = rows
        self.totalCellCount = cols*rows
        
        self.rect = self.sheet.get_rect()
        w = self.cellWidth = self.rect.width / cols
        h = self.cellHeight = self.rect.height / rows
        hw, hh = self.cellCenter = (w/2, h/2)
        
        
        self.cells = list([(index%cols*w, index/cols*h, w, h) for index in range(self.totalCellCount)])
        
        #Idle Images------------------------------------------------------------
        
        self.idle_north = list([0*cols])
        self.idle_east = list([1*cols])
        self.idle_south = list([2*cols])
        self.idle_west = list([3*cols])
        
        #Other Images-----------------------------------------------------------
        
        self.north = list([0,1,2,3,4,5,6,7,8,9,10,11,48,49,50,51,52,53,54,55,56,57,58,59])
        self.east = list([12,13,14,15,16,17,18,19,20,21,22,23,60,61,62,63,64,65,66,67,68,69,70,71])
        self.south = list([24,25,26,27,28,29,30,31,32,33,34,35,72,73,74,75,76,77,78,79,80,81,82,83])
        self.west = list([36,37,38,39,40,41,42,43,44,45,46,47,84,85,86,87,88,89,90,91,92,93,94,95])
        
        self.handle = list([
            (0,0), (-hw, 0), (-w, 0),
            (0, -hh), (-hw, -hh), (-w, -hh),
            (0, -h), (-hw, -h), (-w, -h),])
            
        
    def draw(self, surface, cellindex, x, y, handle = 0):
                         
        self.charx += self.x_change
        self.chary += self.y_change    
        
        surface.blit(self.sheet, (self.charx + self.handle[handle][0], self.chary + self.handle[handle][1]), self.cells[cellindex])

#Arrow/Projectile Code----------------------------------------------------------

arrows_shot = list()
speed = 20
degrees = 0
d2r = (math.pi *2)/360
short = 10
medium = 20
far = 40

class shot_arrow:
    def __init__(self, image, x, y, distance, degrees):
        mx,my = pygame.mouse.get_pos()
        radians = math.atan2(my-y, mx-x)
        self.image = image
        self.x = x
        self.y = y
        self.degrees = degrees
        self.distance = distance
        self.rotated = pygame.transform.rotate(self.image, self.degrees).convert_alpha()
        self.rect = self.rotated.get_rect()
        self.dx = math.cos(radians)
        self.dy = math.sin(radians)

def shoot_arrow(x,y):
    
    mx,my = pygame.mouse.get_pos()
    radians = math.atan2(my-y, mx-x)
    degrees = (radians / -d2r)
    
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            a = shot_arrow(arrow, x, y, far, degrees)
            arrows_shot.append([a.x, a.y, a.degrees, a.distance, a.rotated, a.rect, a.dx, a.dy])
    for i in arrows_shot:
        gameDisplay.blit(i[4],(i[0]-(i[5].center[0]),i[1]-(i[5].center[1])))
        
        if i[3] != 0:
            i[3] -=1
            i[0] += i[6]*speed
            i[1] += i[7]*speed
        elif i[3] == 0:
            arrows_shot.remove(i)


#Button Definitions-------------------------------------------------------------

def text_button(ia,a,x,y,w,h,action,text,font):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    surfaceText = font.render(text, True, black)
    textRect = surfaceText.get_rect()
    text_x_pos = x+(w/2)-(textRect[2]/2)
    text_y_pos = y+(h/2)-(textRect[3]/2)
    
    if x+w>mouse[0]>x and y+h > mouse[1] > y:
        gameDisplay.blit(a,(x,y))
        gameDisplay.blit(surfaceText,((text_x_pos, text_y_pos)))
        if click[0] == 1 and action != None:
            action()
    else:
        gameDisplay.blit(ia,(x,y))
        gameDisplay.blit(surfaceText,((text_x_pos, text_y_pos)))
          
def button(ia,a,x,y,w,h,action):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed() 
    
    if x+w>mouse[0]>x and y+h > mouse[1] > y:
        gameDisplay.blit(a,(x,y))
        
        if click[0] == 1 and action != None:
            action()
    else:
        gameDisplay.blit(ia,(x,y))

#Main Menu Loop-----------------------------------------------------------------                    
                                                                  
def main_menu():
    
    gameDisplay.fill(white)
    gameDisplay.blit(gametitle,((display_width/2)-(title_width/2),0))
    
    pygame.display.update()
    
    time.sleep(.1)
          
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
                     
        text_button(mainmenubuttoniaImg, mainmenubuttonaImg,(display_width/2)-(mainmenubutton_width/2),(0+title_height+100),mainmenubutton_width,mainmenubutton_height,playgame_button,"Play Game",basic_font)                
        text_button(mainmenubuttoniaImg, mainmenubuttonaImg,(display_width/2)-(mainmenubutton_width/2),(0+title_height+100+mainmenubutton_height+20),mainmenubutton_width,mainmenubutton_height,tutorial,"Tutorial",basic_font) 
        text_button(mainmenubuttoniaImg, mainmenubuttonaImg,(display_width/2)-(mainmenubutton_width/2),(0+title_height+100+(mainmenubutton_height*2)+(20*2)),mainmenubutton_width,mainmenubutton_height,options,"Options",basic_font)
        text_button(mainmenubuttoniaImg, mainmenubuttonaImg,(display_width/2)-(mainmenubutton_width/2),(0+title_height+100+(mainmenubutton_height*3)+(20*3)),mainmenubutton_width,mainmenubutton_height,exit_game,"Exit",basic_font)
        
        
        pygame.display.update()
        
#Playgame Button Loop-----------------------------------------------------------        
        
def playgame_button():
    
    gameDisplay.fill(white)
    gameDisplay.blit(gametitle,((display_width/2)-(title_width/2),0))
    
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
            
        text_button(mainmenubuttoniaImg, mainmenubuttonaImg,(display_width/2)-(mainmenubutton_width/2),(0+title_height+100),mainmenubutton_width,mainmenubutton_height,playgame_button,'Slot 1',basic_font)
        text_button(mainmenubuttoniaImg, mainmenubuttonaImg,(display_width/2)-(mainmenubutton_width/2),(0+title_height+100+mainmenubutton_height+10),mainmenubutton_width,mainmenubutton_height,playgame_button,'Slot 2',basic_font)
        text_button(mainmenubuttoniaImg, mainmenubuttonaImg,(display_width/2)-(mainmenubutton_width/2),(0+title_height+100+(mainmenubutton_height*2)+(10*2)),mainmenubutton_width,mainmenubutton_height,playgame_button,'Slot 3',basic_font)
        text_button(mainmenubuttoniaImg, mainmenubuttonaImg,(display_width/2)-(mainmenubutton_width/2),(0+title_height+100+(mainmenubutton_height*3)+(10*3)),mainmenubutton_width,mainmenubutton_height,create_character,'Create Character',basic_font)
        text_button(mainmenubuttoniaImg, mainmenubuttonaImg,(display_width/2)-(mainmenubutton_width/2),(0+title_height+100+(mainmenubutton_height*4)+(10*4)),mainmenubutton_width,mainmenubutton_height,playgame_button,'Delete Character',basic_font)
        text_button(mainmenubuttoniaImg, mainmenubuttonaImg,(display_width/2)-(mainmenubutton_width/2),(0+title_height+100+(mainmenubutton_height*5)+(10*5)),mainmenubutton_width,mainmenubutton_height,main_menu,'Back',basic_font)
        
        pygame.display.update()


#Tutorial Loop------------------------------------------------------------------

def tutorial():
    gameDisplay.fill(white)

    #Spritesheet Info-----------------------------------------------------------    
            
    s = spritesheet('Images/link2_spritesheet.png', 12, 8)
    
    s.charx = HW
    s.chary = HH
    s.x_change = 0
    s.y_change = 0
    left_key = 0
    right_key = 0
    up_key = 0
    down_key = 0
    s.speed = 10
    
    mx,my = pygame.mouse.get_pos()
    radians = math.atan2(my-s.chary, mx-s.charx)
    degrees = (radians / -d2r)
    
    Center_Handle = 4
    
    char_direction = s.idle_south    
    
    index = 0
    
    
    while True:        
        mx,my = pygame.mouse.get_pos()
        radians = math.atan2(my-s.chary, mx-s.charx)
        degrees = (radians / -d2r)
        for event in pygame.event.get():
            
    #Exit-----------------------------------------------------------------------        
            
            if event.type == pygame.QUIT:
                 pygame.quit()
                 sys.exit() 
          
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a: #Left/West
                    if s.charx > 0:
                        if right_key == 1:
                            s.x_change -= s.speed*2
                        else:    
                            s.x_change -= s.speed
                    else:
                        s.x_change =0
                    left_key = 1
                    char_direction = s.west
                if event.key == pygame.K_d: #Right/East
                    if left_key == 1:
                        s.x_change += s.speed*2 
                    else:
                        s.x_change += s.speed 
                    right_key = 1
                    char_direction = s.east
                if event.key == pygame.K_w: #Up/North
                    if down_key == 1:
                        s.y_change -= s.speed*2    
                    else:   
                        s.y_change -= s.speed
                    up_key = 1
                    char_direction = s.north
                if event.key == pygame.K_s: #Down/South
                    if up_key == 1:
                        s.y_change += s.speed*2
                    else:    
                        s.y_change += s.speed
                    down_key = 1
                    char_direction = s.south
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a: #Left
                    if right_key == 1 and s.x_change <= -s.speed:
                        s.x_change += s.speed*2
                    elif right_key == 1 and s.x_change == s.speed:
                        s.x_change += 0
                    else:    
                        s.x_change += s.speed
                    left_key = 0
                    if up_key == 1:
                        char_direction = s.north
                    elif down_key == 1:
                        char_direction = s.south
                    elif right_key == 1:
                        char_direction = s.east
                    else:
                        char_direction = s.idle_west
                        index = 0 
                if event.key == pygame.K_d: #Right
                    if left_key == 1 and s.x_change >= s.speed:
                        s.x_change -= s.speed*2    
                    elif left_key == 1 and s.x_change == -s.speed:
                        s.x_change -= 0
                    else:    
                        s.x_change -= s.speed 
                    right_key = 0
                    if up_key == 1:
                        char_direction = s.north
                    elif down_key == 1:
                        char_direction = s.south
                    elif left_key == 1:
                        char_direction = s.west
                    else:
                        char_direction = s.idle_east
                        index = 0
                if event.key == pygame.K_w: #Up
                    if down_key == 1 and s.y_change <= -s.speed:
                        s.y_change += s.speed*2
                    elif down_key == 1 and s.y_change == s.speed:
                        s.y_change += 0
                    else:
                        s.y_change += s.speed
                    up_key = 0
                    if left_key == 1:
                        char_direction = s.west
                    elif right_key == 1:
                        char_direction = s.east
                    elif down_key == 1:
                        char_direction = s.south
                    else:
                        char_direction = s.idle_north
                        index = 0
                if event.key == pygame.K_s: #Down
                    if up_key == 1 and s.y_change >= s.speed:
                        s.y_change -= s.speed*2
                    elif up_key == 1 and s.y_change == -s.speed:
                        s.y_change -= 0    
                    else:    
                        s.y_change -= s.speed
                    down_key = 0
                    if left_key == 1:
                        char_direction = s.west
                    elif right_key == 1:
                        char_direction = s.east 
                    elif up_key == 1:
                        char_direction = s.north  
                    else:
                        char_direction = s.idle_south
                        index = 0        
            if event.type == pygame.MOUSEBUTTONDOWN:
                a = shot_arrow(arrow, s.charx, s.chary, far, degrees)
                arrows_shot.append([a.x, a.y, a.degrees, a.distance, a.rotated, a.rect, a.dx, a.dy])   
            
                                                        
        #Blitting---------------------------------------------------------------                 
                                                                   
        gameDisplay.fill(white)
        
        for x in range(int(display_width/60)):
            for y in range(int(display_height/60)):
                gameDisplay.blit(grasstile,(x*64,y*64))

        #shoot_arrow(s.charx, s.chary)
        
        for i in arrows_shot:
            gameDisplay.blit(i[4],(i[0]-(i[5].center[0]),i[1]-(i[5].center[1])))
        
            if i[3] != 0:
                i[3] -=1
                i[0] += i[6]*speed
                i[1] += i[7]*speed
            elif i[3] == 0:
                arrows_shot.remove(i)
        
        #Spritesheet------------------------------------------------------------
        
        s.draw(gameDisplay, char_direction[index % (s.cols*2)], s.charx, s.chary, Center_Handle) 
        
        if left_key == 1 or right_key == 1 or up_key == 1 or down_key == 1 and index != s.cols*2 :
            index = index%(s.cols*2) + 1
        else:
            index = 0
        
        clock.tick(FPS)
        
        #gameDisplay.blit(charpic,(charx,chary))
        pygame.display.update()

#Options Loop-------------------------------------------------------------------                  
                                                         
def options():
    gameDisplay.fill(white)
    gameDisplay.blit(gametitle,((display_width/2)-(title_width/2),0))
    
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

#Exit Game----------------------------------------------------------------------

def exit_game():
    pygame.quit()
    sys.exit()

#Create Character Loop----------------------------------------------------------

def create_character():
    gameDisplay.fill(white)
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()  
    
    human_shirts = (humanshirt1Img, humanshirt2Img)
    
    
    view_x = (display_width/2)-(charview_width/2)
    view_y = (display_height/2)-(charview_height/2)
    
    gameDisplay.blit(barbackground,(0,0))
    
    gameDisplay.blit(customizeracebutton,(16,customizebar_height/10))
    gameDisplay.blit(customizehairbutton,(customizebutton_size+(16.5*2)+(display_width/30),customizebar_height/10))
    gameDisplay.blit(customizehairbutton,(customizebutton_size*2+(16.5*3)+(display_width/30)*2,customizebar_height/10))
    gameDisplay.blit(customizehairbutton,(customizebutton_size*3+(16.5*4)+(display_width/30)*3,customizebar_height/10))
    gameDisplay.blit(customizehairbutton,(customizebutton_size*4+(16.5*5)+(display_width/30)*4,customizebar_height/10))
    gameDisplay.blit(customizesavebutton,(customizebutton_size*5+(16.5*6)+(display_width/30)*5,customizebar_height/10))
    
    gameDisplay.blit(viewbaseImg,((display_width/2)-(viewbase_width/2),(display_height/2)-((viewbase_height/2)-(charview_height/2)-20)))
    gameDisplay.blit(humancharviewImg,(view_x,view_y))
    gameDisplay.blit(human_shirts[1],(view_x,view_y))
    
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        
        
        gameDisplay.blit(viewbaseImg,((display_width/2)-(viewbase_width/2),(display_height/2)-((viewbase_height/2)-(charview_height/2)-20)))
        gameDisplay.blit(humancharviewImg,(view_x,view_y))
        gameDisplay.blit(human_shirts[1],(view_x,view_y))
        

        pygame.display.update()                
               
#Delete Character Loop----------------------------------------------------------               
                  
def delete_character():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()                  

#Game Loop----------------------------------------------------------------------
                                                
def game_loop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

main_menu()       