from Connect4.game import Game


def print_board(board):
    """Print a two-dimensional board in a Connect Four-style grid."""
    if not board:
        return

    width = len(board[0])
    border = '+' + '---+' * width
    for row in board:
        print(border)
        def colored_disc(cell):
            if cell == 1:
                return '\033[34m●\033[0m'
            if cell == 2:
                return '\033[31m●\033[0m'
            return ' '

        print('|' + '|'.join(f' {colored_disc(cell)} ' for cell in row) + '|')
    print(border)


if __name__ == '__main__':
    game = Game()
    # game.move(1)
    # game.move(1)
    # game.move(2)
    # game.move(4)
    

    while game.state == 1:
        column = int(input('Input column for your move: '))
        while game.move(column) == -1:
            print('Invalid move!')
            column = int(input('Input column for your move: '))


        print_board(game.getBoard())
        print(f'Move: {game.moves}')

    if game.state == 3:
        print('It is a draw!')
        
    else:
        print(f'Player {game.currentPlayer} wins!')


    