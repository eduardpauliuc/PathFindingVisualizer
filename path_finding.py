import pygame
import sys
import math
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os
import time

from constants import *
from algorithms import bfs, astar
from models import cell, button

pygame.font.init()


screen = pygame.display.set_mode((displayWidth, displayHeight))
screen.fill((255,255,255))

grid = [[0 for column in range(noOfColumns)] for row in range(noOfRows)]


startButton = button(grey, displayWidth / 8 - 100, 505, 100, 30, screen, text='Place start')
startButton.draw()

endButton = button(grey, displayWidth * 2 / 8 - 100, 505, 100, 30, screen, text='Place end')
endButton.draw()

clearButton = button(grey, displayWidth * 3 / 8 - 100, 505, 100, 30, screen, text='Clear')
clearButton.draw()

bfsButton = button(grey, displayWidth * 4 / 8 - 100, 505, 100, 30, screen, text='BFS search')
bfsButton.draw()

astarButton = button(grey, displayWidth * 5 / 8 - 100, 505, 100, 30, screen, text='A* search')
astarButton.draw()

slowButton = button(grey, displayWidth * 6 / 8 - 60, 505, 70, 30, screen, text='Slow')
slowButton.draw()

normalButton = button(grey, displayWidth * 7 / 8 - 100, 505, 70, 30, screen, text='Normal')
normalButton.draw(True)

fastButton = button(grey, displayWidth * 8 / 8 - 140, 505, 70, 30, screen, text='Fast')
fastButton.draw()

# Create Cells
for i in range(noOfRows):
    for j in range(noOfColumns):
        grid[i][j] = cell(i, j, screen)


# Border grid
for i in range(0,noOfRows):
   grid[i][0].make(grey)
   grid[i][0].isObstacle = True
   grid[i][noOfColumns-1].isObstacle = True
   grid[i][noOfColumns-1].make(grey)

for j in range(0,noOfColumns):
    grid[0][j].make(grey)
    grid[noOfRows-1][j].make(grey)
    grid[0][j].isObstacle = True
    grid[noOfRows-1][j].isObstacle = True


pygame.init()

start = None
end = None

running = True

previousClicked = None

animateSpeed = 0.005

placingStart = False
placingEnd = False

isAnimating = False

def clearBoard():
    global grid, sart, end
    start = None
    end = None
    for i in range(1, noOfRows-1):
        for j in range(1, noOfColumns-1):
            grid[i][j] = cell(i,j, screen)
            grid[i][j].makeEmpty()

def prepareForSearch():
    for row in range(1, noOfRows-1):
        for col in range(1, noOfColumns-1):
            if grid[row][col].isObstacle == False:
                #print((row,col))
                if grid[row][col] != end and grid[row][col] != start:
                    grid[row][col].makeEmpty()
                grid[row][col].neighbors = []
                grid[row][col].visited = False
                grid[row][col].addNeighbors(grid)


def checkForClicks():
    ev = pygame.event.get()

    for event in ev:
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            # Pause
            if event.key == pygame.K_SPACE:
                isPaused = True
                while isPaused == True:
                    e = pygame.event.get()
                    pygame.event.clear()
                    for newev in e:
                        if newev.type == pygame.KEYDOWN and newev.key == pygame.K_SPACE:
                            isPaused = False
    
    if pygame.mouse.get_pressed()[0]:
            try:
                pos = pygame.mouse.get_pos()
                mousePress(pos)
            except AttributeError:
                pass

def showVisited(visitedOrder):
    global isAnimating
    isAnimating = True
    for i in range(0, len(visitedOrder) + 4):
        
        if i <= len(visitedOrder)-1:
            visitedOrder[i].makePath()

        if i >= 5:
            visitedOrder[i-5].makeVisited()

        time.sleep(animateSpeed)
        if checkForClicks():
            return

    isAnimating = False

def showPath():
    global isAnimating
    isAnimating = True
    if end.visited == True:
        before = end.previous
        while before != start:
            before.makePath()
            before = before.previous
            time.sleep(0.02)
            if checkForClicks():
                return
    isAnimating = False

def changeSpeed(x):
    global animateSpeed

    fastButton.draw(False)
    normalButton.draw(False)
    slowButton.draw(False)

    if x == 0:
        animateSpeed = 0.05
        slowButton.draw(True)
    if x == 1:
        animateSpeed = 0.005
        normalButton.draw(True)
    if x == 2:
        animateSpeed = 0
        fastButton.draw(True)
    
    print('New speed:', animateSpeed)

def placeStart():
    global start, placingStart
    placingStart = True
    if start != None:
        start.makeEmpty()
        start = None

def placeEnd():
    global end, placingEnd
    placingEnd = True
    if end != None:
        end.makeEmpty()
        end = None

# When clicking on cells
def mousePress(x):
    global placingStart, start, placingEnd, end, animateSpeed
    
    if startButton.isOver(x) and isAnimating == False:
        placeStart()
    
    if endButton.isOver(x) and isAnimating == False:
        placeEnd()
    
    if bfsButton.isOver(x):
        if start != None and end != None:
            visitedOrder = []
            prepareForSearch()
            bfs(grid, noOfColumns, noOfRows, start, end, visitedOrder)
            showVisited(visitedOrder)
            showPath()
    
    if astarButton.isOver(x):
        if start != None and end != None:
            prepareForSearch()
            astar()
    
    if slowButton.isOver(x):
        changeSpeed(0)
    
    if normalButton.isOver(x):
        changeSpeed(1)

    if fastButton.isOver(x):
        changeSpeed(2)
    
    if clearButton.isOver(x) and isAnimating == False:
        clearBoard()
    
    # if you clicked a cell
    global previousClicked
    row = int(x[1] // (h+margin))
    col = int(x[0] // (w+margin))
    if 1 <= row < noOfRows-1 and 1 <= col < noOfColumns-1 and isAnimating == False:
        if placingStart:
            start = grid[row][col]
            start.makeStart()
            placingStart = False

        if placingEnd:
            end = grid[row][col]
            end.makeEnd()
            placingEnd = False

        acess = grid[row][col]
        if acess != start and acess != end and acess != previousClicked:
            previousClicked = acess
            if acess.isObstacle == False:
                acess.makeObstacle()
            else:
                acess.makeEmpty()


while running:
    ev = pygame.event.get()

    for event in ev:
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            exit()
        if pygame.mouse.get_pressed()[0]:
            try:
                pos = pygame.mouse.get_pos()
                mousePress(pos)
            except AttributeError:
                pass
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                placeStart()
            if event.key == pygame.K_e:
                placeEnd()
            if event.key == pygame.K_c and isAnimating == False:
                clearBoard()

pygame.quit()