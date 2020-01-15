import csv
import copy
from mcts import mcts
from board import Board
import datetime
from multiprocessing import Process
import random
PLAYER_1 = 1
PLAYER_2 = -1
NOBODY = 0
def play_one_game(player1exp):
   """ Play one game where player 1 has the supplied exploration constant.
       returns the winner of the game or NOBODY if the game was a draw."""
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


def playAndReport(exploration_constant, how_many_games, filename):
   """ Play a series of games where player 1 has the supplied exploration constant.
       Writes the win counts to results.csv """
   player1wins = 0
   player2wins = 0
   for _ in range (how_many_games):
      winner=play_one_game(exploration_constant)
      if winner == PLAYER_1:
         player1wins+=1
      elif winner == PLAYER_2:
         player2wins+=1
      print (f"{exploration_constant} player1wins = {player1wins}")
      print (f"{exploration_constant} player2wins = {player2wins}")

   while True:
      try:
         with open(filename, 'a') as csvfile:
            time_string = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
            filewriter = csv.writer(csvfile, delimiter=',')
            filewriter.writerow([time_string, exp,player1wins,player2wins])
            break
      except:
         # if two processes access file at same time one will fail, so retry here
         print("retryng write to file")
         time.sleep(random.randint(1,5))
#######################################
# start a new CSV (spreadsheet) file.  Upload this to Google drive.
filename = 'Results_{0:%Y-%m-%d_%H_%M_%S}.csv'.format(datetime.datetime.now())

with open(filename, 'w') as csvfile:
   filewriter = csv.writer(csvfile, delimiter=',')
   filewriter.writerow(["time", "exp const","player1wins","player2wins"])

exploration_constant = 0.05
processes =[]
# Evaluate 40 different exploration constants.
for _ in range(0,40):
   # Run 100 games with the exploration constant.
   # Create a dedicated process for running those 100 games.
   p = Process(target=playAndReport, args=(exploration_constant,100,filename))
   p.start()
   #keep a list of all of the proccesses so that we can wait for them all to finish.
   processes.append(p)
   exploration_constant+=0.05
#wait for all processses to finish
for p in processes:
   p.join()
