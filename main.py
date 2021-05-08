import pygame
import sys
import datetime

WHITE = (255,255,255)
BLACK = (0, 0, 0)

widthOfBox = 10 #12 
width, height = 600, 600
boxesWidth = width//widthOfBox
boxesHeight = height//widthOfBox

grid = ([[[] for i in range(boxesWidth)]for i in range(boxesWidth)])

lineColor = (100, 100, 100)
gapWidth = 1

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
now = datetime.datetime.now()
            
def find_neighbours(row, col):
    neighbours = 0
    for i in range(-1, 2):
        try:
            if grid[row+i][col-1] == 1:
                neighbours += 1
        except:
            pass
    try:
        if grid[row-1][col] == 1:
            neighbours += 1
    except:
        pass
    try:
        if grid[row+1][col] == 1:
            neighbours += 1
    except:
        pass
    for i in range(-1, 2):
        try:
            if grid[row+i][col+1] == 1:
                neighbours += 1
        except:
            pass
    return neighbours

    return neighbours

def drawLines():
    for col in range(boxesHeight):
        for row in range(boxesWidth):
            pygame.draw.line(screen, lineColor, (0, row*widthOfBox), (height, row*widthOfBox), gapWidth)
            pygame.draw.line(screen, lineColor, (col*widthOfBox, 0), (col*widthOfBox, width), gapWidth)
        
def draw_grid():
    for col in range(boxesWidth):
        for row in range(boxesHeight):
            node = grid[row][col]
            if node == 1:
                colour = BLACK
            else:
                colour = WHITE
            x = row*widthOfBox
            y = col*widthOfBox
            rect = pygame.Rect(x, y, widthOfBox, widthOfBox) #left, top, width, height 
            pygame.draw.rect(screen, colour, rect)
    drawLines()

def calculate_next_grid():
    next_grid = ([[[] for i in range(boxesWidth)]for i in range(boxesWidth)])
    for col in range(width//widthOfBox):
        for row in range(width//widthOfBox):
            numberOfNeighbours = find_neighbours(col, row)
            if grid[col][row] == 1 and find_neighbours(col, row) == 2 or find_neighbours(col, row) == 3: # alive and has 2 neighbours it stays alive
                next_grid[col][row] = 1 # stays alive
            if grid[col][row] == 0 and find_neighbours(col, row) == 3:
                next_grid[col][row] = 1
    return next_grid

def getRowAndColNumber(x, y): # given an x and y coorsinate returns the row and column where that location falls
    for col in range(boxesHeight):
        for row in range(boxesWidth):
            if x > col*widthOfBox and x < (col+1)*widthOfBox:
                if y > row*widthOfBox and y < (row+1)*widthOfBox:
                    return (row, col)
    return (None, None) # else

font = pygame. font. SysFont("Arial", 18)
def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 1, pygame.Color("coral"))
    screen.blit(fps_text, (25, 25))

pause = True
tickSpeed = 10

clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            sys.exit()

        mouseX, mouseY = pygame.mouse.get_pos() 
        col_num, row_num = getRowAndColNumber(mouseX, mouseY)
        
        if pygame.mouse.get_pressed()[0]: # left click
            if row_num != None and col_num != None:
                grid[row_num][col_num] = 1

        if pygame.mouse.get_pressed()[2]:
            if row_num != None and col_num != None:
                grid[row_num][col_num] = 0

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if pause:
                    pause = False
                else:
                    pause = True

            if event.key == pygame.K_ESCAPE:
                grid = [[[] for i in range(boxesWidth)]for i in range(boxesWidth)]

    if pause == False:
        previousGrid = grid
        grid = calculate_next_grid()
        if previousGrid == grid:
            pause = True


    screen.fill((210,210,210))
    draw_grid()
    update_fps()

    clock.tick(15) # max fps

    pygame.display.update()
