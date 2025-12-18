from graphics import *

def fill_test_grid(sq_size: int):
    test_grid = []
    rows = int(600 / sq_size)
    columns = int(800 / sq_size)
    for i in range(rows):
        if i % 2 == 0: # go left to right
            for j in range(columns):
                nw_point = Point(j*sq_size, i*sq_size)
                se_point = Point((j+1)*sq_size, (i+1)*sq_size)
                test_grid.append([nw_point, se_point])
        if i % 2 != 0: # go right to left
            for j in range(columns - 1, -1, -1):
                nw_point = Point(j*sq_size, i*sq_size)
                se_point = Point((j+1)*sq_size, (i+1)*sq_size)
                test_grid.append([nw_point, se_point])

    return test_grid