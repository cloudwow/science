from __future__ import division

import time
import math
import random
import copy
import random

def rollout(board, player):
    while not board.isOver:
        move = random.sample(board.availableMoves, 1)[0]
        board.makeMove(move)
    # if player is -1 and player one than reward is 1
    return board.winner * player


class treeNode():
    def __init__(self, state, parent):
        self.state = state
        self.isTerminal = state.isOver
        self.isFullyExpanded = self.isTerminal
        self.parent = parent
        self.numVisits = 0
        self.totalReward = 0
        self.children = {}


class mcts():
    def __init__(self, timeLimit=None, iterationLimit=None, explorationConstant=1 / math.sqrt(2)):

        if timeLimit != None:
            if iterationLimit != None:
                raise ValueError("Cannot have both a time limit and an iteration limit")
            # time taken for each MCTS search in milliseconds
            self.timeLimit = timeLimit
            self.limitType = 'time'
        else:
            if iterationLimit == None:
                raise ValueError("Must have either a time limit or an iteration limit")
            # number of iterations of the search
            if iterationLimit < 1:
                raise ValueError("Iteration limit must be greater than one")
            self.searchLimit = iterationLimit
            self.limitType = 'iterations'
        self.explorationConstant = explorationConstant
    def getMove(self, board):
        return self.search(board)

    def search(self, initialState):
        self.search_player = initialState.currentPlayer;
        self.root = treeNode(initialState, None)

        if self.limitType == 'time':
            timeLimit = time.time() + self.timeLimit / 1000
            while time.time() < timeLimit:
                self.executeRound()
        else:
            for i in range(self.searchLimit):
                self.executeRound()

        bestChild = self.getBestChild(self.root, 0)
        return self.getAction(self.root, bestChild)

    def executeRound(self):
        """expand one node """
        node = self.selectNode(self.root)
        reward = rollout(copy.deepcopy(node.state), self.search_player)
        self.backpropogate(node, reward)

    def selectNode(self, node):
        """ find the best node to expand"""
        while not node.isTerminal:
            if node.isFullyExpanded:
                node = self.getBestChild(node, self.explorationConstant)
            else:
                return self.expand(node)
        return node

    def expand(self, node):
        actions = node.state.availableMoves
        for action in actions:
            if action not in node.children:
                node.state.makeMove(action)
                # make a copy of the board with that move
                newState = copy.deepcopy(node.state)
                # undo the move to put node's state back where it was
                node.state.undoLastMove()
                newNode = treeNode(newState, node)
                node.children[action] = newNode
                if len(actions) == len(node.children):
                    node.isFullyExpanded = True
                return newNode

        raise Exception("Should never reach here")

    def backpropogate(self, node, reward):
        while node is not None:
            node.numVisits += 1
            node.totalReward += reward
            node = node.parent

    def getBestChild(self, node, explorationValue):
        bestValue = float("-inf")
        bestNodes = []
        for child in node.children.values():
            nodeValue =child.totalReward / child.numVisits + explorationValue * math.sqrt(
                2 * math.log(node.numVisits) / child.numVisits)
            if nodeValue > bestValue:
                bestValue = nodeValue
                bestNodes = [child]
            elif nodeValue == bestValue:
                bestNodes.append(child)
        return random.choice(bestNodes)

    def getAction(self, root, bestChild):
        for action, node in root.children.items():
            if node is bestChild:
                return action
