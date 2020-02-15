from pygame.locals import *
import pygame




class Snake:

    # step : the pixels of one move
    step = 30

    # position saves the coordinate of each section of the snake body
    position = []

    # 
    legacy = 0
    tmp_legacy = 0

    # moving speed of x axis and y axis, [step, 0] stands for right direction
    speed = [step, 0]

    # image of snake body
    snake_body = pygame.image.load("images/snake_body.png")

    # image of snake head
    snake_head = pygame.image.load("images/head.png")

    # length of snake
    length = 0

    def __init__(self, length):
        self.length = length
        for i in range(0, length):
            self.position.append([self.step * 3 - self.step * i, 300])

    def update(self):
        self.tmp_legacy += 1
        if self.tmp_legacy >= self.legacy:
            for i in range(len(self.position) - 1, 0, -1):
                self.position[i][0] = self.position[i-1][0]
                self.position[i][1] = self.position[i-1][1]
            self.position[0][0] += self.speed[0]
            self.position[0][1] += self.speed[1]
            self.tmp_legacy = 0

    def draw(self, surface):
        surface.blit(self.snake_head, tuple(self.position[0]))
        for i in range(1, len(self.position)):
            surface.blit(self.snake_body, tuple(self.position[i]))


            
# background color 
black = (0, 0, 0)

# window size
weight = 1000
height = 700
size = (weight, height)

# init a screen
pygame.init() 
screen = pygame.display.set_mode(size) 

# set window's title
pygame.display.set_caption("Sunikieee") 

while 1:
    """
    keep updating the screen to make an animation 
    """


    for event in pygame.event.get():
        """
        make the close botton of window valid
        """
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    screen.fill(black)
    pygame.display.flip()
    