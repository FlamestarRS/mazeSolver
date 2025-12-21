from __future__ import annotations
from tkinter import Tk, BOTH, Canvas
from time import sleep
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, INTERVAL
import random

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
    
    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False

    def draw_line(self, line: Line, color="black"):
        line.draw(self.__canvas, color)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas: Canvas, color):
        canvas.create_line(
            self.p1.x, self.p1.y, 
            self.p2.x, self.p2.y, 
            fill=color, width=2
            )
        
class Cell:
    def __init__(self, p1: Point, p2: Point, win: Window | None = None):
        self.N_wall = True
        self.S_wall = True
        self.E_wall = True
        self.W_wall = True
        self.visited = False
        self.__x1 = p1.x
        self.__x2 = p2.x
        self.__y1 = p1.y
        self.__y2 = p2.y
        self.__win = win

    def draw(self, color="black"):
        
        self.auto_correct()

        n = Line(Point(self.__x1, self.__y1), Point(self.__x2, self.__y1))
        s = Line(Point(self.__x1, self.__y2), Point(self.__x2, self.__y2))
        e = Line(Point(self.__x2, self.__y1), Point(self.__x2, self.__y2))
        w = Line(Point(self.__x1, self.__y1), Point(self.__x1, self.__y2))
        if self.__win == None:
            return
        if self.N_wall:
            self.__win.draw_line(n, color)
        else:
            self.__win.draw_line(n, "#d9d9d9")
        if self.S_wall:
            self.__win.draw_line(s, color)
        else:
            self.__win.draw_line(s, "#d9d9d9")
        if self.E_wall:
            self.__win.draw_line(e, color)
        else:
            self.__win.draw_line(e, "#d9d9d9")
        if self.W_wall:
            self.__win.draw_line(w, color)
        else:
            self.__win.draw_line(w, "#d9d9d9")

    def auto_correct(self): # ensures cell walls are constructed based on NW and SE points
        if self.__x1 > self.__x2:  
             self.__x1, self.__x2 = self.__x2, self.__x1
        if self.__y1 > self.__y2:
             self.__y1, self.__y2 = self.__y2, self.__y1

    def draw_move(self, to_cell: Cell, undo=False):
        if self.__win == None:
            return
        center = Point(((self.__x1 + self.__x2) / 2), ((self.__y1 + self.__y2) / 2))
        dest_center = Point(((to_cell.__x1 + to_cell.__x2) / 2), ((to_cell.__y1 + to_cell.__y2) / 2))
        color = "gray" if undo else "red"
        self.__win.draw_line(Line(center, dest_center), color)


class Maze:
    def __init__(
        self,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None,
    ):
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        self.__cells = []
        self.__create_cells()
        if seed != None:
            random.seed(seed)

        self.__break_enterance_and_exit()
        self.__break_walls_r(0, 0)
        self.__reset_cells_visited()

    def __create_cells(self):
        starting_x_pos = (SCREEN_WIDTH - self.__num_cols * self.__cell_size_x) / 2
        starting_y_pos = (SCREEN_HEIGHT - self.__num_rows * self.__cell_size_y) / 2
        for i in range(self.__num_rows):
            row = []
            for j in range(self.__num_cols):
                nw_point = Point(starting_x_pos + (j*self.__cell_size_x), starting_y_pos + (i*self.__cell_size_y))
                se_point = Point(starting_x_pos + ((j+1)*self.__cell_size_x), starting_y_pos + ((i+1)*self.__cell_size_y))
                cell = Cell(nw_point, se_point, self.__win)
                row.append(cell)
                if self.__win != None:
                    cell.draw()
                    self.__animate()
                
            self.__cells.append(row)
    
    def __animate(self):
        self.__win.redraw()
        sleep(INTERVAL)
            
    def __break_enterance_and_exit(self):
        self.__cells[0][0].N_wall = False
        self.__cells[-1][-1].S_wall = False
        self.__cells[0][0].draw()
        self.__cells[-1][-1].draw()

    def __break_walls_r(self, i, j):
        self.__cells[i][j].visited = True
        
        while True:
            neighbors = {}

            if i + 1 < len(self.__cells):
                neighbors['S'] = self.__cells[i+1][j]

            if i - 1 >= 0:
                neighbors['N'] = self.__cells[i-1][j]

            if j + 1 < len(self.__cells[i]):
                neighbors['E'] = self.__cells[i][j+1]

            if j - 1 >= 0:
                neighbors['W'] = self.__cells[i][j-1]

            to_visit = {}
            for direction, cell in neighbors.items():
                if cell.visited:
                    continue
                to_visit[direction] = cell

            if len(to_visit) == 0:
                self.__cells[i][j].draw()
                return
            
            direction = random.choice(list(to_visit))
            match direction:
                case 'N':
                    self.__cells[i][j].N_wall = False
                    self.__cells[i-1][j].S_wall = False
                    self.__cells[i][j].draw()
                    self.__cells[i-1][j].draw()
                    self.__break_walls_r(i-1, j)
                case 'S':
                    self.__cells[i][j].S_wall = False
                    self.__cells[i+1][j].N_wall = False
                    self.__cells[i][j].draw()
                    self.__cells[i+1][j].draw()
                    self.__break_walls_r(i+1, j)
                case 'E':
                    self.__cells[i][j].E_wall = False
                    self.__cells[i][j+1].W_wall = False
                    self.__cells[i][j].draw()
                    self.__cells[i][j+1].draw()
                    self.__break_walls_r(i, j+1)
                case 'W':
                    self.__cells[i][j].W_wall = False
                    self.__cells[i][j-1].E_wall = False
                    self.__cells[i][j].draw()
                    self.__cells[i][j-1].draw()
                    self.__break_walls_r(i, j-1)
              
    def __reset_cells_visited(self):
        for row in self.__cells:
            for cell in row:
                cell.visited = False

    def __solve_r(self, i=0, j=0):
        self.__animate()
        self.__cells[i][j].visited = True

        if self.__cells[i][j] == self.__cells[-1][-1]:
            return True

        neighbors = []

        if i + 1 < len(self.__cells): # does south cell exist and new/accessible
            if not self.__cells[i+1][j].visited and not self.__cells[i][j].S_wall:
                neighbors.append((i+1, j))

        if i - 1 >= 0: # does north cell exist and new/accessible
            if not self.__cells[i-1][j].visited and not self.__cells[i][j].N_wall:
                neighbors.append((i-1, j))

        if j + 1 < len(self.__cells[i]): # does east cell exist and new/accessible
            if not self.__cells[i][j+1].visited and not self.__cells[i][j].E_wall:
                neighbors.append((i, j+1))

        if j - 1 >= 0: # does west cell exist and new/accessible
            if not self.__cells[i][j-1].visited and not self.__cells[i][j].W_wall:
                neighbors.append((i, j-1))

        for row, col in neighbors:
            self.__cells[i][j].draw_move(self.__cells[row][col])
            if self.__solve_r(row, col):
                return True
            else:
                self.__cells[i][j].draw_move(self.__cells[row][col], True)

        return False

    def solve(self):
        return self.__solve_r()
