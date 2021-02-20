import pygame
import sys
import time

white = (255,255,255)
black = (0, 0, 0)
margin = 1

widthOfBox = 12 #12 
width, height = 600, 600

grid = [[0 for x in range(round(width/widthOfBox))] for y in range(round(height/widthOfBox))]

screen = pygame.display.set_mode((width, height))

def get_row_values():
    row_values = []
    number = 0
    for rows in range(round(width/widthOfBox)):
        if number == 0:
            number -= widthOfBox
        number += widthOfBox
        number+=margin
        values = [number, number+widthOfBox]
        row_values.append(values)
    return row_values
row_values = get_row_values()

def get_column_values():
    col_values = []
    number = 0
    for cols in range(round(height/widthOfBox)):
        if number == 0:
            number -= widthOfBox
        number += widthOfBox
        number+=margin
        values = [number, number+widthOfBox]
        col_values.append(values)
    return col_values
col_values = get_column_values()

def get_rowORcol_number(XYcoordinates, rowcol_values):
    for i in range(len(rowcol_values)):
        if XYcoordinates >= rowcol_values[i][0] and XYcoordinates <= rowcol_values[i][1]:
            return i
            
def find_neighbours(row, col):
    neighbours = 0
    relative_col = 0
    relative_row = -2
    if grid[row][col] == 1:
        neighbours -= 1
    for i in range(3):
        relative_row+=1
        relative_col = -2
        for i in range(3):
            relative_col+=1
            try:
                if grid[row+relative_row][col+relative_col] == 1:
                    neighbours += 1
            except:
                pass
    return neighbours
            
def draw_grid():
    length_from_top = 0
    first = True
    for col in range(round(height/widthOfBox)):
        if first:
            length_from_top -= widthOfBox
            first = False
        length_from_top += widthOfBox+margin
        for row in range(round(width/widthOfBox)): # this draws horisontal rows 
            if grid[row][col] == 1:
                color = black
            else:
                color = white

            rect = pygame.Rect((row*widthOfBox)+row, length_from_top, widthOfBox, widthOfBox) #left, top, width, height 
            pygame.draw.rect(screen, color, rect)
    pygame.display.update()

def calculate_next_grid():
    next_grid = [[0 for x in range(round(width/widthOfBox))] for y in range(round(height/widthOfBox))]
    for col in range(round(width/widthOfBox)):
        for row in range(round(width/widthOfBox)):
            if grid[col][row] == 1 and find_neighbours(col, row) == 2: # alive and has 2 neighbours it stays alive
                next_grid[col][row] = 1 # stays alive
            if grid[col][row] == 1 and find_neighbours(col, row) == 3:
                next_grid[col][row] = 1 #stays alive
            if grid[col][row] == 0 and find_neighbours(col, row) == 3:
                next_grid[col][row] = 1
    return next_grid

draw = True
wait_time = 0.26

clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
        if pygame.mouse.get_pressed()[0]: # left click
            mouseX, mouseY = pygame.mouse.get_pos() 
            row_num = get_rowORcol_number(mouseX, col_values)
            col_num = get_rowORcol_number(mouseY, row_values)
            grid[row_num][col_num]= 1

        if pygame.mouse.get_pressed()[2]:
            mouseX, mouseY = pygame.mouse.get_pos() 
            row_num = get_rowORcol_number(mouseX, col_values)
            col_num = get_rowORcol_number(mouseY, row_values)
            grid[row_num][col_num]= 0

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if draw == True:
                    draw = False
                else:
                    draw = True
            if event.key == pygame.K_ESCAPE:
                grid = [[0 for x in range(round(width/widthOfBox))] for y in range(round(height/widthOfBox))]
            if event.key == pygame.K_RIGHT:
                if wait_time >= 0.05:
                    wait_time -= 0.05
            if event.key == pygame.K_LEFT:
                if wait_time != 1:
                    wait_time += 0.05
            #print(row_num, col_num)

            if event.key == pygame.K_l:
                for row in grid:
                    print(str(row)+',')

    if grid == [[0 for x in range(round(width/widthOfBox))] for y in range(round(height/widthOfBox))]: # if grid is filled with blank squares
        draw = True

    if draw == False:
        calculate_next_grid()
        grid = calculate_next_grid()
        time.sleep(wait_time)
    screen.fill((210,210,210))
    draw_grid()
    clock.tick(60)
