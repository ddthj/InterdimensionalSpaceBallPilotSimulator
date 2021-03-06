'''
InterDimensional Space Ball Pilot Simulator!
By ddthj/SquidFairy/GooseFairy (I have too many names)

'''
import pygame
import math

pygame.init()
window = pygame.display.set_mode((1400,840),pygame.RESIZABLE)
pygame.display.set_caption('Interdimensional Space Ball Pilot Simulator')
space = [0,0,20] #the color of space
white = [255,255,255]
instrument_panel_color = [100,100,100]
ship_color = [0,200,50]
#load images here
image_stars = pygame.image.load('stars.png')

pygame.joystick.init()
joystick_mode = False



if pygame.joystick.get_count() > 0:
    joystick_mode = True
    print("found a joystick")
else:
    print("no joystick found")



#variables for resizing everything properly
x_multi = 1      

def render(image,x,y,w,h):
    image = pygame.transform.scale(image,(w,h))
    RECT = pygame.Rect(x,y,w,h)
    window.blit(image,RECT)

def render_without_fucking_it(image,x,y):
    RECT = image.get_rect(center = (x,y))
    window.blit(image,RECT)


def rect(color, x, y, width, height):
    pygame.draw.rect(window,color,(x,y,width,height))

class sector_beacon():
    def __init__(self,x,y):
        self.type = "sb"
        self.x = x
        self.y = y
        #self.image = pygame.image.load("sb")
    def render(self,player_loc):
        #todo make this scale with window size and only render when player is nearby
        #render(self.image,self.x,self.y,30,30)
        rect(white,self.x-45+player_loc[0] +700,-self.y-45+player_loc[1]+220,90,90)
        
        
class sector_beacon_instrument():
    def __init__(self,panel_spot):
        self.base = pygame.image.load("sbi.png")
        self.needle = pygame.image.load("sbi_needle.png")
        self.panel_position = panel_spot
        self.target = 0
        self.position = 0
        self.velocity = 5 #ignore this for now lol

    def tick(self,player,objects):
        x = player.x
        y = player.y

        for item in objects:
            if item.type == "sb":
                sx = item.x
                sy = item.y

        if sx > x and sy > y:
            self.target = 135
        elif sx > x and sy < y:
            self.target = 45
        elif sx < x and sy > y:
            self.target = 225
        elif sx < x and sy < y:
            self.target = 315

        
        right_range = -1
        if self.target+180 > 359:
            right_range = self.target - 180
        if self.position > self.target or self.position < right_range and right_range != -1:
            self.position -= self.velocity
        else:
            self.position += self.velocity
        
        if self.velocity > 0 and abs(self.position - self.target) < 20:
            self.velocity -=1
            if self.velocity >1 and abs(self.position - self.target) < 10:
                self.velocity -= 2
        elif self.velocity < 20:
            self.velocity += 1
        
        if self.position > 359:
            self.position -= 360
        elif self.position < 0:
            self.position += 360
        
        
    def render(self):
        image = pygame.transform.scale(self.needle,(10,100))
        image = pygame.transform.rotate(image,self.position)
        #change w/h to match window scale at some point pls
        render(self.base,self.panel_position[0],self.panel_position[1],200,200)

        render_without_fucking_it(image,self.panel_position[0]+100,self.panel_position[1]+100)
        
        


class space_ball():
    def __init__(self,level):
        self.type = "player"
        self.voltage = 25
        self.x = 0
        self.y = 0
        self.rotation = 0
        self.layer = 0
        self.velocity = [0,0,0] #direction, speed, #rotational velocity
        self.instruments = [] # this will hold all of the active instruments
        self.instruments.append(sector_beacon_instrument((0,300)))
        if level < 5:
            self.fuel = 99999999
            self.discharge = False
        elif level > 5:
            self.fuel = 1000
            self.discharge = True
    def tick(self,inputs,objects):
        #input = x axis (forward/backward), z axis (rotation)
        #rotation speed will be inversly proportional to velocity?

        #first calculating the direction/velocity 
        self.velocity[2] = inputs[1]
        
        if self.velocity[0] + self.velocity[2] > 360:
            self.velocity[0] = self.velocity[0] + self.velocity[2] - 360
        elif self.velocity[0] + self.velocity[2] < 0:
            self.velocity[0] = self.velocity[0] + self.velocity[2] + 360
        else:
            self.velocity[0] += self.velocity[2]

        if inputs[0] > self.velocity[1]:
            self.velocity[1] += 10
        elif inputs[0] < self.velocity[1]:
            self.velocity[1] -= 10
        #print(str(self.x)+" " + str(self.y))

        #second applying the movement
        self.x += int(math.sin(math.radians(self.velocity[0]))*self.velocity[1])
        self.y += int(math.sin(math.radians(90-self.velocity[0]))*self.velocity[1])
        for item in self.instruments:
            item.tick(self,objects)
    def render(self):
        #render instrument panel
        
        rect(instrument_panel_color,0,300,1400,540)
        for item in self.instruments:
            item.render()
        #render ship
        rect(ship_color,700-50,220-50,100,100)

'''
###############################################this is where the game actually runs |
                                                                                    V
'''

player = space_ball(1)
sim_objects = []
sim_objects.append(sector_beacon(500,500))
Clock = pygame.time.Clock()
w=a=s=d=False
while 1:
    Clock.tick(20)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.VIDEORESIZE:
            print(str(event.dict['size']))
            x_multi = event.dict['size'][0]
            window = pygame.display.set_mode((event.dict['size'][0],int(float(event.dict['size'][0]) * float(3/5))),pygame.RESIZABLE)
        elif event.type == pygame.KEYDOWN:
            #print(str(event.key))
            if event.key==pygame.K_UP:# or pygame.K_w:
                w=True
            if event.key==pygame.K_DOWN:# or pygame.K_s:
                s=True
            if event.key==pygame.K_LEFT:# or pygame.K_a:
                a=True
            if event.key==pygame.K_RIGHT:# or pygame.K_d:
                d=True
        elif event.type == pygame.KEYUP:
            if event.key==pygame.K_UP:# or pygame.K_w:
                w=False
            if event.key==pygame.K_DOWN:# or pygame.K_s:
                s=False
            if event.key==pygame.K_LEFT:# or pygame.K_a:
                a=False
            if event.key==pygame.K_RIGHT:# or pygame.K_d:
                d=False            
            
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if joystick_mode:
        pass
    else:
        inputs = []
        #print(str(w))

        if w==True and s == False:
            inputs.append(100)
        elif s==True and w == False:
            inputs.append(-100)
        else:
            inputs.append(0)

        if a==True and d == False:
            inputs.append(-10)
        elif d==True and a == False:
            inputs.append(10)
        else:
            inputs.append(0)
        #print(str(inputs))
        inputs.append(mouse)
        inputs.append(click)
        player.tick(inputs,sim_objects)
    
    '''
    TO MAKE THINGS CLEAR:
    the y axis is inverted in pygame, meaning moving down = increasing y numbers. so we invert it to make things righter
    the x axis is normal, but since the map moves around the player we invert the x axis and in-invert the y axis to make things rightest
    ''' 
    fake_x = -player.x % 1400
    fake_y = player.y % 840
    
    #rendering starts in center + up down left right from center
    render(image_stars,fake_x,fake_y,1400,840)
    render(image_stars,fake_x+1400,fake_y,1400,840)
    render(image_stars,fake_x-1400,fake_y,1400,840)
    render(image_stars,fake_x,fake_y+840,1400,840)
    render(image_stars,fake_x,fake_y-840,1400,840)
    #diagonals too
    render(image_stars,fake_x-1400,fake_y+840,1400,840)
    render(image_stars,fake_x-1400,fake_y-840,1400,840)
    render(image_stars,fake_x+1400,fake_y+840,1400,840)
    render(image_stars,fake_x+1400,fake_y-840,1400,840)

    
    for item in sim_objects:
        item.render((-player.x,player.y))
    player.render()
        
    
    pygame.display.update()
    
            
    

    

