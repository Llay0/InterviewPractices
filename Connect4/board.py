DEFAULT_ROWS = 6
DEFAULT_COLS = 7
DEFAULT_WINNING_DISC_COUNT = 4

class Board:
    def __init__(self, cols=DEFAULT_COLS, rows=DEFAULT_ROWS, winning_disc_count=DEFAULT_WINNING_DISC_COUNT):
        self.cols = cols
        self.rows = rows 
        self.winning_disc_count = winning_disc_count
        self.board = [[0] * cols for _ in range(rows)]  

    def getCols(self) -> int:
        return self.cols

    def getRows(self) -> int:
        return self.rows

    def validBoard(self) -> bool:
        return self.rows > self.winning_disc_count and self.cols > self.winning_disc_count
