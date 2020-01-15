import csv
import copy
from mcts import mcts
from board import Board
import datetime
from multiprocessing import Process
import random

def play(player1exp):
      b = Board()

      player1 = mcts(iterationLimit=5000,  explorationConstant=player1exp)
      player2 = mcts(iterationLimit=5000)
      while not b.isOver:
         m = player1.search(copy.deepcopy(b))
         #print(m)
         b.makeMove(m)
         #print(b)
         if b.isOver:
            break
         m = player2.search(copy.deepcopy(b))
         #print(m)
         b.makeMove(m)

         #print(b)
     # print(f"WInner: {b.winner}")
      return b.winner
with open('results.csv', 'a') as csvfile:
   filewriter = csv.writer(csvfile, delimiter=',')
   filewriter.writerow(["time", "exp const","player1wins","player2wins"])


def playAndReport(exp, howMany):
   player1wins = 0
   player2wins = 0
   for _ in range (howMany):
      winner=play(exp)
      if winner == 1:
         player1wins+=1
      if winner == -1:
         player2wins+=1
      print (f"{exp} player1wins = {player1wins}")
      print (f"{exp} player2wins = {player2wins}")

   while True:
      try:
         with open('results.csv', 'a') as csvfile:
            time_string = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
            filewriter = csv.writer(csvfile, delimiter=',')
            filewriter.writerow([time_string, exp,player1wins,player2wins])
            break
      except:
         # if two processes access file at same time one will fail, so retry here
         print("retryng write to file")
         time.sleep(random.randint(1,5))
exp = 0.05
processes =[]
for _ in range(0,40):
   p = Process(target=playAndReport, args=(exp,100,))
   p.start()
   processes.append(p)
   exp+=0.05
#wait for all processses to finish
for p in processes:
   p.join()
