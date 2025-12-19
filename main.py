from graphics import *

def main():
    win = Window(SCREEN_WIDTH, SCREEN_HEIGHT)
    rows = 20
    cols = 30
    row_width = 10
    col_width = 10
    maze = Maze(rows, cols, row_width, col_width, win)
    maze._Maze__break_enterance_and_exit()
    win.wait_for_close()


if __name__ == "__main__":
    main()