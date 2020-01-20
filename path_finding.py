import pygame
import os
import time
from sys import exit

from data.const import *
from data import const
from data.algorithms import bfs, astar, dfs
from data.models import cell, button
from data.popup import changeDimensionsPopup

pygame.font.init()


screen = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption('Path finding visualizer')
pygame.display.set_icon(windowIcon)
screen.fill((255,255,255))

transformIcons()


startButton = button((128, 255, 255), displayWidth / 9 - 100, 505, 100, 30, screen, text='Place start')

endButton = button((255, 77, 77), displayWidth * 2 / 9 - 100, 505, 100, 30, screen, text='Place end')

clearButton = button(grey, displayWidth * 3 / 9 - 100, 505, 100, 30, screen, text='Clear')

dfsButton = button((255, 255, 128), displayWidth * 4 / 9 - 100, 505, 100, 30, screen, text='DFS')

bfsButton = button((255, 255, 128), displayWidth * 5 / 9 - 100, 505, 100, 30, screen, text='BFS')

astarButton = button((255, 255, 128), displayWidth * 6 / 9 - 100, 505, 100, 30, screen, text='A* search')

slowButton = button(grey, displayWidth * 7 / 9 - 50, 505, 50, 30, screen, text='Slow')

normalButton = button(grey, displayWidth * 8 / 9 - 100, 505, 50, 30, screen, text='Normal')

fastButton = button(grey, displayWidth * 9 / 9 - 152, 505, 50, 30, screen, text='Fast')

popupButton = button(grey, displayWidth * 10 / 9 - 155, 505, 28, 28, screen, text='')

def drawButtons():
    startButton.draw()
    endButton.draw()
    clearButton.draw()
    dfsButton.draw()
    bfsButton.draw()
    astarButton.draw()
    slowButton.draw()
    normalButton.draw(True)
    fastButton.draw()
    screen.blit(settingsIcon, (int(displayWidth * 9 / 8 - 170), 505))

drawButtons()
# Create Grid

grid = None

def setGrid():
    global grid

    grid = [[0 for column in range(const.noOfColumns)] for row in range(const.noOfRows)]
    for i in range(const.noOfRows):
        for j in range(const.noOfColumns):
            grid[i][j] = cell(i, j, screen)

setGrid()

def borderGrid(clear=False):
    global grid
    color = grey
    if clear:
        color = white
    # Border grid
    for i in range(0,const.noOfRows):
        grid[i][0].make(color)
        grid[i][0].isObstacle = True
        grid[i][const.noOfColumns-1].isObstacle = True
        grid[i][const.noOfColumns-1].make(color)

    for j in range(0,const.noOfColumns):
        grid[0][j].make(color)
        grid[const.noOfRows-1][j].make(color)
        grid[0][j].isObstacle = True
        grid[const.noOfRows-1][j].isObstacle = True

borderGrid()

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
    for i in range(1, const.noOfRows-1):
        for j in range(1, const.noOfColumns-1):
            grid[i][j] = cell(i,j, screen)
            grid[i][j].makeEmpty()

def prepareForSearch():
    for row in range(1, const.noOfRows-1):
        for col in range(1, const.noOfColumns-1):
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
            elif event.key == pygame.K_RETURN:
                return True
    
    if pygame.mouse.get_pressed()[0]:
            try:
                pos = pygame.mouse.get_pos()
                mousePress(pos)
            except AttributeError:
                pass

def showVisited(visitedOrder):
    global isAnimating
    isAnimating = True
    skipAnimating = False
    for i in range(0, len(visitedOrder) + 5):
        
        if i <= len(visitedOrder)-1:
            if visitedOrder[i] is not start:
                visitedOrder[i].makeVisited(True)

        if i >= 5:
            if visitedOrder[i-5] is not start:
                visitedOrder[i-5].makeVisited()

        if skipAnimating == False:
            time.sleep(animateSpeed)

        if checkForClicks():
            skipAnimating = True

    isAnimating = False

def showPath():
    global isAnimating
    isAnimating = True
    step = 0
    path = []
    skipAnimation = False
    if end.visited == True:
        before = end.previous
        while before != start:
            path.append(before)
            step+=1
            before = before.previous

    i = len(path) - 1
    while i >= -1:

        if i > -1:
            path[i].makePath(True)
        if i < len(path) - 1:
            path[i+1].makePath()

        if skipAnimation == False:
            time.sleep(0.12)
        i-=1

        if checkForClicks():
            skipAnimation = True

    print('steps: ', step)
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

def prepareStartPlace():
    global start, placingStart
    placingStart = True
    if start != None:
        start.makeEmpty()
        start = None

def placeStartPos(x):
    # print(const.dirRow, const.dirCol, const.noOfColumns)
    row = int(x[1] // (const.h + margin))
    col = int(x[0] // (const.w + margin))
    
    if 1 <= row < const.noOfRows-1 and 1 <= col < const.noOfColumns-1:
        placeStart(row,col)

def placeEndPos(x):
    row = int(x[1] // (const.h + margin))
    col = int(x[0] // (const.w + margin))
    
    if 1 <= row < const.noOfRows-1 and 1 <= col < const.noOfColumns-1:
        placeEnd(row,col)

def placeStart(row, col):
    global start, placingStart

    start = grid[row][col]
    start.makeStart()
    placingStart = False

def prepareEndPlace():
    global end, placingEnd
    placingEnd = True
    if end != None:
        end.makeEmpty()
        end = None

def placeEnd(row, col):
    global end, placingEnd
    end = grid[row][col]
    end.makeEnd()
    placingEnd = False

def settingsPopup():
    changeDimensionsPopup()
    pygame.draw.rect(screen, white, (0, 0, gridWidth, gridHeight))
    setDimensions()
    transformIcons()
    setGrid()
    borderGrid()


# When clicking on cells
def mousePress(x):
    global placingStart, start, placingEnd, end, animateSpeed
    
    if startButton.isOver(x) and isAnimating == False:
        prepareStartPlace()
    
    if endButton.isOver(x) and isAnimating == False:
        prepareEndPlace()
    
    if dfsButton.isOver(x) and isAnimating == False:
        if start != None and end != None:
            visitedOrder = []
            prepareForSearch()
            dfs(grid, start, end, visitedOrder)
            showVisited(visitedOrder)
            showPath()


    if bfsButton.isOver(x) and isAnimating == False:
        if start != None and end != None:
            visitedOrder = []
            prepareForSearch()
            bfs(grid, start, end, visitedOrder)
            showVisited(visitedOrder)
            showPath()
    
    if astarButton.isOver(x) and isAnimating == False:
        if start != None and end != None:
            visitedOrder = []
            prepareForSearch()
            astar(grid, start, end, visitedOrder)
            showVisited(visitedOrder)
            showPath()

    if popupButton.isOver(x):
        settingsPopup()
    
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
    row = int(x[1] // (const.h + margin))
    col = int(x[0] // (const.w + margin))
    if 1 <= row < const.noOfRows-1 and 1 <= col < const.noOfColumns-1 and isAnimating == False:
        #print(row, col)
        if placingStart:
            placeStart(row,col)

        if placingEnd:
            placeEnd(row,col)

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
        elif pygame.mouse.get_pressed()[0]:
            try:
                pos = pygame.mouse.get_pos()
                mousePress(pos)
            except AttributeError:
                pass
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                pos = pygame.mouse.get_pos()
                prepareStartPlace()
                placeStartPos(pos)
            elif event.key == pygame.K_e:
                pos = pygame.mouse.get_pos()
                prepareEndPlace()
                placeEndPos(pos)
            elif event.key == pygame.K_c and isAnimating == False:
                clearBoard()

pygame.quit()