from games.board import *
from simulation.simulator import *
import pandas as pd
import numpy as np


def make_simulation(puzzle_size=3, max_cost=25, random_data=False, mul_factor=3, multiple_sols=False):
    board = Board(
        side_size=puzzle_size,
        board=None,
        shuffle=random_data,
        rand_moves=max_cost*mul_factor
    )
    board.print_state()

    return Simulator(board, max_cost, multiple_sols).run(), board

def generate_data(puzzle_size=3,
                  n_puzzle=300,
                  max_cost=25,
                  random_data=True,
                  mul_factor=3,
                  save=True,
                  multiple_sols=False
                  ):
    """
    Generate and write simulation into a file
    Data: state: [(int), ..., (int)], move: [(int), (int)]
    :param puzzle_size: size of the puzzle
    :param n_puzzle: # of puzzle that are generated
    :param max_cost: maximum cost of a simulation
    :param random_data: generate simulation randomly from scratch
    :param mul_factor: param for non-completely random simulation
    :param save: saves data generated
    :param multiple_sols: looks for multiple solution to a board (with same cost)
    :return: stats about the process
    """
    # Data to write
    data = []
    # Expanded nodes
    exp_nodes = 0
    # Cost array
    costs = []
    # Number of puzzle tried and solved
    puzzle_solved, puzzle_tried = 0, 0

    while puzzle_solved < n_puzzle:
        sim_results, board = make_simulation(puzzle_size, max_cost, random_data, mul_factor, multiple_sols)
        exp_nodes += sim_results[1]
        puzzle_tried += 1

        if puzzle_tried % 10 == 0:
            print('Puzzle solved at stage {}: {}'.format(puzzle_tried, puzzle_solved))

        for node in sim_results[0]:
            moves = node.get_moves_data()
            data.append([board.get_board(), moves])

        if sim_results[0]:
            puzzle_solved += 1
            costs.append(sim_results[2])

    print('Puzzle solved: {}\tPuzzle solved/Tot.: {}%'.format(puzzle_solved, (puzzle_solved/puzzle_tried)*100))
    print('# of expanded nodes during the simulation: {}'.format(exp_nodes), end='\n\n')

    if save:
        f = pd.DataFrame(data, columns=['Board', 'Moves'])
        f_name = 'data/data_' + str(puzzle_size)
        f.to_csv(f_name, index=False)
        return puzzle_solved, exp_nodes, costs
    else:
        return data

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
        DOWN  -> [0, 1, 0, 0]
        LEFT  -> [0, 0, 1, 0]
        RIGHT -> [0, 0, 0, 1]
        FINAL -> [0, 0, 0, 0]
    """
    return [
        1 if move < -1 else 0,
        1 if move > 1 else 0,
        1 if move == -1 else 0,
        1 if move == 1 else 0
    ]

def get_data_for_nn(side_size):
    x, y = [], []

    data = read_data(side_size)

    for d in data:
        state, moves = d[0], d[1]
        for move in moves:
            x.append(state)
            y.append(convert_move_for_nn(move))

            state = Board(side_size, state).make_move([move])

    print('Dataset size: ', len(x))
    return x, y

def refactor_array(v):
    return [int(n) for n in v.translate(str.maketrans("", "", "[],\n")).split(' ')]

def reshape_for_nn(state, side_size):
    output = []
    for i in range(side_size**2):
        one_hot = np.zeros(side_size**2)
        one_hot[state[i] - 1] = 1

        output.append(one_hot)
    return np.array(output).flatten().reshape(side_size**4)

def convert_prediction(prediction, side_size):
    output = []
    max_index = np.argmax(prediction)
    while prediction[max_index] != 0:
        sign = -1 if max_index % 2 == 0 else 1
        output.append(sign if max_index > 1 else sign*side_size)
        prediction[max_index] = 0
        max_index = np.argmax(prediction)

    return output
