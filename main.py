from graphics import *
from constants import test_points, fill_test_grid

def main():
    win = Window(800, 600)
    test_line = Line(Point(400, 400), Point(300, 300))

    test_color = "red"
    grid = fill_test_grid()
    cells = []
    for item in grid:
        cell = Cell(win)
        cell.draw(item[0], item[1], "black")
        cells.append(cell)

    for i in range(len(cells)):
        if i == len(cells)-1:
            break
        cells[i].draw_move(cells[i+1], undo=True)

    win.wait_for_close()

if __name__ == "__main__":
    main()