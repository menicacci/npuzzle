class Graph:

    def __init__(self, node=None):
        self.__vertex = node

    def get_vertex(self):
        return self.__vertex

    def create_graph(self):
        self.__vertex = Node(1)

    def print_graph(self):
        self.get_vertex().print_node()


class Node:

    def __init__(self, data):
        self.__data = data
        self.__nodes_to = []
        self.__moves_to = []

    def get_data(self):
        return self.__data

    def get_nodes_to(self):
        return self.__nodes_to

    def get_moves_to(self):
        return self.__moves_to

    def add_connection_to(self, value, move):
        new_node = Node(value)
        self.__nodes_to.append(new_node)
        self.__moves_to.append(move)
        return new_node

    def print_node(self, level=0):
        print('\t' * level, 'State: ', self.get_data())

        for i in range(len(self.get_moves_to())):
            print('\t' * level, 'Move: ', self.get_moves_to()[i])
            self.get_nodes_to()[i].print_node(level + 1)
