from start_collect_four_game import Board, Player, is_player_won, is_draw

def test_board_initialization():
    board = Board()
    assert board.rows == 6
    assert board.columns == 7

    for row in board._board:
        assert all(cell == '.' for cell in row)


def test_update_board():
    board = Board()
    assert board.update_board(0, Player.RED) is True
    assert board._board[board.rows - 1][0] == Player.RED


def test_update_board_invalid_column():
    board = Board()
    assert board.update_board(-1, Player.RED) is False
    assert board.update_board(board.columns, Player.RED) is False


def test_horizontal_win():
    board = Board()
    row = board.rows - 1
    for col in range(4):
        board._board[row][col] = Player.RED
    assert is_player_won(board, Player.RED)


def test_vertical_win():
    board = Board()
    col = 0
    for row in range(4):
        board._board[row][col] = Player.YELLOW
    assert is_player_won(board, Player.YELLOW)


def test_is_draw():
    board = Board()

    for col in range(board.columns):
        board._board[0][col] = Player.RED
    assert is_draw(board)


def test_is_not_draw():
    board = Board()

    assert not is_draw(board)


def test_diagonal_down_right_win():
    board = Board()
    for i in range(4):
        board._board[i][i] = Player.RED
    assert is_player_won(board, Player.RED)


def test_diagonal_down_left_win():
    board = Board()
    start_col = 3
    for i in range(4):
        board._board[i][start_col - i] = Player.YELLOW
    assert is_player_won(board, Player.YELLOW)
