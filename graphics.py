from __future__ import annotations
from tkinter import Tk, BOTH, Canvas


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
    def __init__(self, win: Window):
        self.N_wall = True
        self.S_wall = True
        self.E_wall = True
        self.W_wall = True
        self.__x1 = -1
        self.__x2 = -1
        self.__y1 = -1
        self.__y2 = -1
        self.__win = win

    def draw(self, p1: Point, p2: Point, color="black"):
        self.__x1 = p1.x
        self.__x2 = p2.x
        self.__y1 = p1.y
        self.__y2 = p2.y

        self.auto_correct()

        n = Line(Point(self.__x1, self.__y1), Point(self.__x2, self.__y1))
        s = Line(Point(self.__x1, self.__y2), Point(self.__x2, self.__y2))
        e = Line(Point(self.__x2, self.__y1), Point(self.__x2, self.__y2))
        w = Line(Point(self.__x1, self.__y1), Point(self.__x1, self.__y2))
        if self.N_wall:
            self.__win.draw_line(n, color)
        if self.S_wall:
            self.__win.draw_line(s, color)
        if self.E_wall:
            self.__win.draw_line(e, color)
        if self.W_wall:
            self.__win.draw_line(w, color)

    def auto_correct(self): # ensures cell walls are constructed based on NW and SE points
        if self.__x1 > self.__x2:  
             self.__x1, self.__x2 = self.__x2, self.__x1
        if self.__y1 > self.__y2:
             self.__y1, self.__y2 = self.__y2, self.__y1