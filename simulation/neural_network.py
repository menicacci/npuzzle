import numpy as np
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout
import time
import random
from simulation.data import get_data_for_nn, reshape_for_nn, convert_prediction

np.random.seed(1)

class Intelligence:

    def __init__(self, side_size, load=False, model_it=0):
        self.side_size = side_size
        if not load:
            self.model = Sequential()
            self.model.add(Dense(units=2 * (side_size ** 4),
                                 input_dim=(side_size ** 4),
                                 activation='relu'))
            self.model.add(Dropout(0.1))
            self.model.add(Dense(units=4 * (side_size ** 4),
                                 activation='relu'))
            self.model.add(Dropout(0.1))
            self.model.add(Dense(units=2 * (side_size ** 4),
                                 activation='relu'))
            self.model.add(Dense(units=4,
                                 activation='relu'))
            self.model.compile(optimizer='adam',
                               loss='mse')
        else:
            self.model = load_model('models/nn-{}/nn-{}-{}.h5'.format(side_size, side_size, model_it))

    def train(self, splits):
        x_all, y_all = get_data_for_nn(self.side_size)
        x_groups = [[] for _ in range(splits)]
        y_groups = [[] for _ in range(splits)]

        # Randomize dataset
        for i in range(len(x_all)):
            pos = random.randint(0, splits - 1)
            x_groups[pos].append(x_all[i])
            y_groups[pos].append(y_all[i])

        x_train, y_train = [], []

        for i in range(splits):
            t0 = time.time()

            for x in x_groups[i]:
                x_train.append(reshape_for_nn(x, self.side_size))
            for y in y_groups[i]:
                y_train.append(y)

            self.model.fit(np.array(x_train), np.array(y_train), epochs=30)
            if (i+1) % 5 == 0:
                self.model.save("models/nn-{}/nn-{}-{}.h5".format(self.side_size, self.side_size, (i+1)))

            print("\n-> {} iterations completed out of {}".format((i+1), splits))
            print("Iteration time:", time.time() - t0)

    def predict(self, board):
        return self.model.predict(
            reshape_for_nn(
                state=board.get_board(),
                side_size=board.get_size()
            ).reshape((1, self.side_size**4))
        )

    def solve(self, board, max_cost=200):
        """
        Solves a board (only if solvable) with a maximum moves limit
        :param board: Board object
        :param max_cost: Maximum cost limit
        :return: Solution cost (int), move sequence (array)
        """
        board.print_state()
        if not board.is_solvable():
            print('Board unsolvable')
            return -1, None

        cost, move_seq = 0, []
        last_move = 0
        while not board.goal_test() and cost < max_cost:
            # Legal moves
            available_moves = board.get_available_moves()
            # Moves predicted from NN
            nn_pred = convert_prediction(self.predict(board)[0], self.side_size)
            # Moves predicted from NN filtered
            nn_moves = list(filter(lambda av_move: av_move[0] in nn_pred, available_moves))

            move_to_make = None
            for m in nn_moves:
                # Check for cycles
                if m[0] + last_move != 0:
                    move_to_make = m
                    break
                else:
                    available_moves.remove(m)
            # Move from NN rejected
            if move_to_make is None:
                move_to_make = random.choice(available_moves)
            # Make move chosen
            board = board.make_new(move_to_make)
            # Updates
            cost += 1
            last_move = move_to_make[0]
            move_seq.append(move_to_make)
        return cost, move_seq if cost != max_cost else []
