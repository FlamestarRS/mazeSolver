from graphics import *
from constants import test_points

def main():
    win = Window(800, 600)
    test_line = Line(Point(400, 400), Point(300, 300))

    test_color = "red"

    cells = []
    for item in test_points:
        cell = Cell(win)
        cell.draw(item[0], item[1], "red")
        cells.append(cell)

    win.wait_for_close()

if __name__ == "__main__":
    main()