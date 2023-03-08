import random


class Board:

    def __init__(self, side_size, board=None, shuffle=True, rand_moves=0):
        """
        :param side_size: side size of the board
        :param board: puzzle board
        :param shuffle: when generating a board, it shuffles the numbers
        :param rand_moves: make n random moves on the board
        """
        self.__side_size = side_size
        self.__board = self.gen_board(shuffle) if board is None else board
        self.make_n_moves(rand_moves)
        self.__zero_idx = self.find_zero()
        self.__h_value = self.calculate_h()

    def get_board(self):
        return self.__board

    def get_h(self):
        return self.__h_value

    def get_size(self):
        return self.__side_size

    def gen_board(self, shuffle):
        """
        Generates a new board
        :param shuffle: randomize board status
        :return: [1, ..., n] (board status)
        """
        board = list(range(1, self.__side_size ** 2))
        if shuffle:
            random.shuffle(board)
        board.append(0)
        return board

    def find_zero(self):
        return self.__board.index(0)

    def is_solvable(self):
        """
        Checks if it is solvable
        :return: (bool)
        """
        is_odd = self.__side_size % 2 != 0
        inv_count_odd = self.count_inversions() % 2 != 0

        return not inv_count_odd if is_odd \
            else ((self.__side_size - (self.__zero_idx // self.__side_size)) % 2 == 0) == inv_count_odd

    def count_inversions(self):
        """
        Counts the number of inversions inside the array board
        :return: number of inversion (int)
        """
        inv_count = 0
        for i in range(self.__side_size**2 - 1):
            for j in range(i + 1, self.__side_size**2):
                inv_count += 1 if (self.__board[j] and self.__board[i] and self.__board[i] > self.__board[j]) else 0

        return inv_count

    def calculate_h(self):
        """
        Based on the board, calculates the evaluation function
        :return: h value (int)
        """
        indxs = list(range(self.__side_size ** 2))
        indxs.pop(self.__zero_idx)

        return sum([self.calculate_dist(i) for i in indxs])

    def calculate_dist(self, i):
        """
        Calculates distance from objective position for number with index i on the board
        :param i: index of number != 0 on the board
        :return: distance (int)
        """
        # Ideal position (x_obj, y_obj) for n
        x_obj = (self.__board[i] - 1) % self.__side_size
        y_obj = (self.__board[i] - 1) // self.__side_size

        return abs(x_obj - (i % self.__side_size)) + abs(y_obj - (i // self.__side_size))

    def get_available_moves(self):
        """
        Returns a list of available moves based on board status
        :return: [[3, 'U'], [1, 'R']]
        """
        # [UP, DOWN, LEFT, RIGHT]
        moves = [[-self.__side_size, 'U'], [self.__side_size, 'D'], [-1, 'L'], [1, 'R']]
        # Condition for each move
        conds = [
            not (self.__zero_idx // self.__side_size == 0),
            not (self.__zero_idx // self.__side_size == self.__side_size - 1),
            not (self.__zero_idx % self.__side_size == 0),
            not (self.__zero_idx % self.__side_size == self.__side_size - 1)
        ]
        return [m for (m, remove) in zip(moves, conds) if remove]

    def make_move(self, move):
        """
        Makes a move on the board
        :param move: move to make
        :return: new board status after the move
        """
        new_state = self.__board.copy()
        # Switch 0 and the number involved
        new_state[self.__zero_idx], new_state[self.__zero_idx + move[0]] = new_state[self.__zero_idx + move[0]], 0
        return new_state

    def make_n_moves(self, n_moves):
        """
        Makes n moves on the board
        :param n_moves: number of moves to make
        """
        for _ in range(n_moves):
            self.__zero_idx = self.find_zero()
            moves = self.get_available_moves()
            self.__board = self.make_move(moves[random.randrange(len(moves))])

    def goal_test(self):
        """
        Checks if the board is in an optimal position
        :return: bool (True if the state is optimal)
        """
        return self.__h_value == 0

    def equals(self, other):
        return self.__board == other.__board

    def print_state(self):
        for i in range(self.__side_size ** 2):
            print(self.__board[i], end=' ' if (i % self.__side_size != self.__side_size - 1) else '\n')
        print()
