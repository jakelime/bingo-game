import sqlite3
from pathlib import Path
from typing import Optional

from bingo import APP_NAME
from bingo.custom_logger import getLogger
from bingo.models import GameData

lg = getLogger(APP_NAME)


DATABASE_NAME = "bingo_simulations.db"
DBPATH = Path.cwd() / "output_data" / DATABASE_NAME
if not DBPATH.parent.exists():
    DBPATH.parent.mkdir(parents=True, exist_ok=True)
    lg.info(f"Created directory for database: {DBPATH.parent}")
DBPATH_STR = str(DBPATH.absolute())


class SQLiteDatabase:
    """
    A class to handle SQLite database operations for Bingo game simulations.
    """

    def __init__(self, dbpath: str = DBPATH_STR):
        self.dbpath = dbpath
        self.connection = self.get_db_connection()

    def get_db_connection(self) -> Optional[sqlite3.Connection]:
        """
        Establishes a connection to the SQLite database and creates the table if it doesn't exist.
        """
        conn = None
        try:
            conn = sqlite3.connect(self.dbpath)
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS simulations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    board_size INTEGER,
                    number_pool_size INTEGER,
                    num_boards INTEGER,
                    winning_number_size INTEGER,
                    winning_boards_count INTEGER,
                    timestamp_entry DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """
            )
            conn.commit()
            lg.info(f"Connected to database: {DATABASE_NAME}")
            return conn
        except sqlite3.Error as e:
            lg.error(f"Database connection error: {e}")
            if conn:
                conn.close()
            return None

    def insert_game_data(self, data: GameData):
        """
        Inserts a single GameData record into the simulations table.
        """
        conn = self.connection
        if not conn:
            raise RuntimeError(
                "db connection is not established. Please call get_db_connection() first."
            )

        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO simulations (board_size, number_pool_size, num_boards, winning_number_size, winning_boards_count)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    data.board_size,
                    data.number_pool_size,
                    data.num_boards,
                    data.winning_number_size,
                    data.winning_boards_count,
                ),
            )
            conn.commit()
            lg.info(f"Inserted data into DB: {data.winning_boards_count} winners")
        except sqlite3.Error as e:
            lg.error(f"Error inserting data: {e}")
