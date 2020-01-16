import pygame

#Colors
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
grey = (220, 220, 220)
white = (255, 255, 255)
black = (0, 0, 0)
turqoise = (133, 228, 215)
purple = (156, 68, 208)
brown = (139, 37, 0)
yellow =  (213, 213, 32)

# GLOBAL VARIABLES
displayWidth = 1000
displayHeight = 550
gridWidth = 1000
gridHeight = 500

# Grid dimensions
noOfColumns = 60
noOfRows = 30


# Cell dimensions
margin = 2
w = (gridWidth-margin*(noOfColumns+1)) / noOfColumns
h = (gridHeight-margin*(noOfRows+1)) / noOfRows


# Icons
fireIcon = pygame.image.load('fire.jpg')
fireIcon = pygame.transform.scale(fireIcon, (int(w),int(h)))

startIcon = pygame.image.load('start.png')
startIcon = pygame.transform.scale(startIcon, (int(w),int(h)))

endIcon = pygame.image.load('end.png')
endIcon = pygame.transform.scale(endIcon, (int(w),int(h)))