import pygame

from constants import *

#  GRID CELL
class cell:
    def __init__(self, x, y, screen):
        self.i = x
        self.j = y
        self.neighbors = []
        self.previous = None
        self.isObstacle = False
        self.visited = False
        self.closed = False
        self.value = 1
        self.screen = screen
    
    # Display cell
    def make(self, color):
        pygame.draw.rect(self.screen, color, (self.j * (w + margin) + margin, self.i * (h + margin) + margin, w, h))
        pygame.display.update()

    def makeEmpty(self):
        self.isObstacle = False
        pygame.draw.rect(self.screen, white, (self.j * (w + margin) + margin, self.i * (h + margin) + margin, w, h))
        pygame.display.update()
    
    def makeObstacle(self):
        self.isObstacle = True
        self.screen.blit(fireIcon, (self.j * (w + margin) + margin, self.i * (h + margin) + margin))
        pygame.display.update()

    def makeStart(self):
        self.screen.blit(startIcon, (self.j * (w + margin) + margin, self.i * (h + margin) + margin))
        pygame.display.update()
    
    def makeEnd(self):
        self.screen.blit(endIcon, (self.j * (w + margin) + margin, self.i * (h + margin) + margin))
        pygame.display.update()
    
    def makeVisited(self):
        pygame.draw.rect(self.screen, turqoise, (self.j * (w + margin) + margin, self.i * (h + margin) + margin, w, h))
        pygame.display.update()

    def makePath(self):
        pygame.draw.rect(self.screen, purple, (self.j * (w + margin) + margin, self.i * (h + margin) + margin, w, h))
        pygame.display.update()

    # Set cell as path
    def path(self, color):
        pygame.draw.rect(self.screen, color, (self.i * (w + margin) + margin, self.j * (h + margin) + margin, w, h))
        pygame.display.update()

    # Add neighbors list to cell object
    def addNeighbors(self, grid):
        i = self.i
        j = self.j
        if i > 0 and grid[self.i - 1][j].isObstacle == False:
            self.neighbors.append(grid[self.i - 1][j])
        if j < noOfColumns-1 and grid[self.i][j + 1].isObstacle == False:
            self.neighbors.append(grid[self.i][j + 1])
        if i < noOfRows-1 and grid[self.i + 1][j].isObstacle == False:
            self.neighbors.append(grid[self.i + 1][j])
        if j > 0 and grid[self.i][j - 1].isObstacle == False:
            self.neighbors.append(grid[self.i][j - 1])

# BUTTON
class button():
    def __init__(self, color, x,y, width, height, screen, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.screen = screen

    def empty(self):
        pygame.draw.rect(self.screen, grey, (self.x,self.y,self.width,self.height),0)
        

    def draw(self,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(self.screen, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
        else:
            pygame.draw.rect(self.screen, grey, (self.x-2,self.y-2,self.width+4,self.height+4),0)     
        pygame.draw.rect(self.screen, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('arial', 15)
            text = font.render(self.text, 1, (0,0,0))
            self.screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

        pygame.display.update()

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False
