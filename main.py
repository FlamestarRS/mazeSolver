from graphics import *

def main():
    win = Window(800, 600)
    test_line = Line(Point(400, 400), Point(300, 300))
    test_color = "red"
    win.draw_line(test_line, test_color)
    win.wait_for_close()

if __name__ == "__main__":
    main()