import random
import pandas as pd

random.seed(42)  # For reproducibility


class BingoBoard:
    size: int
    board: dict[int, dict[int, int]]
    number_pool: list[int]

    def __init__(self, size=7, number_pool_size: int = 200):
        self.size = size
        self.number_pool = list(range(1, number_pool_size + 1))
        self.matrix = self.create_board_matrix()

    def create_board_matrix(self):
        output_board = {}
        for r_idx in range(self.size):
            row_dict = {}
            for c_idx in range(self.size):
                number = random.choice(self.number_pool)
                row_dict[c_idx] = number
                self.number_pool.remove(number)
            output_board[r_idx] = row_dict
        return output_board

    def print_board(self) -> str:
        df = self.to_dataframe()
        return df.to_string()

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.matrix).T


class BingoGame:
    winning_numbers: list[int] = []

    def __init__(self, size=7, number_pool_size: int = 200):
        self.size = size
        self.number_pool_size = number_pool_size

    def generate_board(self) -> BingoBoard:
        return BingoBoard(size=self.size, number_pool_size=self.number_pool_size)

    def generate_winning_numbers(self, count: int = 50) -> list[int]:
        self.winning_numbers = random.sample(range(1, self.number_pool_size + 1), count)
        return self.winning_numbers

    def validate_board(self, board: BingoBoard) -> bool:
        matrix = board.matrix

        r_ptr, c_ptr = 0, 0
        loop_breaker = False
        first_winning_set_count = 0
        while r_ptr < self.size and c_ptr < self.size:
            v = matrix[r_ptr][c_ptr]
            # print(f"{v=}")
            if v in self.winning_numbers:
                matrix[r_ptr][c_ptr] = "W"
                first_winning_set_count = 1
                # Check left of the current position (row-wise)
                for ptr_left in range(0, c_ptr):
                    # print(
                    #     f"matrix[{r_ptr}][{ptr_left}]={matrix[r_ptr][ptr_left]}, {matrix[r_ptr][ptr_left] in self.winning_numbers}"
                    # )
                    if matrix[r_ptr][ptr_left] in self.winning_numbers:
                        matrix[r_ptr][ptr_left] = "W"
                        first_winning_set_count += 1
                    else:
                        loop_breaker = True
                        break
                # Check right of the current position (row-wise)
                for ptr_right in range(c_ptr + 1, self.size):
                    if matrix[r_ptr][ptr_right] in self.winning_numbers:
                        matrix[r_ptr][ptr_right] = "W"
                        first_winning_set_count += 1
                    else:
                        loop_breaker = True
                        break

                # Check up of the current position (column-wise)
                for ptr_up in range(0, r_ptr):
                    # print(
                    #     f"matrix[{ptr_up}][{c_ptr}]={matrix[ptr_up][c_ptr]}, {matrix[ptr_up][c_ptr] in self.winning_numbers}"
                    # )
                    if matrix[ptr_up][c_ptr] in self.winning_numbers:
                        matrix[ptr_up][c_ptr] = "W"
                        first_winning_set_count += 1
                    else:
                        loop_breaker = True
                        break
                # Check down of the current position (column-wise)
                for ptr_down in range(r_ptr + 1, self.size):
                    # print(
                    #     f"matrix[{ptr_down}][{c_ptr}]={matrix[ptr_down][c_ptr]}, {matrix[ptr_down][c_ptr] in self.winning_numbers}"
                    # )
                    if matrix[ptr_down][c_ptr] in self.winning_numbers:
                        matrix[ptr_down][c_ptr] = "W"
                        first_winning_set_count += 1
                    else:
                        loop_breaker = True
                        break

            if loop_breaker:
                break

            r_ptr += 1
            c_ptr += 1
            # break
            # if matrix[r_ptr][c_ptr] in self.winning_numbers:
            #     matrix[r_ptr][c_ptr] = "W"
            #     r_ptr += 1
            #     c_ptr += 1
            # else:
            #     break
            # return False

        df = pd.DataFrame(matrix).T
        print(f"Validated board:\n{df.to_string()}")
        print(f"{first_winning_set_count=}")
        return True


def main():
    game = BingoGame(size=7, number_pool_size=200)
    board = game.generate_board()
    # game.generate_winning_numbers(100)
    # game.winning_numbers = [197, 28, 182, 24, 38, 147, 161]
    # game.winning_numbers = [164, 29, 65]
    # game.winning_numbers = [156, 126, 35, 120, 116, 93, 17]
    game.winning_numbers = [197, 29, 10, 8, 133, 91, 35, 164]
    print(f"{board.print_board()}")

    print(f"Winning numbers: {game.winning_numbers}")

    print(f"{game.validate_board(board)}")


if __name__ == "__main__":
    main()
