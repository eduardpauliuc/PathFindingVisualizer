import pygame

#Colors
red = (162, 42, 40)
green = (0, 153, 51)
blue = (0, 0, 255)
grey = (220, 220, 220)
white = (255, 255, 255)
black = (0, 0, 0)
turqoise = (133, 228, 215)
purple = (156, 68, 208)
brown = (204, 102, 0)
yellow =  (213, 213, 32)

# GLOBAL VARIABLES
displayWidth = 1000
displayHeight = 550
gridWidth = 1000
gridHeight = 500

# Grid dimensions - VARIABLE
noOfColumns = 30
noOfRows = 15


# Cell dimensions - VARIABLE
margin = 2

w = h = 0
def setDimensions():
    global w, h
    w = (gridWidth-margin*(noOfColumns+1)) / noOfColumns
    h = (gridHeight-margin*(noOfRows+1)) / noOfRows

setDimensions()

def changeDimensions(rows, cols):
    global noOfColumns, noOfRows
    noOfColumns = cols
    noOfRows = noOfRows

# Icons
fireIcon = None
startIcon = None
endIcon = None
pathIcon = None

settingsIcon = pygame.image.load('settings.jpg')
settingsIcon = pygame.transform.scale(settingsIcon, (int(w),int(h)))
windowIcon = pygame.image.load('xi.png')
windowIcon = pygame.transform.scale(windowIcon, (32,32))

def transformIcons():
    global fireIcon, startIcon, endIcon, pathIcon
    fireIcon = pygame.image.load('fire.jpg')
    fireIcon = pygame.transform.scale(fireIcon, (int(w),int(h)))
    startIcon = pygame.image.load('start.png')
    startIcon = pygame.transform.scale(startIcon, (int(w),int(h)))
    endIcon = pygame.image.load('end.png')
    endIcon = pygame.transform.scale(endIcon, (int(w),int(h)))
    pathIcon = pygame.image.load('path.png')
    pathIcon = pygame.transform.scale(pathIcon, (int(w),int(h)))


#directions

noOfDirections = -1
dirRow = []
dirCol = []

def setDirections(x):
    global dirRow, dirCol, noOfDirections

    if noOfDirections != -1 and abs(noOfDirections - x) != 4:
        return
    
    noOfDirections = x

    if x == 4:
        dirRow = [-1, 0, 1, 0]
        dirCol = [0, 1, 0, -1]
    else:
        dirRow = [-1, 0, 1, 0, -1, 1, 1, -1]
        dirCol = [0, 1, 0, -1, 1, 1, -1, -1]
    
setDirections(8)


