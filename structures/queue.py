from heapq import *


class Queue:
    def __init__(self):
        self.__queue = []

    def push(self, e):
        self.__queue.append(e)

    def pop(self):
        return heappop(self.__queue) if not self.is_empty() else None

    def enqueue(self, node):
        new_nodes = node.generate_sons()
        for n in new_nodes:
            heappush(self.__queue, n)
        return len(new_nodes)

    def reset(self):
        self.__queue = []

    def is_empty(self):
        return not bool(self.__queue)
