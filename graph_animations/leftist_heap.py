from dataclasses import dataclass
from typing import Any, Generic


@dataclass
class Node:
    key: Any
    value: Any
    left: 'Node' = None
    right: 'Node' = None
    distance: int = 0

    @staticmethod
    def dist(node: 'Node'):
        if node is None:
            return -1
        return node.distance


class LeftistHeap:
    def __init__(self):
        self.head = None

    @staticmethod
    def merge(x: Node, y: Node):
        if x is None:
            return y
        if y is None:
            return x
        if y.key < x.key:
            x, y = y, x
        x.right = LeftistHeap.merge(x.right, y)
        if Node.dist(x.right) > Node.dist(x.left):
            x.left, x.right = x.right, x.left
        x.distance = Node.dist(x.right) + 1
        return x

    def is_empty(self):
        return self.head is None

    def insert(self, pair: Any | tuple[Any, Any]):
        if isinstance(pair, tuple):
            new = Node(pair[0], pair[1])
        else:
            new = Node(pair, pair)
        if self.head is None:
            self.head = new
        else:
            self.head = LeftistHeap.merge(self.head, new)

    def min(self):
        return self.head.key

    def pop_min(self):
        res = self.min()
        self.head = LeftistHeap.merge(self.head.left, self.head.right)
        return res


if __name__ == "__main__":
    test = LeftistHeap()
    for i in range(10):
        test.insert([i, i])
    while test.head is not None:
        print(test.pop_min())
