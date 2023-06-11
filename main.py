from games.board import Board
from simulation.neural_network import Intelligence
from simulation.simulator import Simulator
from simulation.data import generate_data, read_data


if __name__ == "__main__":
    b = Board(4, [5, 1, 2, 3,
                  9, 6, 7, 4,
                  13, 10, 11, 8,
                  14, 15, 12, 0])

    nn = Intelligence(4, True, 20)
    nn_c, _ = nn.solve(b)
    print('NN cost: ', nn_c)

    s = Simulator(b, 40, False)
    _, _, sim_c = s.run()
    print('Simulation cost: ', sim_c)

    '''
    # For generating new data
    n_solv_p, exp_nodes, costs = generate_data(
        puzzle_size=6,
        n_puzzle=100,
        max_cost=45,
        random_data=False,
        mul_factor=4,
        save=True
    )
    '''
