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

    def is_solvable(self):
        return self.__state.is_solvable()

    def add_son(self, state, move):
        son = Tree(self, state, self.get_cost() + 1, move)
        self.__sons.append(son)
        return son

    def height(self, h=0):
        son_max_h = h
        for son in self.get_sons():
            s_h = son.height(h + 1)
            if s_h > son_max_h:
                son_max_h = s_h
        return son_max_h

    def get_son(self, state):
        for son in self.get_sons():
            if son.get_state().equals(state):
                return son
            return None

    def exist(self, state):
        return self.get_son(state) is not None

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

        l_p = len(path)
        data = [[path[i].get_state().get_board(), path[i + 1].get_move()[0] if i < l_p - 1 else 0] for i in range(l_p)]
        return data

    def get_moves_data(self):
        return [d[1] for d in self.get_data()]

    def reset(self, state):
        self.__sons = []
        self.__state = state

    def __lt__(self, other):
        return self.get_value() < other.get_value()

    def print_tree(self, tab_count=0):
        print('\t'*tab_count, self.get_state().get_board(), self.get_move())
        tab_count += 1
        for son in self.get_sons():
            son.print_tree(tab_count)

    #
    # Functions for visualizing puzzle with multiple solutions
    #

    def get_resolution_tree(self, solutions):
        solution_paths = [sol.get_path() for sol in solutions]
        solution_tree = Tree(None, self.get_state(), 0, [0, 'S'])

        for sol_path in solution_paths:
            sol_path.reverse()
            sol_path.pop(0)
            solution_tree.insert_in_sequence(sol_path)
        return solution_tree

    def insert_in_sequence(self, sol_path):
        if bool(sol_path):
            state, move = sol_path[0].get_state(), sol_path[0].get_move()
            sol_path.pop(0)

            new_son = self.add_son(state, move) if not self.exist(state) else self.get_son(state)
            new_son.insert_in_sequence(sol_path)

    def get_graph(self):
        g = [[] for _ in range(self.height() + 1)]
        self.calculate_graph(g, 0, [1])

        return g

    # TODO: Refactor
    def calculate_graph(self, g, h, seq_id):
        node = None
        if bool(g[h]):
            for n in g[h]:
                if self.get_state().equals(n[1]):
                    node = n
                    break
        if node is None:
            g[h].append([[seq_id.copy()], self.get_state(), [self.get_move()]])
        else:
            node[0].append(seq_id.copy())
            node[2].append(self.get_move())

        if len(self.get_sons()) == 1:
            self.get_sons()[0].calculate_graph(g, h+1, seq_id.copy())
        else:
            i = 1
            for son in self.get_sons():
                s = seq_id.copy()
                s.append(i)
                son.calculate_graph(g, h+1, s.copy())
                i += 1
