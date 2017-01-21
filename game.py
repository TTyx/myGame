'''
import pygame
import time
import random

pygame.init()

display_width = 800
display_height = 600

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

block_color = (53,115,255)

car_width = 73

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()

carImg = pygame.image.load('racecar.png')


def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged: "+str(count), True, black)
    gameDisplay.blit(text,(0,0))

def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])

def car(x,y):
    gameDisplay.blit(carImg,(x,y))

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()
    time.sleep(2)
    game_loop()

def crash():
    message_display('You Crashed')
    
def game_loop():
    x = (display_width * 0.45)
    y = (display_height * 0.8)

    x_change = 0

    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 4
    thing_width = 100
    thing_height = 100

    thingCount = 1
    dodged = 0
    gameExit = False

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change
        gameDisplay.fill(white)

        #things(thingx, thingy, thingw, thingh, color)
        things(thing_startx, thing_starty, thing_width, thing_height, block_color)

        thing_starty += thing_speed
        car(x,y)
        things_dodged(dodged)

        if x > display_width - car_width or x < 0:
            crash()

        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0,display_width)
            dodged += 1
            thing_speed += 1
            thing_width += (dodged * 1.2)

        if y < thing_starty+thing_height:
            print('y crossover')

            if x > thing_startx and x < thing_startx + thing_width or x+car_width > thing_startx and x + car_width < thing_startx+thing_width:
                print('x crossover')
                crash()
        
        pygame.display.update()
        clock.tick(60)

game_loop()
pygame.quit()
quit()

'''




'''
Map Rendering Demo
rendermap.py
By James Walker (trading as Ilmiont Software).
Copyright (C)Ilmiont Software 2013. All rights reserved.

This is a simple program demonstrating rendering a 2D map in Python with Pygame from a list of map data.
Support for isometric or flat view is included.
'''

import pygame
from pygame.locals import *
import sys

pygame.init()

xWindow = 510
yWindow = 960

DISPLAYSURF = pygame.display.set_mode((yWindow, xWindow), RESIZABLE)#, pygame.FULLSCREEN)    #set the display mode, window title and FPS clock
pygame.display.set_caption('Map Rendering Demo')
FPSCLOCK = pygame.time.Clock()

map_data = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 1, 2, 0, 0, 0, 2, 2, 2, 30, 0, 0, 0, 0],
[0, 3, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
[0, 0, 1, 0, 0, 0, 1, 3, 0, 3, 1, 0, 0, 0, 0],
[0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 2, 0, 0, 0],
[0, 0, 1, 3, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1],
[0, 0, 1, 2, 3, 0, 1, 0, 0, 0, 3, 2, 3, 0, 0],
[0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 3, 0, 2, 1, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 1, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 3, 1, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 3, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 2, 3, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]               #the data for the map expressed as [row[tile]].

dirt = pygame.image.load('dirt.png').convert_alpha()  #load images
grass = pygame.image.load('grass.png').convert_alpha()
trench = pygame.image.load('trench.png').convert_alpha()
LPF = pygame.image.load('LPF.png').convert_alpha()

tileWidth = 64  #holds the tile width and height
tileHeight = 64

currentRow = -7  #holds the current map row we are working on (y)
currentTile = 7 #holds the current tile we are working on (x)

for row in map_data:    #for every row of the map...
    for tile in row:
        if tile == 0:
            tileImage = grass
        elif tile == 1:
            tileImage = dirt
        elif tile == 2:
            tileImage = trench
        elif tile == 3:
            tileImage = LPF
        #print(tile)
        cartx = currentTile * tileWidth      #x is the index of the currentTile * the tile width
        #print(cartx)
        carty = currentRow * tileHeight      #y is the index of the currentRow * the tile height
        #print(carty)
        x = (cartx - carty) / 2
        #print(x)
        y = (cartx + carty) / 4
        #print(y)
        #print('\n\n')
        currentTile += 1    #increase the currentTile holder so we know that we are starting rendering a new tile in a moment

        DISPLAYSURF.blit(tileImage, (x, y)) #display the actual tile
    currentTile = 7 #reset the current working tile to 0 (we're starting a new row remember so we need to render the first tile of that row at index 0)
    currentRow += 1 #increment the current working row so we know we're starting a new row (used for calculating the y coord for the tile)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

    pygame.display.flip()
    FPSCLOCK.tick(30)

game_loop()
pygame.quit()
quit()
