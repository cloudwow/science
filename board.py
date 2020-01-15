import numpy as np
BOARD_WIDTH = 9


class Move:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Move):
            return self.__key() == other.__key()
        return False

    def __key(self):
        return (self.x, self.y)

    def __hash__(self):
        return hash(self.__key())

    def __str__(self):
        return f"({self.x},{self.y})"


class Board:
    def __init__(self):
        self.cells = np.zeros((BOARD_WIDTH, BOARD_WIDTH))
        self.available_moves = set()

        for x in range(BOARD_WIDTH):
            for y in range(BOARD_WIDTH):
                self.available_moves.add(Move(x, y))
        self.current_player = 1
        self.move_stack = []
        self._winner = 0

    def get(self, x, y):
        return self.cells[y][x]

    @property
    def currentPlayer(self):
        return self.current_player

    @property
    def isOver(self):
        return self.hasWinner() or len(self.available_moves) == 0

    @property
    def winner(self):
        return self._winner

    def hasWinner(self):
        return self._winner != 0

    @property
    def availableMoves(self):
        if self.hasWinner():
            return []
        return self.available_moves

    @property
    def lastMove():
        return self.move_stack[-1]

    def __str__(self):
        return self.cells.__str__()

    def makeMove(self, move):
        if self.hasWinner():
            raise Exception("game has already been won")
        if not move in self.available_moves:
            raise Exception(f"invalid move: {move}")
        self.available_moves.remove(move)
        self.cells[move.y][move.x] = self.current_player
        self.move_stack.append(move)
        self.lookForWin(move)
        self.current_player *= -1

    def lookForWin(self, fromMove):
        inARow = 0
        for x in range(fromMove.x-4, fromMove.x+5):
            if x >= 0 and x < BOARD_WIDTH and self.cells[fromMove.y][x] == self.current_player:
                inARow += 1
                if inARow == 5:
                    self._winner = self.current_player
                    return
            else:
                inARow = 0
        inARow = 0
        for y in range(fromMove.y-4, fromMove.y+5):

            if y >= 0 and y < BOARD_WIDTH and self.cells[y][fromMove.x] == self.current_player:
                inARow += 1
                if inARow == 5:

                    self._winner = self.current_player
                    return
            else:
                inARow = 0

        inARow = 0
        for d in range(-4, +5):
            x = fromMove.x+d
            y = fromMove.y+d
            if x >= 0 and x < BOARD_WIDTH and y >= 0 and y < BOARD_WIDTH and self.cells[y][x] == self.current_player:
                inARow += 1
                if inARow == 5:

                    self._winner = self.current_player
                    return
            else:
                inARow = 0
        for d in range(-5, +5):
            x = fromMove.x+d
            y = fromMove.y-d
            if x >= 0 and x < BOARD_WIDTH and y >= 0 and y < BOARD_WIDTH and self.cells[y][x] == self.current_player:
                inARow += 1
                if inARow == 5:

                    self._winner = self.current_player
                    return
            else:
                inARow = 0

    def undoLastMove(self):
        move = self.move_stack.pop()
        self.cells[move.y][move.x] = 0
        self.available_moves.add(move)
        self.current_player *= -1
        self._winner = 0


if __name__ == "__main__":
    b = Board()
    print(b)

    m11 = Move(1, 1)
    m22 = Move(2, 2)
    m33 = Move(3, 3)
    print(m11 == m11)
    print(m11 == m22)
    b.makeMove(m11)
    b.makeMove(m22)
    b.makeMove(Move(1, 2))
    b.makeMove(Move(2, 3))
    b.makeMove(Move(1, 3))
    b.makeMove(Move(2, 4))
    b.makeMove(Move(1, 4))
    b.makeMove(Move(5, 2))

    print(f"has winner: {b.hasWinner()}")
    b.makeMove(Move(1, 5))
    print(f"has winner: {b.hasWinner()}")
    print(b)
    b.undo_last_move()

    b.makeMove(m33)
 #   print(b)
