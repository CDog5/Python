import pygame,math
from queue import PriorityQueue
from tkinter import *
from tkinter import messagebox 
#Callum Sheppard 2020
WIDTH = 650
WINDOW = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("A* Pathfinder")
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
Tk().wm_withdraw() #to hide the main window

class Square:
    def __init__(self,row,col,width,total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.colour = WHITE
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows
    def get_pos(self):
        return self.row,self.col
    def draw(self,window):
        pygame.draw.rect(window,self.colour,(self.x,self.y,self.width,self.width))
    def update_neighbours(self,grid):
        self.neighbours = []
        if self.row < self.total_rows - 1 and not grid [self.row + 1][self.col].colour == BLACK:
            self.neighbours.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid [self.row - 1][self.col].colour == BLACK:
            self.neighbours.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid [self.row][self.col + 1].colour == BLACK:
            self.neighbours.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid [self.row][self.col - 1].colour == BLACK:
            self.neighbours.append(grid[self.row][self.col - 1])
    def __lt__(self,other):
        return False
def heuristic(point1,point2):
    x1,y1 = point1
    x2,y2 = point2
    return abs(x1-x2)+abs(y1-y2)
def make_grid(rows,width):
    grid=[]
    gap=width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            square = Square(i,j,gap,rows)
            grid[i].append(square)
    return grid
def draw_grid(window,rows,width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(window,GREY,(0,i*gap),(width,i*gap))
        for j in range(rows):
            pygame.draw.line(window,GREY,(j*gap,0),(j*gap,width))
def draw(window,grid,rows,width):
    window.fill(WHITE)
    for row in grid:
        for square in row:
            square.draw(window)
    draw_grid(window,rows,width)
    pygame.display.update()
def get_clicked_pos(pos,rows,width):
    gap = width // rows
    y,x=pos
    row = y // gap
    col = x // gap
    return row,col
def reconstruct_path(came_from,current,draw):
    count = 0
    while current in came_from:
        current = came_from[current]
        current.colour = TURQUOISE
        draw()
        count +=1
    return count

def algorithm(draw,grid,start,end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0,count,start))
    came_from = {}
    g_score = {square: float("inf")for row in grid for square in row}
    g_score[start] = 0
    f_score = {square: float("inf")for row in grid for square in row}
    f_score[start] = heuristic(start.get_pos(),end.get_pos())
    open_set_hash = {start}
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]
        open_set_hash.remove(current)
        if current == end:
            count = reconstruct_path(came_from,end,draw)
            start.colour = PURPLE
            end.colour = ORANGE
            draw()
            messagebox.showinfo('A* Pathfinder','Found the shortest path! It is '+str(count)+' squares long.')
            return True
        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + heuristic(neighbour.get_pos(),end.get_pos())
                if neighbour not in open_set_hash:
                    count +=1
                    open_set.put((f_score[neighbour],count,neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.colour = GREEN
        draw()
        if current != start:
            current.colour = RED
    return False
  
def main(window,width):
    ROWS = 50
    grid = make_grid(ROWS,width)
    start = None
    end = None  
    run = True
    while run:
        draw(window,grid,ROWS,width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]: #Left mouse button
                pos = pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos,ROWS,width)
                square = grid[row][col]
                if not start and square != end:
                    start = square
                    start.colour = PURPLE
                elif not end and square != start:
                    end = square
                    end.colour = ORANGE
                elif square != start and square != end:
                    square.colour = BLACK
            elif pygame.mouse.get_pressed()[2]: #Right mouse button
                pos = pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos,ROWS,width)
                square = grid[row][col]
                square.colour = WHITE
                if square == start:
                    start = None
                elif square == end:
                    end = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for square in row:
                            square.update_neighbours(grid)
                    algorithm(lambda: draw(window,grid,ROWS,width),grid,start,end)
                if event.key == pygame.K_c or event.key == pygame.K_r:
                    start = None
                    end = None
                    grid = make_grid(ROWS,width)
                    
    pygame.quit()
main(WINDOW,WIDTH)
