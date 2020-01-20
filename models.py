import pygame

from const import *
import const

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
        pygame.draw.rect(self.screen, color, (self.j * (const.w + margin) + margin, self.i * (const.h + margin) + margin, const.w, const.h))
        pygame.display.update()

    def makeEmpty(self):
        self.isObstacle = False
        pygame.draw.rect(self.screen, white, (self.j * (const.w + margin) + margin, self.i * (const.h + margin) + margin, const.w, const.h))
        pygame.display.update()
    
    def makeObstacle(self):
        self.isObstacle = True
        self.screen.blit(const.fireIcon, (self.j * (const.w + margin) + margin, self.i * (const.h + margin) + margin))
        pygame.display.update()

    def makeStart(self):
        self.screen.blit(const.startIcon, (self.j * (const.w + margin) + margin, self.i * (const.h + margin) + margin))
        pygame.display.update()
    
    def makeEnd(self):
        self.screen.blit(const.endIcon, (self.j * (const.w + margin) + margin, self.i * (const.h + margin) + margin))
        pygame.display.update()
    
    def makeVisited(self, first=False):
        if first == True:
            pygame.draw.rect(self.screen, (0, 102, 102), (self.j * (const.w + margin) + margin, self.i * (const.h + margin) + margin, const.w, const.h))
        else:
            pygame.draw.rect(self.screen, turqoise, (self.j * (const.w + margin) + margin, self.i * (const.h + margin) + margin, const.w, const.h))
        pygame.display.update()

    def makePath(self, first=False):
        if first == True:
            self.screen.blit(const.pathIcon, (self.j * (const.w + margin) + margin, self.i * (const.h + margin) + margin))
        else: 
            pygame.draw.rect(self.screen, red, (self.j * (const.w + margin) + margin, self.i * (const.h + margin) + margin, const.w, const.h))
        
        
        pygame.display.update()

    # Set cell as path
    def path(self, color):
        pygame.draw.rect(self.screen, color, (self.i * (const.w + margin) + margin, self.j * (const.h + margin) + margin, const.w, const.h))
        pygame.display.update()

    # Add neighbors list to cell object
    def addNeighbors(self, grid):
        i = self.i
        j = self.j

        for dir in range(const.noOfDirections):
            newI = i + const.dirRow[dir]
            newJ = j + const.dirCol[dir]

            if 0 < newI < const.noOfRows-1 and 0 < newJ < const.noOfColumns-1 and grid[newI][newJ].isObstacle == False:
                self.neighbors.append(grid[newI][newJ])

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
