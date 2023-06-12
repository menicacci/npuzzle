from structures.queue import Queue
from structures.tree import Tree


class Simulator:
    def __init__(self, state, max_cost, multiple_sols=False):
        """
        :param state: problem state
        :param max_cost: maximum cost of a solution
        """
        self.__tree = Tree(None, state, 0, [0, 'S'])
        self.__queue = Queue()
        self.__max_cost = max_cost
        self.__mul_sols = multiple_sols

    def get_tree(self):
        return self.__tree

    def run(self):
        if not self.__tree.is_solvable():
            return [], 0, 0

        self.__queue.push(self.__tree)
        expanded_nodes, cost, node = 0, 0, None
        solutions = []
        while cost <= self.__max_cost:
            node = self.__queue.pop()

            if node.is_goal_state():
                solutions.append(node)
                if not self.__mul_sols:
                    break
                self.__max_cost = node.get_cost()

            cost = node.get_value()
            expanded_nodes += self.__queue.enqueue(node)
        return solutions, expanded_nodes, self.__max_cost
