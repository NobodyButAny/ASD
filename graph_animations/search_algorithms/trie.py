from dataclasses import dataclass
from typing import Dict


class Vertex:
    def __init__(self):
        self.to: Dict[int | str, 'Vertex'] = {}
        self.terminal: bool = False


class Trie:
    def __init__(self):
        self.root = Vertex()

    def add(self, string: str):
        v = self.root
        for char in string:
            if char not in v.to:
                v.to[char] = Vertex()
            v = v.to[char]
        v.terminal = True

    def find(self, string: str):
        v = self.root
        for char in string:
            if char not in v.to:
                return False
            v = v.to[char]
        return v.terminal

    def delete(self, string: str):
        v = self.root
        for char in string:
            if char not in v.to:
                return
            v = v.to[char]
        v.terminal = False


if __name__ == "__main__":
    test = Trie()
    test.add('cat')
    test.add('cod')
    test.add('dad')
    print(
        test.find('cat'),
        test.find('add'),
        test.find('dad'),
        test.find('cod')
    )
    test.delete('cat')
    print(
        test.find('cat'),
        test.find('add'),
        test.find('dad'),
        test.find('cod')
    )
