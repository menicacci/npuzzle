from data.data import *

if __name__ == "__main__":
    puzzle_size = 3
    n_puzzle = 100
    max_cost = 40
    random_data = True
    mul_factor = 3

    file_name = 'data_' + str(puzzle_size) + '.txt'

    p_s, e_n = generate_data(puzzle_size, n_puzzle, max_cost, file_name)
