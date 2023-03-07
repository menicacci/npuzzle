from functools import *
from games.board import *


@total_ordering
class Tree:
    def __init__(self, parent, state, cost, move=None):
        """
        :param parent: parent node
        :param state: state stored inside the node
        :param cost: cost associated
        :param move: move made from previous state (root-node: S)
        """
        self.__parent = parent
        self.__sons = []
        self.__state = state
        self.__cost = cost
        self.__h = state.get_h()
        self.__move = move

    def get_parent(self):
        return self.__parent

    def get_sons(self):
        return self.__sons

    def get_cost(self):
        return self.__cost

    def get_value(self):
        return self.__h + self.__cost

    def get_move(self):
        return self.__move

    def get_state(self):
        return self.__state

    def is_goal_state(self):
        return self.get_state().goal_test()

    def add_son(self, state, move):
        son = Tree(self, state, self.get_cost() + 1, move)
        self.__sons.append(son)
        return son

    def generate_sons(self):
        sons = []
        moves = self.get_state().get_available_moves()
        for m in moves:
            # Checks if opposite move has been made from the parent
            # Prevents sequence of moves like 'R' -> 'L'
            if (self.get_move()[0] + m[0]) != 0:
                s = self.get_state().make_move(m)
                sons.append(self.add_son(Board(self.__state.get_size(), s), m))
        return sons

    def get_path(self):
        node, path = self, []
        while node is not None:
            path.append(node)
            node = node.__parent
        return path

    def print_path(self):
        path = self.get_path()
        while path:
            n = path.pop()
            print(n.get_move()[1] + '\n' if n.get_move() is not None else '',)
            n.get_state().print_state()
        print('\nCost:', n.get_cost(), '\n')

    def get_data(self):
        path = self.get_path()
        path.reverse()

        lp = len(path)
        data = [[path[i].get_state().get_board(), path[i + 1].get_move()[0] if i < lp - 1 else 0] for i in range(lp)]
        return data

    def reset(self):
        self.__sons = []

    def __lt__(self, other):
        return self.get_value() < other.get_value()
