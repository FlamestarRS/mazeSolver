import unittest
from graphics import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 10
        num_rows = 12
        m1 = Maze(num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._Maze__cells),
            num_rows,
        )
        self.assertEqual(
            len(m1._Maze__cells[0]),
            num_cols,
        )

    def test_maze_reset_cells_visited(self):
        num_cols = 10
        num_rows = 12
        m1 = Maze(num_rows, num_cols, 10, 10)
        m1._Maze__break_enterance_and_exit()
        m1._Maze__break_walls_r(0, 0)
        m1._Maze__reset_cells_visited()
        for row in m1._Maze__cells:
            for cell in row:
                self.assertEqual(
                    cell.visited,
                    False,
                )

if __name__ == "__main__":
    unittest.main()