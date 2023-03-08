from structures.queue import Queue
from structures.tree import Tree


class Simulator:
    def __init__(self, state, max_cost):
        """
        :param state: problem state
        :param max_cost: maximum cost of a solution
        """
        self.__tree = Tree(None, state, 0, [0, 'S'])
        self.__queue = Queue()
        self.__max_cost = max_cost

    def start(self):
        """
        Makes a simulation based on the state passed at initialization
        :return: Solution node (if found) and number of expanded nodes
        """
        if not self.__tree.is_solvable():
            return self.__tree, 0, False

        self.__queue.push(self.__tree)
        expanded_nodes, cost, node = 0, 0, None
        while cost < self.__max_cost:
            node = self.__queue.pop()
            if node is None or node.is_goal_state():
                break

            cost = node.get_cost()
            expanded_nodes += self.__queue.enqueue(node)
        return node, expanded_nodes, node is not None

    def reset(self, new_cost=0):
        """
        Reset the simulation
        :param new_cost: new maximum cost
        """
        self.__tree.reset()
        self.__queue.reset()
        self.__max_cost = new_cost if new_cost > 0 else self.__max_cost
