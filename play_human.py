import copy
from mcts import mcts
from board import Board
import tkinter as tk
from board_gui import BoardFrame


def playHuman():
   print("mcts goes first.  it can take a while...")
   b = Board()
   player1 = mcts(iterationLimit=5000)
   window = tk.Tk()
   window.wm_title("GOMOKU GAME")
   gui= BoardFrame(master= window, board=b, player1=player1)
   gui.pack()

   window.mainloop()

playHuman()