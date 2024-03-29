from typing import Dict


class Vertex:
    def __init__(self, parent_char_: str | int, parent_: 'Vertex'):
        self.to: Dict[str | int, 'Vertex'] = {}
        self.go: Dict[str | int, 'Vertex'] = {}
        self.link: 'Vertex' = None
        self.parent: 'Vertex' = parent_
        self.parent_char: str | int = parent_char_
        self.terminal: bool = False
        self.ids: list[int] = []


class Aho_Korasik:
    def __init__(self):
        self.root = Vertex(-1, None)

    def link(self, v: Vertex):
        if v.link is None:
            if v == self.root or v.parent == self.root:
                v.link = self.root
            else:
                v.link = self.go(
                    self.link(v.parent),
                    v.parent_char
                )
        return v.link

    def go(self, v: Vertex, char: str):
        if char not in v.go:
            if char in v.to:
                v.go[char] = v.to[char]
            elif v == self.root:
                v.go[char] = self.root
            else:
                v.go[char] = self.go(
                    self.link(v),
                    char
                )
        return v.go[char]

    def add(self, string: str, id: int):
        v = self.root
        for c in string:
            if c not in v.to:
                v.to[c] = Vertex(c, v)
            v = v.to[c]
        v.terminal = True
        v.ids.append(id)

    def find(self, text: str):
        res = []
        v = self.root
        for i, c in enumerate(text):
            v = self.go(v, c)
            if v.terminal:
                print(f'Entry at {i} of {v.ids}')
                res.append([i, v.ids])
        return res


if __name__ == '__main__':
    test = Aho_Korasik()
    dictionary = {
        1: 'at',
        4: 'cat',
        2: 'bat',
        3: 'mad',
    }
    for i in dictionary:
        test.add(dictionary[i], i)
    string = """A quick brown cat had a baseball bat, all his friend thought he's gone mad!"""
    result = test.find(string)
    for pos, ids in result:
        print(string[:pos+1])
        print(pos, string[pos], *[dictionary[i] for i in ids])

