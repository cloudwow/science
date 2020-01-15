import copy
from mcts import mcts
from board import Board

def play():
      b = Board()

      player1 = mcts(iterationLimit=500)
      player2 = mcts(iterationLimit=500)
      while not b.isOver:
         m = player1.search(copy.deepcopy(b))
         print(m)
         b.makeMove(m)
         print(b)
         if b.isOver:
            break
         m = player2.search(copy.deepcopy(b))
         print(m)
         b.makeMove(m)

         print(b)
      print(f"WInner: {b.winner}")


play()
