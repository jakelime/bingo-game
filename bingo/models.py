import dataclasses


@dataclasses.dataclass
class GameData:
    board_size: int
    number_pool_size: int
    num_boards: int
    winning_number_size: int
    winning_boards_count: int
