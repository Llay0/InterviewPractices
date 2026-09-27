# 1. Interviewer Prompt
- Create a 2-player Connect4 style game within a 7x6 grid where player's win by dropping coloured discs into the grid and lining 4 discs vertically, horizontally or diagonally in a row. 

# 2. Requirements
- 2 player experience (alternate turns)
- Grid of specified dimensions (7x6 in this example)
- Winner is decided as soon as player achieves 4 in a row (By default, other player loses)
- Draws are possible if the grid is full and no winning pattern exists
- Counters are dropped from the 'top' and fall to the lowest row in that column
- Players choose a column to drop their disc into
- Each player has their own uniquely coloured disc to identify their turns
- Track game state to alternate turns and assign wins or draws. 

# 3. Class Design

## Classes
- Player 
- Game
- Board


class Game:
    player1: Player class
    player2: Player class
    state: IN_PROGRESS, WIN, DRAW enum

    getTurn() -> int
    getState() -> state
    checkWin() -> bool
    checkMove() -> bool


enum state:
    IN_PROGRESS
    WIN
    DRAW


✅class Board:
    columns: COLS - assigned = 7
    rows: ROWS - assigned = 6

    Board(columns, rows) -> class
    getCols() -> columns
    getRows() -> rows
    validBoard() -> bool



✅class Player:
    name: string
    disc: RED, BLUE enum

✅enum Disc:
    RED
    BLUE


    



