import pygame
import sys
import math
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os
import time

from constants import *
from algorithms import bfs
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

slowButton = button(grey, displayWidth * 5 / 8 - 100, 505, 100, 30, screen, text='Slow')
slowButton.draw()

normalButton = button(grey, displayWidth * 6 / 8 - 100, 505, 100, 30, screen, text='Normal')
normalButton.draw(True)

fastButton = button(grey, displayWidth * 7 / 8 - 100, 505, 100, 30, screen, text='Fast')
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

# Popup comment
if(True):
    # When closing popup
    # def onsubmit():
    #     global start
    #     global end
    #     st = startBox.get().split(',')
    #     ed = endBox.get().split(',')
    #     start = grid[int(st[0])][int(st[1])]
    #     end = grid[int(ed[0])][int(ed[1])]
    #     window.quit()
    #     window.destroy()
    # Defining popup
    #window = Tk()
    #label = Label(window, text='Start(x,y): ')
    #startBox = Entry(window)
    #label1 = Label(window, text='End(x,y): ')
    #endBox = Entry(window)
    #var = IntVar()
    #showPath = ttk.Checkbutton(window, text='Show Steps :', onvalue=1, offvalue=0, variable=var)

    #submit = Button(window, text='Submit', command=onsubmit)

    #showPath.grid(columnspan=2, row=2)
    #submit.grid(columnspan=2, row=3)
    #label1.grid(row=1, pady=3)
    #endBox.grid(row=1, column=1, pady=3)
    #startBox.grid(row=0, column=1, pady=3)
    #label.grid(row=0, pady=3)

    #window.update()
    #mainloop()
    print()

pygame.init()
# openSet.append(start)

start = None
end = None

running = True

previousClicked = None

animateSpeed = 0.01

placingStart = False
placingEnd = False

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


def checkIfClosed():
    ev = pygame.event.get()

    for event in ev:
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            exit()



def showVisited(visitedOrder):
    print(animateSpeed)
    for i in range(0, len(visitedOrder) + 4):
        
        if i <= len(visitedOrder)-1:
            visitedOrder[i].makePath()

        if i >= 5:
            visitedOrder[i-5].makeVisited()

        time.sleep(animateSpeed)
        if checkIfClosed():
            return

def showPath():
    if end.visited == True:
        before = end.previous
        while before != start:
            before.makePath()
            before = before.previous
            time.sleep(0.02)
            if checkIfClosed():
                return

def changeSpeed(x):
    global animateSpeed

    fastButton.draw(False)
    normalButton.draw(False)
    slowButton.draw(False)

    if x == 0:
        animateSpeed = 0.05
        slowButton.draw(True)
    if x == 1:
        animateSpeed = 0.002
        normalButton.draw(True)
    if x == 2:
        animateSpeed = 0
        fastButton.draw(True)
    
    print(animateSpeed)

# When clicking on cells
def mousePress(x):
    global placingStart, start, placingEnd, end, animateSpeed
    
    if startButton.isOver(x):
        placingStart = True
        if start != None:
            start.makeEmpty()
            start = None
    
    if endButton.isOver(x):
        placingEnd = True
        if end != None:
            end.makeEmpty()
            end = None
    
    if bfsButton.isOver(x):
        if start != None and end != None:
            visitedOrder = []
            prepareForSearch()
            bfs(grid, noOfColumns, noOfRows, start, end, visitedOrder)
            showVisited(visitedOrder)
            showPath()
    
    if slowButton.isOver(x):
        changeSpeed(0)
    
    if normalButton.isOver(x):
        changeSpeed(1)

    if fastButton.isOver(x):
        changeSpeed(2)
    
    if clearButton.isOver(x):
        clearBoard()
    
    # if you clicked a cell
    global previousClicked
    row = int(x[1] // (h+margin))
    col = int(x[0] // (w+margin))
    if 1 <= row < noOfRows-1 and 1 <= col < noOfColumns-1:
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
            if event.key == pygame.K_SPACE:
                loop = False
                break

pygame.quit()