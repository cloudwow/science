import tkinter as tk
import math
from board  import Move
BLACK = -1
WHITE = 1

CELL_PIXELS = 80


class BoardCanvas(tk.Canvas):

    def drawState(self):
        for i in range(9):
            for j in range(9):
                piece = self.board.get(i, j)
                if piece == 0:
                    continue
                if piece == 1:
                    color = WHITE
                else:
                    color = BLACK
                self.draw_stone(i, j, color)

    def __init__(self,  board, player1, height=0, width=0, master=None,):
        tk.Canvas.__init__(self, master,  height=height, width=width)
        self.draw_gameBoard()
        self.turn = 2
        self.undo = False
        self.depth = 2
        self.prev_exist = False
        self.prev_row = 0
        self.prev_col = 0
        self.player1 = player1
        self.board = board

    def draw_gameBoard(self):
        """Plot the game board."""

        # 15 horizontal lines
        for i in range(9):
            start_pixel_x = (i + 1) * CELL_PIXELS
            start_pixel_y = (0 + 1) * CELL_PIXELS
            end_pixel_x = (i + 1) * CELL_PIXELS
            end_pixel_y = (9 + 1) * CELL_PIXELS
            self.create_line(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y)

        # 15 vertical lines
        for j in range(9):
            start_pixel_x = (0 + 1) * CELL_PIXELS
            start_pixel_y = (j + 1) * CELL_PIXELS
            end_pixel_x = (9 + 1) * CELL_PIXELS
            end_pixel_y = (j + 1) * CELL_PIXELS
            self.create_line(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y)

        # place a "star" to particular intersections
        self.draw_star(3, 3)
        self.draw_star(7, 7)

    def draw_star(self, row, col):
        """Draw a "star" on a given intersection

        Args:
                row, col (i.e. coord of an intersection)
        """
        start_pixel_x = (row + 1) * CELL_PIXELS - 2
        start_pixel_y = (col + 1) * CELL_PIXELS - 2
        end_pixel_x = (row + 1) * CELL_PIXELS + 2
        end_pixel_y = (col + 1) * CELL_PIXELS + 2

        self.create_oval(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y, fill='black')

    def draw_stone(self, row, col, color):
        """Draw a stone (with a circle on it to denote latest move) on a given intersection.

        Specify the color of the stone depending on the turn.

        Args:
                row, col (i.e. coord of an intersection)
        """

        inner_start_x = (row + 1) * CELL_PIXELS - 12
        inner_start_y = (col + 1) * CELL_PIXELS - 12
        inner_end_x = (row + 1) * CELL_PIXELS + 12
        inner_end_y = (col + 1) * CELL_PIXELS + 12

        outer_start_x = (row + 1) * CELL_PIXELS - 14
        outer_start_y = (col + 1) * CELL_PIXELS - 14
        outer_end_x = (row + 1) * CELL_PIXELS + 14
        outer_end_y = (col + 1) * CELL_PIXELS + 14

        start_pixel_x = (row + 1) * CELL_PIXELS - 17
        start_pixel_y = (col + 1) * CELL_PIXELS - 17
        end_pixel_x = (row + 1) * CELL_PIXELS + 17
        end_pixel_y = (col + 1) * CELL_PIXELS + 17

        if color == BLACK:
            self.create_oval(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y, fill='black')
            self.create_oval(outer_start_x, outer_start_y, outer_end_x, outer_end_y, fill='white')
            self.create_oval(inner_start_x, inner_start_y, inner_end_x, inner_end_y, fill='black')
        else:
            self.create_oval(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y, fill='white')
            self.create_oval(outer_start_x, outer_start_y, outer_end_x, outer_end_y, fill='black')
            self.create_oval(inner_start_x, inner_start_y, inner_end_x, inner_end_y, fill='white')

    def draw_prev_stone(self, row, col):

        start_pixel_x = (row + 1) * CELL_PIXELS - 10
        start_pixel_y = (col + 1) * CELL_PIXELS - 10
        end_pixel_x = (row + 1) * CELL_PIXELS + 10
        end_pixel_y = (col + 1) * CELL_PIXELS + 10

        if self.turn == 1:
            self.create_oval(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y, fill='white')
        elif self.turn == 2:
            self.create_oval(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y, fill='black')

    def doUserMove(self, event):
        pass


class BoardFrame(tk.Frame):
    """The Frame Widget is mainly used as a geometry master for other widgets, or to
    provide padding between other widgets.
    """

    def __init__(self, board, player1, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.board = board
        self.player1 = player1
        self.create_widgets(board, player1)

        master.after(500, self.gameLoop)

    def handleUserInput(self,  event):
        for i in range(9):
                for j in range(9):
                    pixel_x = (i + 1) * CELL_PIXELS
                    pixel_y = (j + 1) * CELL_PIXELS
                    square_x = math.pow((event.x - pixel_x), 2)
                    square_y = math.pow((event.y - pixel_y), 2)
                    distance = math.sqrt(square_x + square_y)
                     # since there is noly one intersection such that the distance between it
                    # and where the user clicks is less than 15, it is not necessary to find
                    # the actual least distance
                    if (distance < 15):
                        print(f"board pos {i},{j}")
                        if  self.board.get( i,j) != 0:
                            print(f"board pos {i},{j} already has piece {self.board.get( i,j) }")
                            return

                        move=Move( i,j)
                        print(f"User's move is {move}")
                        self.board.makeMove(move)
                        invalid_pos=False
                        row, col=i, j

                        self.boardCanvas.drawState()
                        self.master.update()
                        print(self.board)
                        self.unbind('<Button-1>')
                        self.master.after(100, self.gameLoop)

    def die(self):
        self.master.destroy()
    def gameLoop(self):
       # while True:
            if self.board.isOver:
                print(f"Winner: {self.board.winner}")
                self.master.after(100, self.die)
                return

            move=self.player1.getMove(self.board)
            print(f"mcts move is {move}")

            self.board.makeMove(move)
            print(self.board)
            self.boardCanvas.drawState()
            self.master.update()
            if self.board.isOver:
                print(f"Winner: {self.board.winner}")
                self.master.after(100, self.die)
            else:
                self.boardCanvas.bind('<Button-1>', self.handleUserInput)
    def create_widgets(self, board, player1):
        self.boardCanvas=BoardCanvas(board = board, height = CELL_PIXELS*9+200,
                                     width = CELL_PIXELS*9+200, player1 = player1)
        self.boardCanvas.pack()

    def setState(self, board):
        self.boardCanvas.drawState(board)
