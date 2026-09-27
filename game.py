from enum import Enum
from board import Board

class Disc(Enum):
    RED = 1
    BLUE = 2

class Player:
    def __init__(self, name, colour):
        self.name = name
        self.colour = colour

class State(Enum):
    IN_PROGRESS = 1
    WIN = 2
    DRAW = 3

class Game:
    def __init__(self):
        self.player1 = Player('Player 1', Disc.RED.value)
        self.player2 = Player('Player 2', Disc.BLUE.value)
        self.state = State.IN_PROGRESS.value
        self.currentPlayer = 1
        self.board = Board().board
        self.rows = Board().getRows()
        self.cols = Board().getCols()
        self.moves = 0

    def getTurn(self) -> int:
        return self.currentPlayer

    def getState(self):
        return self.state

    def getBoard(self):
        return self.board

    def checkMove(self, move):
        if 0 > move > self.board.getCols():
            return -1

        if self.board[0][move] != 0:
            return -1

    def move(self, column):
        if self.checkMove(column) == -1:
            return -1 

        self.moves += 1

        lastMove = ()
        for row in range(len(self.board) - 1, -1, -1):
            if self.board[row][column] == 0:
                self.board[row][column] = self.player1.colour if self.currentPlayer == 1 else self.player2.colour
                lastMove = (row, column)
                break


        if self.checkWin(lastMove, self.currentPlayer):
            self.state = State.WIN.value

        if self.moves == self.rows * self.cols:
            self.state = State.DRAW.value

        if self.state == State.IN_PROGRESS.value:
            self.currentPlayer = 2 if self.currentPlayer == 1 else 1 

    def countInDirection(self, row, col, dr, dc, colour):
        count = 0
        r = row + dr
        c = col + dc
        while (0 <= r < self.rows and 0 <= c < self.cols) and self.board[r][c] == colour:
            count += 1
            r += dr
            c += dc
        return count
        
    def checkWin(self, move, colour) -> bool:
        row, col = move[0], move[1]
        directions = [[0, 1], [1, 0], [1, 1], [-1, 1]]
        for dx, dy in directions:
            count = 1
            count += self.countInDirection(row, col, dx, dy, colour)
            count += self.countInDirection(row, col, -dx, -dy, colour)
            if count >= 4:
                return True

        return False

    
