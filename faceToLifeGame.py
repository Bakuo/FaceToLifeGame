#coding: utf-8
import pygame
from pygame.locals import *
import random
import sys
#import os
#import codecs
from PIL import Image
import numpy as np

# import module that I made
import faceCamera
import detectFace

SCR_RECT = Rect(0, 0, 800, 800) # screen size depends on the size of detected face
CS = 10 # cell size
THRESHOLD = 100 # the threshold to pixelate the pic
NUM_ROW = SCR_RECT.height / CS # row of field
NUM_COL = SCR_RECT.width / CS # column of field
DEAD, ALIVE, STAY = 0, 1, 2 # constant for live or dead
RAND_LIFE = 0.1

# You can choose the file from agtFace.jpg or face.jpg
img = np.array(Image.open('face.jpg').convert('L'))

class LifeGame:
    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode(SCR_RECT.size)
        pygame.display.set_caption(u"Conway's Game of Life")
        self.font = pygame.font.SysFont(None, 16)
        # Field that has size of NUM_ROW * NUM_ROL
        self.field = [[DEAD for x in range(NUM_COL)] for y in range(NUM_ROW)]
        self.color = [[DEAD for x in range(NUM_COL)] for y in range(NUM_ROW)]
        self.generation = 0 # the number of generation
        self.time = 100
        self.run = False # run or not
        self.cursor = [NUM_COL, NUM_ROW] # the position of carsor
        # initiate the life game
        self.clear()
        # main loop
        clock = pygame.time.Clock()

        self.draw_face()

        while True:
            clock.tick(30)
            self.update()
            self.draw(screen)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    # move cursor by key
                    elif event.key == K_LEFT:
                        self.cursor[0] -= 1
                        if self.cursor[0] < 0: self.cursor[0] = 0
                    elif event.key == K_RIGHT:
                        self.cursor[0] += 1
                        if self.cursor[0] > NUM_COL-1: self.cursor[0] = NUM_COL-1
                    elif event.key == K_UP:
                        self.cursor[1] -= 1
                        if self.cursor[1] < 0: self.cursor[1] = 0
                    elif event.key == K_DOWN:
                        self.cursor[1] += 1
                        if self.cursor[1] > NUM_ROW-1: self.cursor[1] = NUM_ROW-1
                    # turn a cell when pushing space key
                    elif event.key == K_SPACE:
                        x, y = self.cursor
                        if self.field[y][x] == DEAD:
                            self.field[y][x] = ALIVE
                            self.color[y][x] = ALIVE
                        elif self.field[y][x] == ALIVE:
                            self.field[y][x] = DEAD
                    # start simulation when pushing 's' key
                    elif event.key == K_s:
                        self.run = not self.run
                    # progress just one generation by pushing 'n'
                    elif event.key == K_n:
                        self.step()
                    # clear by pushing 'c'
                    elif event.key == K_c:
                        self.clear()
                        self.run = False
                    # add a alive cell randomly by pushing 'r'
                    elif event.key == K_r:
                        self.rand()

                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    # turn a cell by pushing left click
                    px, py = event.pos
                    x, y = px/CS, py/CS
                    self.cursor = [x, y]
                    if self.field[y][x] == DEAD:
                        self.field[y][x] = ALIVE
                        self.color[y][x] = ALIVE
                    elif self.field[y][x] == ALIVE:
                        self.field[y][x] = DEAD
                elif event.type == MOUSEMOTION and event.buttons == (1,0,0):
                    px, py = event.pos
                    x, y = px/CS, py/CS
                    if self.field[y][x] == DEAD:
                        self.field[y][x] = ALIVE
                        self.color[y][x] = ALIVE
                    elif self.field[y][x] == ALIVE:
                        self.field[y][x] = DEAD

    def clear(self):
        """Initiate a game"""
        self.generation = 0
        for y in range(NUM_ROW):
            for x in range(NUM_COL):
                self.field[y][x] = DEAD
    def rand(self):
        """Add a alive cell randomly"""
        for y in range(NUM_ROW):
            for x in range(NUM_COL):
                if random.random() < RAND_LIFE:
                    self.field[y][x] = ALIVE
                    self.color[y][x] = ALIVE
    def update(self):
        pygame.time.wait(200)
        """Update the field"""
        if self.run:
            self.step() # Progress one step
    def step(self):
        """Progress one generation"""
        # next field
        next_field = [[False for x in range(NUM_COL)] for y in range(NUM_ROW)]
        # Set the field by following the rule of life game
        sum_alive_cells = 0
        for y in range(NUM_ROW):
            for x in range(NUM_COL):
                num_alive_cells = self.around(x, y)
                if num_alive_cells == 2:
                    # keep a cell if 2 cells around the cell are alive
                    next_field[y][x] = self.field[y][x]
                    self.color[y][x] = STAY
                    sum_alive_cells += 1
                elif num_alive_cells == 3:
                    # born a cell if 3 cells around the cell are alive
                    next_field[y][x] = ALIVE
                    self.color[y][x] = ALIVE
                    sum_alive_cells += 1
                else:
                    # other cells are dead
                    next_field[y][x] = DEAD
                    self.color[y][x] = DEAD
        self.field = next_field
        self.generation += 1

    def draw(self, screen):
        """Draw the field"""
        # Paint cells
        for y in range(NUM_ROW):
            for x in range(NUM_COL):
                if self.field[y][x] == ALIVE:
                    if(self.color[y][x] == ALIVE):
                        pygame.draw.rect(screen, (255,255,0), Rect(x*CS,y*CS,CS,CS))
                    elif(self.color[y][x] == STAY):
                        pygame.draw.rect(screen, (255,0,255),Rect(x*CS,y*CS,CS,CS))
                elif self.field[y][x] == DEAD:
                    pygame.draw.rect(screen, (0,255,255), Rect(x*CS,y*CS,CS,CS))
                pygame.draw.line(screen, (255,255,255), (x*CS,0),(x*CS,SCR_RECT.height))
                pygame.draw.line(screen, (255,255,255), (0,y*CS),(SCR_RECT.width,y*CS))

        # Draw cursor
        pygame.draw.rect(screen, (0,0,255), Rect(self.cursor[0]*CS,self.cursor[1]*CS,CS,CS), 1)
        # Draw the information of the game
        screen.blit(self.font.render("generation:%d" % self.generation, True, (0,0,0)), (0,0))
        screen.blit(self.font.render("space : birth/kill",True,(0,0,0,)),(0,12))
        screen.blit(self.font.render("s : start/stop",True,(0,0,0)),(0,24))
        screen.blit(self.font.render("n : next",True,(0,0,0)),(0,36))
        screen.blit(self.font.render("r : random",True,(0,0,0)),(0,48))
    
    def around(self, x, y):
        """Return the number of the alive cells around (x,y)"""
        if x == 0 or x == NUM_COL-1 or y == 0 or y == NUM_ROW-1:
            return 0
        sum = 0
        sum += self.field[y-1][x-1] # cell at the upper left
        sum += self.field[y-1][x]   # cell at upper side
        sum += self.field[y-1][x+1] # cell at the upper right
        sum += self.field[y][x-1]   # cell at the left
        sum += self.field[y][x+1]   # cell at the right
        sum += self.field[y+1][x-1] # cell at the lower left 
        sum += self.field[y+1][x]   # cell at the lower side 
        sum += self.field[y+1][x+1] # cell at the lower right
        return sum

    def draw_face(self):
        x = detectFace.detectedFace[0] - 50
        y = detectFace.detectedFace[1] - 50
        width = detectFace.detectedFace[2] + 100
        height = detectFace.detectedFace[3] + 100
        
        for i in xrange(0,NUM_ROW):
            for j in xrange(0,NUM_COL):
                searchX = x + i*width/NUM_ROW
                searchY = y + j*height/NUM_COL
                if img[searchY][searchX] < THRESHOLD:
                    self.field[j][i] = ALIVE
                    self.color[j][i] = ALIVE

if __name__ == "__main__":
    LifeGame()
