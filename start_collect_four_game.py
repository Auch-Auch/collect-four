from enum import Enum
from argparse import ArgumentParser, Namespace


NUM_PLAYERS = 2
ROWS = 6
COLUMNS = 7
PLACEHOLDER = "."


class Player(str, Enum):
    RED = "R"
    YELLOW = "Y"
    GREEN = "G"
    BLUE = "B"
    PURPLE = "P"
    ORANGE = "O"


class Board:
    def __init__(self, rows: int = ROWS, columns: int = COLUMNS):
        self.rows = rows
        self.columns = columns
        self._board = [[PLACEHOLDER for _ in range(columns)] for _ in range(rows)]

    def update_board(self, column: int, player: Player) -> bool:
        if (
            column < 0
            or column >= self.columns
            or self._board[0][column] != PLACEHOLDER
        ):
            return False
        for row in reversed(range(self.rows)):
            if self._board[row][column] == PLACEHOLDER:
                self._board[row][column] = player
                return True
        return False

    def __getitem__(self, row_index: int) -> list[str]:
        return self._board[row_index]

    def __str__(self) -> str:
        rows = [" ".join(row) for row in self._board]
        return "\n".join(rows) + "\n" + " ".join(map(str, range(self.columns)))

    def reset(self) -> None:
        self._board = [
            [PLACEHOLDER for _ in range(self.columns)] for _ in range(self.rows)
        ]


def init_board(rows: int = ROWS, columns: int = COLUMNS) -> Board:
    return Board(rows, columns)


def is_draw(board: Board) -> bool:
    return all(board[0][col] != PLACEHOLDER for col in range(board.columns))


def is_player_won(board: Board, player: Player) -> bool:
    rows, columns = board.rows, board.columns

    # Horizontal check
    for row in range(rows):
        for col in range(columns - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True

    # Vertical check
    for col in range(columns):
        for row in range(rows - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    # Diagonal down-right check
    for row in range(rows - 3):
        for col in range(columns - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    # Diagonal down-left check
    for row in range(rows - 3):
        for col in range(3, columns):
            if all(board[row + i][col - i] == player for i in range(4)):
                return True

    return False


def get_players(num_of_players: int = NUM_PLAYERS) -> list[Player]:
    all_colors = list(Player)
    if num_of_players > len(all_colors):
        print(f"Too many players! Only {len(all_colors)} colors supported.")
        return []
    players = all_colors[:num_of_players]
    return players


def start_game_loop(args: Namespace) -> None:
    print(
        "You are playing Connect Four! Two players RED and YELLOW take turns dropping pieces into the board. The first player to get four in a row wins."
    )
    board = init_board(args.rows, args.columns)
    players = get_players(args.players)
    if not players:
        return
    while True:
        board.reset()
        turn = 0
        while True:
            print(board)
            current_player = players[turn % len(players)]
            try:
                column = int(
                    input(
                        f"Player {current_player.name}, choose a column (0-{board.columns - 1}): "
                    )
                )
            except ValueError:
                print("Invalid number.")
                continue
            except KeyboardInterrupt:
                print("\nGame ended. Goodbye!")
                return

            if not 0 <= column < board.columns:
                print("Invalid column.")
                continue

            if not board.update_board(column, current_player):
                print("Cannot make that move.")
                continue

            if is_player_won(board, current_player):
                print(board)
                print(f"Player {current_player.name} wins!")
                break

            if is_draw(board):
                print(board)
                print("It's a draw!")
                break

            turn += 1

        try:
            again = input("Play again? (y/n): ").strip().lower()
        except KeyboardInterrupt:
            print("\nGame ended. Goodbye!")
            return

        if again != "y":
            print("Thanks for playing!")
            break


def main():
    arg_parser = ArgumentParser("Connect Four game")
    arg_parser.add_argument(
        "--columns", type=int, default=COLUMNS, help="Number of columns"
    )
    arg_parser.add_argument("--rows", type=int, default=ROWS, help="Number of rows")
    arg_parser.add_argument(
        "--players", type=int, default=NUM_PLAYERS, help="Number of players"
    )
    args = arg_parser.parse_args()
    start_game_loop(args)


if __name__ == "__main__":
    main()
