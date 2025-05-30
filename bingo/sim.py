import pandas as pd

from bingo import APP_NAME
from bingo.custom_logger import getLogger
from bingo.game import BingoGame
from bingo.models import GameData
from bingo.database import SQLiteDatabase

lg = getLogger(APP_NAME)


def simulate_game(
    num_boards: int = 350,
    number_pool_size: int = 88,
    board_size: int = 6,
    winning_number_size: int = 50,
) -> GameData:  # Changed return type hint to GameData
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


def run_simulation(n: int = 30):
    """
    Run the simulation and save the results to a SQLite database.
    """
    sqdb = SQLiteDatabase()

    try:
        for i in range(n):
            lg.info(f"Running simulation {i + 1}/{n}")
            for number_pool_size in range(60, 150 + 1, 10):
                for num_board in [200, 250, 300, 350, 400]:
                    for winning_size in range(30, 90 + 1, 5):
                        lg.info(f"Running with winning_number_size={winning_size}")
                        if number_pool_size < winning_size:
                            lg.warning(
                                f"Skipping simulation: {number_pool_size=} < {winning_size=}"
                            )
                            continue
                        game_data = simulate_game(
                            num_boards=num_board,
                            number_pool_size=number_pool_size,
                            board_size=7,
                            winning_number_size=winning_size,
                        )
                        sqdb.insert_game_data(game_data)
            # game_data = simulate_game(
            #     num_boards=250,
            #     number_pool_size=120,
            #     board_size=7,
            #     winning_number_size=60,
            # )
            # sqdb.insert_game_data(game_data)

        # Optionally, fetch and print all data from the DB after simulations
        lg.info("\n--- All simulation results from database ---")
        cursor = sqdb.connection.cursor()
        cursor.execute(
            f"SELECT * FROM simulations ORDER BY timestamp_entry DESC LIMIT {n}"
        )
        rows = cursor.fetchall()
        if rows:
            # Get column names for better DataFrame representation
            col_names = [description[0] for description in cursor.description]
            df = pd.DataFrame(rows, columns=col_names)
            print(df)
        else:
            lg.info("No simulation data found in the database.")

    finally:
        if sqdb.connection:
            sqdb.connection.close()
            lg.info("Database connection closed.")


if __name__ == "__main__":
    run_simulation()
