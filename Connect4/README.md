# Connect4

A small Python implementation of a two-player Connect Four-style game. The intended game uses a 7-column by 6-row grid, alternates between two players, drops discs to the lowest available position in a selected column, and detects horizontal, vertical, and diagonal lines of four discs.

## Project Contents

| File | Purpose |
| --- | --- |
| `board.py` | Defines the default board dimensions and the `Board` class. |
| `game.py` | Defines discs, players, game states, and the core `Game` rules. |
| `connect4.py` | Provides the command-line game loop and board renderer. |
| `plan.md` | Records the interview prompt, requirements, and proposed class design. |

## Requirements and Intended Rules

The design described in `plan.md` calls for:

- Two players taking alternating turns.
- A default 7-column by 6-row grid.
- Players selecting a column rather than a specific row.
- A disc falling to the lowest empty row in that column.
- Distinct discs for each player: red and blue.
- A win when a player creates four consecutive discs horizontally, vertically, or diagonally.
- A draw when the grid is full without a winner.
- Game-state tracking for an in-progress game, a win, or a draw.

## How-To Guide

### Run the command-line game

Run the module from the directory above `Connect4` so the package import works:

```powershell
python -m Connect4.connect4
```

The program prompts for a column number, attempts to place the current player's disc, prints the board, and reports the move count. Input is expected to be an integer. The game ends when its state changes from `IN_PROGRESS` to `WIN` or `DRAW`.

> Current implementation note: the first move currently cannot complete because `Game.checkMove()` calls `getCols()` on `self.board`, while `Game.__init__()` stores only `Board().board`, which is a list. See [Known Issues](#known-issues).

### Use the game model from Python

Once the board ownership issue is corrected, the intended usage is:

```python
from Connect4.game import Game

game = Game()
game.move(3)
print(game.getBoard())
print(game.getTurn())
print(game.getState())
```

Columns are zero-based, so `3` selects the fourth column. A successful move updates the board and changes the turn while the game remains in progress. An invalid move returns `-1`.

### Change the default board configuration

`Board` accepts custom dimensions and a custom winning line length:

```python
from Connect4.board import Board

board = Board(cols=8, rows=7, winning_disc_count=4)
print(board.getCols())
print(board.getRows())
print(board.validBoard())
```

The current `Game` class always creates its own default board, so custom `Board` instances are not yet wired into a `Game`.

### Render a board

`connect4.print_board(board)` prints a two-dimensional list as an ASCII grid. Cell value `1` is shown as a blue terminal disc, cell value `2` as a red terminal disc, and `0` as an empty space. ANSI color support depends on the terminal.

## API Breakdown

### `board.py`

#### Module constants

- `DEFAULT_ROWS = 6`: Default number of board rows.
- `DEFAULT_COLS = 7`: Default number of board columns.
- `DEFAULT_WINNING_DISC_COUNT = 4`: Default number of consecutive discs needed to win.

#### `Board`

`Board` creates and describes a rectangular board. Its internal `board` value is a two-dimensional list initialized with `0` values.

- `__init__(cols=DEFAULT_COLS, rows=DEFAULT_ROWS, winning_disc_count=DEFAULT_WINNING_DISC_COUNT)`: Stores the board dimensions and winning line length, then creates `rows` lists containing `cols` empty cells.
- `getCols() -> int`: Returns the configured column count.
- `getRows() -> int`: Returns the configured row count.
- `validBoard() -> bool`: Returns `True` when both dimensions are greater than the winning line length. It does not validate types, negative values, or the actual contents of the board.

### `game.py`

#### `Disc`

An `Enum` containing the two player disc values:

- `Disc.RED = 1`
- `Disc.BLUE = 2`

#### `Player`

Stores player identity and disc color.

- `__init__(name, colour)`: Sets `name` and `colour` attributes. The current game passes `1` for red and `2` for blue.

#### `State`

An `Enum` containing the game states:

- `State.IN_PROGRESS = 1`
- `State.WIN = 2`
- `State.DRAW = 3`

#### `Game`

Owns the players, board data, turn, move count, and state transitions.

- `__init__()`: Creates Player 1 with a red disc and Player 2 with a blue disc, initializes the game as in progress, sets Player 1 as current, creates a default board, and sets the move count to zero.
- `getTurn() -> int`: Returns `1` or `2` for the current player.
- `getState()`: Returns the numeric state value used by the implementation: `1` in progress, `2` win, or `3` draw.
- `getBoard()`: Returns the internal two-dimensional board list.
- `checkMove(move)`: Intended to reject a column outside the board or a full column by returning `-1`. The current implementation has a board ownership bug described below.
- `move(column)`: Validates and applies a move, drops the current player's disc into the lowest empty cell, increments the move count, checks for a win, checks for a full board, and switches players if the game remains in progress. It returns `-1` for an invalid move and otherwise currently returns `None`.
- `countInDirection(row, col, dr, dc, colour)`: Counts matching discs starting from the neighboring cell in direction `(dr, dc)` until the board edge or a different value is reached.
- `checkWin(move, colour) -> bool`: Checks four directions around the most recently placed disc: horizontal, vertical, and the two diagonal orientations. It returns `True` when the total connected count reaches four.

### `connect4.py`

- `print_board(board)`: Prints a two-dimensional board with borders. It returns immediately for an empty board, maps `1` and `2` to colored disc characters, and prints empty cells as spaces.
- Main program block: Creates a `Game`, repeatedly reads a column from standard input while the game is in progress, retries invalid moves, prints the board and move count, and reports either a draw or the winning player.

## Known Issues

The repository currently contains an incomplete integration between `Board` and `Game`:

```python
self.board = Board().board
```

This assignment stores the raw list, but `checkMove()` later evaluates `self.board.getCols()`. Lists do not provide `getCols()`, so the first call to `move()` raises `AttributeError` before a move is validated. The intended fix is to retain a `Board` instance or retain the dimensions separately and have `checkMove()` use them consistently.

There are also a few behavior details to address for production-quality play:

- `checkMove()` uses `if 0 > move > self.board.getCols()`, which does not reject all invalid column values. A lower-and-upper-bound check should be explicit.
- `connect4.py` converts input directly with `int()`, so non-numeric input raises `ValueError`.
- `Game` uses numeric values from `State` rather than storing `State` enum members directly.
- `Game` currently hard-codes four in `checkWin()` rather than reading a configurable winning-disc count from `Board`.
- `Board.validBoard()` requires dimensions to be strictly greater than the winning count, which may be stricter than necessary for some valid custom boards.

## Suggested Next Steps

1. Keep the `Board` object inside `Game` and expose its cell grid deliberately.
2. Correct column bounds and full-column validation.
3. Handle non-numeric and out-of-range command-line input without terminating the program.
4. Add unit tests for horizontal, vertical, and both diagonal wins, invalid moves, draws, and turn changes.
5. Inject a custom `Board` into `Game` if configurable dimensions are required.