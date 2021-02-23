import pygame
import sys
import time

WHITE = (255,255,255)
BLACK = (0, 0, 0)

widthOfBox = 12 #12 
width, height = 600, 600

lineColor = (100, 100, 100)
gapWidth = 1

screen = pygame.display.set_mode((width, height))

class Node(object):
    def __init__(self, x, y, row, col, color):
        self.x = x #far left x
        self.y = y #top y
        self.row = row
        self.col = col
        self.color = color

    def drawSelf(self):
        self.rect = pygame.Rect(self.x, self.y, widthOfBox, widthOfBox) #left, top, width, height 
        pygame.draw.rect(screen, self.color, self.rect)

grid = [[(Node(x*widthOfBox, y*widthOfBox, x, y, WHITE)) for x in range(width//widthOfBox)] for y in range(height//widthOfBox)]
            
def find_neighbours(row, col):
    neighbours = 0
    for i in range(-1, 2):
        try:
            if grid[row+i][col-1].color == BLACK:
                neighbours += 1
        except:
            pass
    try:
        if grid[row-1][col].color == BLACK:
            neighbours += 1
    except:
        pass
    try:
        if grid[row+1][col].color == BLACK:
            neighbours += 1
    except:
        pass
    for i in range(-1, 2):
        try:
            if grid[row+i][col+1].color == BLACK:
                neighbours += 1
        except:
            pass
    return neighbours
        
def draw_grid():
    for row in grid:
        for item in row:
            item.drawSelf()

    for row in grid:
        for item in range(len(row)):
            ## VERTICAL LINES
            verticalStart = 0, item*widthOfBox # furthest left and item*widthOfBox down
            verticalEnd = width, item*widthOfBox
            pygame.draw.line(screen, lineColor, verticalStart, verticalEnd, gapWidth) #surface, color, start, end, width

            ## HORIZONTAL LINES
            horizontalStart = item*widthOfBox, 0
            horizontalEnd = item*widthOfBox, width
            pygame.draw.line(screen, lineColor, horizontalStart, horizontalEnd, gapWidth) #surface, color, start, end, width

    pygame.display.update()

def calculate_next_grid():
    next_grid = [[(Node(x*widthOfBox, y*widthOfBox, x, y, WHITE)) for x in range(width//widthOfBox)] for y in range(height//widthOfBox)]
    for col in range(width//widthOfBox):
        for row in range(width//widthOfBox):
            numberOfNeighbours = find_neighbours(col, row)

            if grid[col][row].color == BLACK and find_neighbours(col, row) == 2: # alive and has 2 neighbours it stays alive
                next_grid[col][row].color = BLACK # stays alive
            if grid[col][row].color == BLACK and find_neighbours(col, row) == 3:
                next_grid[col][row].color = BLACK #stays alive
            if grid[col][row].color == WHITE and find_neighbours(col, row) == 3:
                next_grid[col][row].color = BLACK
    return next_grid

def getRowAndColNumber(x, y):
    for row in grid:
        for node in row:
            if x > node.x and x < node.x+widthOfBox:
                if y > node.y and y < node.y+widthOfBox:
                    return (node.col, node.row)
    return (None, None)

pause = True
tickSpeed = 10

clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            sys.exit()

        mouseX, mouseY = pygame.mouse.get_pos() 
        row_num, col_num = getRowAndColNumber(mouseX, mouseY)
        
        if pygame.mouse.get_pressed()[0]: # left click
            if row_num != None and col_num != None:
                grid[row_num][col_num].color = BLACK

        if pygame.mouse.get_pressed()[2]:
            if row_num != None and col_num != None:
                grid[row_num][col_num].color = WHITE

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if pause:
                    pause = False
                else:
                    pause = True

            if event.key == pygame.K_ESCAPE:
                grid = [[(Node(x*widthOfBox, y*widthOfBox, x, y, WHITE)) for x in range(width//widthOfBox)] for y in range(height//widthOfBox)]
                
            if event.key == pygame.K_RIGHT:
                if tickSpeed <= 250:
                    tickSpeed += 5
            if event.key == pygame.K_LEFT:
                if tickSpeed >= 6:
                    tickSpeed -= 5
        
    if pause == False:
        grid = calculate_next_grid()

    screen.fill((210,210,210))
    draw_grid()
    clock.tick(tickSpeed)
