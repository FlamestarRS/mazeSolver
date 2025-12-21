from graphics import *

def main():
    win = Window(SCREEN_WIDTH, SCREEN_HEIGHT)
    rows = 20
    cols = 30
    row_width = 20
    col_width = 20
    seed = 0
    maze = Maze(rows, cols, row_width, col_width, win)
    maze._Maze__break_enterance_and_exit()
    maze._Maze__break_walls_r(0, 0)
    maze._Maze__reset_cells_visited()
    win.wait_for_close()


if __name__ == "__main__":
    main()