import dataclasses
import pandas as pd

try:
    from bingo import APP_NAME
    from bingo.game import BingoGame
    from bingo.custom_logger import getLogger
except ImportError:
    print("ERROR: are you running using python -m bingo.{XXX}?")
    raise


lg = getLogger(APP_NAME)


@dataclasses.dataclass
class GameData:
    board_size: int
    number_pool_size: int
    num_boards: int
    winning_number_size: int
    winning_boards_count: int


def simulate_game(
    num_boards: int = 350,
    number_pool_size: int = 88,
    board_size: int = 6,
    winning_number_size: int = 50,
) -> None:
    """
    Main function to demonstrate the Bingo game.
    """
    lg.info(
        f"simulating {num_boards=}, {number_pool_size=}, {board_size=}, {winning_number_size=}..."
    )
    game = BingoGame(
        size=board_size, number_pool_size=number_pool_size
    )  # Common Bingo size and pool
    boards = [game.generate_board() for _ in range(num_boards)]
    lg.debug(f"Generated {len(boards)} Bingo boards.")
    game.generate_winning_numbers(count=winning_number_size)
    winning_count = game.count_winning_boards(boards)
    lg.info(f"  >> {winning_count=}")
    return GameData(
        board_size=board_size,
        number_pool_size=number_pool_size,
        num_boards=num_boards,
        winning_number_size=winning_number_size,
        winning_boards_count=winning_count,
    )
    # board.print_board()

    # # Validate the board against the drawn winning numbers
    # is_winner = game.validate_board(board, print_marked_board=True)
    # print(f"\nIs the board a winner? {is_winner}")


def run_simulation(n: int = 20):
    """
    Run the simulation and print the results.
    """
    datalist = []
    for i in range(n):
        lg.info(f"Running simulation {i + 1}/{n}")
        datalist.append(
            simulate_game(
                num_boards=250,
                number_pool_size=200,
                board_size=6,
                winning_number_size=60,
            )
        )

    df = pd.DataFrame(datalist)
    print(df)


if __name__ == "__main__":
    run_simulation()
