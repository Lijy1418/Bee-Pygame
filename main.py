import pygame
import random 
# important step so the program inhert all the methods
pygame.init()


height, width = 800,800
screen = pygame.display.set_mode((width, height))
# change the title 
pygame.display.set_caption('Roses')


# Read 






#fa,d
beeImg = pygame.image.load('smiling.png')
background = pygame.image.load('bg.jpg')
bomb = pygame.image.load('bomb.png')
roseImg = pygame.image.load('rose.png')
minusImg = pygame.image.load('minus.png')
#flip
fbeeImg = pygame.transform.flip(beeImg,True,False)
image = beeImg


def objectX(obj, position): 
   
   if(position[0] == 'L'): #left section 
      return 0
   
   elif(position[0] == 'R'): #right section
      return screen.get_width() - obj.get_width()
   
   elif(position[0] == 'C'): #at center 
      return (screen.get_width()/2) - (obj.get_width()/2)
   
   return 0


def objectY(obj, position):
   
   if(position[0]== 'U'): # upper section
      return 0 
   
   elif (position[0] == 'D'):# down section
      return screen.get_height() - obj.get_height()
   
   elif(position[0] == 'C'):# center 
      return (screen.get_height()/2) - (obj.get_height()/2)
   return 0



def move(image, x,y):
    screen.blit(image,(x,y))


def check(rect1 , rect2): 

   if (rect1.colliderect(rect2)):
      return True
   else:
       return False
   

def showText(txt, position):
   output= font.render(txt, True, (255,255,255) )
   x,y = objectX(output, position[0]), objectY(output,position[1])
   move(output,x,y)

                          
                                   

   


class Entity: 
   
   def __init__(self, img): 
      self.x = [] 
      self.y = [] 
      self.img = img 
      self.speed = []
      self.rightMost = objectX(self.img, 'R')
      self.images = [] 
      self.rect = img.get_rect()
      (self.CenterX, self.CenterY) = self.rect.center   

   def addValues(self, x, y, speed = random.uniform(0.1,0.8)):
            self.x.append(x)
            self.y.append(y)
            self.images.append(self.img)
            self.speed.append(speed)  
   
   def rectValues(self, i):
      self.rect.x, self.rect.y = self.x[i], self.y[i]

   def moveObjects(self):
    for i in range(len(self.images)):
       self.y[i]+=self.speed[i]
       if(self.y[i] > screen.get_height()):
         self.y[i] = -1*(self.img.get_height())
         self.x[i] = random.randrange(0,self.rightMost)
         self.speed[i] = random.uniform(0.1,0.8)
       move(self.images[i],self.x[i], self.y[i])  





bee_ = Entity(beeImg)
bee_.addValues(objectX(bee_.img, 'C'), (screen.get_height())- (3 * beeImg.get_height()), 0)
bee_.direction = True



rose_ = Entity(roseImg)
for i in range(3): 
   rose_.addValues(random.randrange(0,rose_.rightMost), 0,random.uniform(0.1,0.8))



minus_ = Entity(minusImg)
minus_.addValues(bee_.x[0], bee_.y[0], 0.5)
minus_.shooting = [False]



bomb_ = Entity(bomb)
bomb_.addValues(random.randrange(0,bomb_.rightMost), 0)





gameOver = False


#Result:
score =0
font = pygame.font.Font('freesansbold.ttf', 32)
 





                                  


#to hold the window
running = True
while running:

    
    #background settings
    screen.fill((66, 66, 66))
    screen.blit(background, (0,0))

     
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



            #moving objects 
              #LEFT
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                bee_.images[0] = fbeeImg
                bee_.speed[0] = -0.5



               #RIGHT 
            if event.key == pygame.K_RIGHT:
                bee_.images[0] = beeImg
                bee_.speed[0] = 0.5



               #SPACE 
            if event.key == pygame.K_SPACE:
                 i =0 
                 while(i< len(minus_.images)):
                     if(not minus_.shooting[i]):
                       minus_.shooting[i] = True
                       minus_.x[i] = bee_.x[0]
                       i+=1 
                     i+=1 
                 if(i == len(minus_.images)):
                     minus_.addValues(bee_.x[0], bee_.y[0], 0.5)
                     minus_.shooting.append(True)

        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_LEFT and bee_.speed[0] != 0.5) or (event.key == pygame.K_RIGHT and bee_.speed[0] != - 0.5): 
             bee_.speed[0] = 0 

               

    if(gameOver):
      showText("Game Over", 'CC')
    else:   
     #bee 
    
     bee_.x[0] += bee_.speed[0]
     if(bee_.x[0] < -1 * bee_.img.get_width()): 
        bee_.x[0] = screen.get_width()
     if(bee_.x[0] > screen.get_width() ): 
        bee_.x[0] = -1 * bee_.img.get_width()
     move(bee_.images[0],bee_.x[0], bee_.y[0])
     
 

     #rose
     rose_.moveObjects()
     #bomb
     bomb_.moveObjects()
 
     

     #minus 
     i =0 
     while (i < len(minus_.images)): 
        if(minus_.shooting[i]):
         minus_.y[i] -= 0.5   
         move(minus_.images[i],minus_.x[i], minus_.y[i])
         if(minus_.y[i] <=0 ): 
          minus_.images.pop(i)
          minus_.x.pop(i)
          minus_.y.pop(i)
          minus_.shooting.pop(i)
          i= i-1
        i+=1
          



     #check rose and minus
     for i in range (3): 
        for j in range(len(minus_.images)): 
          rose_.rectValues( i)
          minus_.rectValues(j)
          if(check(minus_.rect,rose_.rect) and minus_.shooting[j]):
           rose_.x[i], rose_.y[i] = random.randrange(0,rose_.rightMost), -10
           rose_.speed[i] = random.uniform(0.1,0.8)
           minus_.y[j]= bee_.y[0]
           minus_.shooting[j] = False
           score+=1 



     #check bomb and minus 
     for i in range(len(minus_.images)):
      bomb_.rectValues( 0)
      minus_.rectValues(i)
      if(check(bomb_.rect, minus_.rect) and minus_.shooting[i]):
        bomb_.x[0], bomb_.y[0] = random.randrange(0,bomb_.rightMost), -10
        bomb_.speed[0] = random.uniform(0.1,0.8)
        gameOver = True



    showText("Score = "+str(score),'LU')
    



    pygame.display.update()










