from games.board import *
from simulation.simulator import *
import pandas as pd


def generate_data(puzzle_size=3, n_puzzle=300, max_cost=25, random_data=True, mul_factor=3):
    """
    Generate and write simulation into a file
    Data: state: [(int), ..., (int)], move: [(int), (int)]
    :param puzzle_size: size of the puzzle
    :param n_puzzle: # of puzzle that are generated
    :param max_cost: maximum cost of a simulation
    :param random_data: generate simulation randomly from scratch
    :param mul_factor: param for non-completely random simulation
    :return: stats about the process
    """
    # Data to write
    data = []
    # Expanded nodes
    exp_nodes = 0
    # Cost array
    costs = []
    # N. of solutions per puzzle
    n_sols = []
    # Number of puzzle solved
    n_solv_p = 0

    for i in range(n_puzzle):
        print('Stage:', (i + 1), 'of:', n_puzzle)

        board = Board(
            side_size=puzzle_size,
            board=None,
            shuffle=random_data,
            rand_moves=0 if random_data else max_cost*mul_factor
        )
        board.print_state()

        s = Simulator(board, max_cost)
        sols, e_nodes, c = s.run()

        for node in sols:
            moves = node.get_moves_data()
            data.append([board.get_board(), moves])

        if bool(sols):
            n_solv_p += 1
            n_sols.append(len(sols))
            costs.append(len(moves))

        exp_nodes += e_nodes

    f = pd.DataFrame(data, columns=['Board', 'Moves'])
    f_name = 'data/data_' + str(puzzle_size)
    f.to_csv(f_name, index=False)

    print('Puzzle solved: ', n_solv_p, '\tPuzzle solved/Tot.: ', (n_solv_p / n_puzzle)*100, '%')
    print('Puzzle unsolved: ', (n_puzzle - n_solv_p), '\tPuzzle unsolved/Tot.: ', ((n_puzzle - n_solv_p) / n_puzzle)*100, '%')
    print('# of expanded nodes during the simulation: ', exp_nodes)
    print()

    return n_solv_p, exp_nodes, costs, n_sols

def read_data(side_size: int):
    """
    Read simulation data from a file
    :param side_size: dimension of board
    :return: simulation attributes contained inside the file
    """
    f_name = 'data/data_' + str(side_size)
    return [[refactor_array(d[0]), refactor_array(d[1])] for d in pd.read_csv(f_name).values.tolist()]

def convert_move_for_nn(move):
    """"
    Converts move format from simulation for a neural network
    :param move: move to convert
    :return: move converted
    Moves format:
        UP    -> [1, 0, 0, 0]
        DOWN  -> [1, 0, 0, 0]
        LEFT  -> [1, 0, 0, 0]
        RIGHT -> [1, 0, 0, 0]
        FINAL -> [0, 0, 0, 0]
    """
    return [
        1 if move < -1 else 0,
        1 if move > 1 else 0,
        1 if move == -1 else 0,
        1 if move == 1 else 0
    ]

def get_data_for_nn(side_size: int):
    data_nn = []
    for d in read_data(side_size):
        state, moves = d[0], d[1]
        sequence = []
        for move in moves:
            sequence.append([state, convert_move_for_nn(move)])
            state = Board(side_size, state).make_move([move])
        data_nn.append(sequence.copy())
    return data_nn

def refactor_array(v):
    v = v.replace('[', '')
    v = v.replace(']', '')
    v = v.replace(',', '')
    v = v.replace('\n', '')
    v = v.split(' ')
    return [int(x) for x in v]
