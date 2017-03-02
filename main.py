'''
InterDimensional Space Ball Pilot!
By ddthj/SquidFairy/GooseFairy (I have too many names)

more to be added

'''
import pygame
import math

pygame.init()
window = pygame.display.set_mode((1400,840),pygame.RESIZABLE)
pygame.display.set_caption('Interdimensional Space Ball Pilot Simulator')
space = [0,0,20]
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

def rect(color, x, y, width, height):
    pygame.draw.rect(window,color,(x,y,width,height))

class space_ball():
    def __init__(self,level):
        self.voltage = 25
        self.x = 0
        self.y = 0
        self.rotation = 0
        self.layer = 0
        self.velocity = [0,0,0] #direction, speed, #rotational velocity
        self.instruments = [] # this will hold all of the active instruments
        if level < 5:
            self.fuel = 99999999
            self.discharge = False
        elif level > 5:
            self.fuel = 1000
            self.discharge = True
    def tick(self,inputs):
        #input = x axis (forward/backward), z axis (rotation)
        #rotation speed will be inversly proportional to velocity

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

        #second applying the movement
        self.x += int(math.sin(math.radians(self.velocity[0]))*self.velocity[1])
        self.y += int(math.sin(math.radians(90-self.velocity[0]))*self.velocity[1])
        for item in self.instruments:
            item.tick()
            
player = space_ball(1)
sim_objects = []
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
            inputs.append(10)
        elif d==True and a == False:
            inputs.append(-10)
        else:
            inputs.append(0)
        #print(str(inputs))
        player.tick(inputs)
    render(image_stars,player.x,player.y,1400,840)
    if player.x > 0:
        render(image_stars,player.x-1400,player.y,1400,840)
    elif player.x < 0:
        render(image_stars,player.x+1400,player.y,1400,840)
        
    
    pygame.display.update()
    
            
    

    

