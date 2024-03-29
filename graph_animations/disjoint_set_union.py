class DisjointSetUnion:
    def __init__(self):
        self.rep = {}
        self.size = {}

    def add(self, element, rep=None):
        if rep is None:
            self.rep[element] = element
            self.size[element] = 1
        elif rep in self.rep:
            self.add(element)
            self.unite(element, rep)
        else:
            raise ValueError("add: Representative should be included in DSU!")
        return self

    def add_joint_set(self, elements):
        for elem in elements:
            self.rep[elem] = elements[0]
            self.size[elem] = 1
        self.size[elements[0]] = len(elements)
        return self

    def add_disjoint_set(self, elements):
        for elem in elements:
            self.rep[elem] = elem
            self.size[elem] = 1
        return self

    def leader(self, elem):
        if self.rep[elem] == elem:
            return elem
        else:
            self.rep[elem] = self.leader(self.rep[elem])
            return self.rep[elem]

    def unite(self, a, b):
        a_lead, b_lead = self.leader(a), self.leader(b)
        if self.size[a_lead] > self.size[b_lead]:
            a_lead, b_lead = b_lead, a_lead
        self.size[b_lead] += self.size[a_lead]
        self.rep[a_lead] = b_lead
        return self


if __name__ == "__main__":
    test = DisjointSetUnion()
    for i in range(0, 6):
        test.add(i)
    test.unite(2, 3)
    test.add_joint_set(range(10, 14))
    for i in test.rep:
        print(f"{i}: {test.leader(i)}, size: {test.size[i]}")
    print('')
    test.unite(2, 10)
    for i in test.rep:
        print(f"{i}: {test.leader(i)}, size: {test.size[i]}")
