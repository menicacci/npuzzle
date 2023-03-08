from games.board import *
from data.simulator import *


def generate_data(puzzle_size=3, n_puzzle=300, max_cost=25, file_name='data_3.txt', random_data=True, mul_factor=3):
    f = open(file_name, "a")

    stage = 1
    # Number of puzzle solved
    n_solv_p = 0
    # Number of puzzle with a cost > max_cost
    n_max_p = 0
    exp_nodes = 0
    dataset_size = 0
    for _ in range(n_puzzle):
        print('Stage:', stage, 'of:', n_puzzle)

        board = Board(
            side_size=puzzle_size,
            board=None,
            shuffle=random_data,
            rand_moves=0 if random_data else max_cost*mul_factor
        )
        board.print_state()

        s = Simulator(board, max_cost)
        node, e_nodes, is_solved = s.start()
        if node is not None:
            n_solv_p += 1 if is_solved else 0
            dataset_size += node.get_cost() + 1

            for d in node.get_data():
                line = str(d[0]) + '\n' + str(convert_for_nn(d[1])) + '\n'
                f.writelines(line)
        else:
            n_max_p += 1
        exp_nodes += e_nodes
        stage += 1

    f.close()

    print('Puzzle solved: ', n_solv_p, '\tPuzzle solved/Tot.: ', (n_solv_p / n_puzzle)*100, '%')
    # Number of unsolved puzzles
    n_unsolv_p = n_puzzle - n_solv_p - n_max_p
    print('Puzzle unsolvable: ', n_unsolv_p, '\tPuzzle unsolved/Tot.: ', (n_unsolv_p / n_puzzle)*100, '%')
    print('Puzzle over maximum cost: ', n_max_p, '\tPuzzle over max cost/Tot.: ', (n_max_p / n_puzzle)*100, '%')

    print('# of expanded nodes during the simulation: ', exp_nodes)
    print('Dataset size: ', dataset_size)

    return n_solv_p, exp_nodes


def read_data(file_name='data.txt'):
    f = open(file_name, "r")
    lines = f.readlines()
    f.close()

    data = []
    for i in range(0, len(lines), 2):
        board_l, move_l = lines[i], lines[i + 1]
        data.append([refactor(board_l), refactor(move_l)])
    return data


def convert_for_nn(move):
    return [move if abs(move) == 1 else 0, move // abs(move) if abs(move) > 1 else 0]


def convert_for_simulation(move, puzzle_size):
    return move[0] + move[1]*puzzle_size


def refactor(v):
    v = v.replace('[', '')
    v = v.replace(']', '')
    v = v.replace(',', '')
    v = v.replace('\n', '')
    v = v.split(' ')
    return [int(x) for x in v]

