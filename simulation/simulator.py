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
        solutions, sol_found, sol_cost = [], False, 0
        while cost < self.__max_cost:
            node = self.__queue.pop()
            if node is None or node.is_goal_state():
                if sol_found and node.get_cost() != sol_cost:
                    break
                else:
                    sol_found, sol_cost = True, node.get_cost()
                    solutions.append(node)
                    if not self.__mul_sols:
                        break

            cost = node.get_cost()
            expanded_nodes += self.__queue.enqueue(node)
        return solutions, expanded_nodes, sol_cost
