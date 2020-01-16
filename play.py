import time
import random
from multiprocessing import Process
import datetime
from board import Board
from mcts import mcts
import copy
import csv
MAX_ITERATIONS = 5000
HOW_MANY_ROUNDS = 40
GAMES_PER_ROUND = 100
LOWEST_EXPLORATION_CONSTANT = 0.225
HIGHEST_EXPLORATION_CONSTANT = 0.625


PLAYER_1 = 1
PLAYER_2 = -1
NOBODY = 0


def play_one_game(player1exp):
    """ Play one game where player 1 has the supplied exploration constant.
        returns the winner of the game or NOBODY if the game was a draw."""
    b = Board()

    player1 = mcts(iterationLimit=MAX_ITERATIONS,  explorationConstant=player1exp)
    player2 = mcts(iterationLimit=MAX_ITERATIONS)
    while not b.isOver:
        m = player1.search(copy.deepcopy(b))
        # print(m)
        b.makeMove(m)
        # print(b)
        if b.isOver:
            break
        m = player2.search(copy.deepcopy(b))
        # print(m)
        b.makeMove(m)

        # print(b)
    # print(f"WInner: {b.winner}")
    return b.winner


def playAndReport(exploration_constant, how_many_games, filename):
    """ Play a series of games where player 1 has the supplied exploration constant.
        Writes the win counts to results.csv """
    player1wins = 0
    player2wins = 0
    draws = 0
    for _ in range(how_many_games):
        winner = play_one_game(exploration_constant)
        if winner == PLAYER_1:
            player1wins += 1
        elif winner == PLAYER_2:
            player2wins += 1
        else:
            draws +=1
        print(f"{round(exploration_constant,2)} player1={player1wins}. player2={player2wins}, draws={draws}")

    while True:
        try:
            with open(filename, 'a') as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',')
                filewriter.writerow([ round(exploration_constant, 5), player1wins, player2wins, draws])
                break
        except:
            # if two processes access file at same time one will fail, so retry here
            print("retryng write to file")
            time.sleep(random.randint(1, 5))


#######################################
# start a new CSV (spreadsheet) file.  Upload this to Google drive.
filename = 'Results_{0:%Y-%m-%d_%H_%M_%S}.csv'.format(datetime.datetime.now())

with open(filename, 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',')
    filewriter.writerow([ "exp const", "player1wins", "player2wins, draws"])

exploration_constant = LOWEST_EXPLORATION_CONSTANT
processes = []
exploration_constant = LOWEST_EXPLORATION_CONSTANT
for _ in range(HOW_MANY_ROUNDS):
    # Run GAMES_PER_ROUND  games with the exploration constant.
    # Create a dedicated process for running those 100 games.
    p = Process(target=playAndReport, args=(exploration_constant, GAMES_PER_ROUND, filename))
    p.start()
    # keep a list of all of the proccesses so that we can wait for them all to finish.
    processes.append(p)
    exploration_constant += ((HIGHEST_EXPLORATION_CONSTANT-LOWEST_EXPLORATION_CONSTANT)/(HOW_MANY_ROUNDS-1))
# wait for all processses to finish
for p in processes:
    p.join()
