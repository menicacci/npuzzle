from simulation.data import *

if __name__ == "__main__":

    puzzle_size = 3

    n_solv_p, exp_nodes, costs, n_sols = generate_data(
        puzzle_size=puzzle_size,
        n_puzzle=10,
        max_cost=35,
        random_data=False,
        mul_factor=3
    )

    for d in get_data_for_nn(puzzle_size):
        print(d)

    '''
    b = Board(3, [3, 2, 1, 7, 5, 6, 0, 4, 8])
    s = Simulator(b, 150, True)

    sols, e_n, c = s.run()

    r_t = s.get_tree().get_resolution_tree(sols)

    for m in [sol.get_moves_data() for sol in sols]:
        print(m)
    print('\n\n')

    g = r_t.get_graph()

    for l in g:
        print('Level: ', g.index(l))
        for n in l:
            print('Board: ', n[1].get_board(), 'Seq ID: ', n[0], 'Moves: ', n[2])     
    '''