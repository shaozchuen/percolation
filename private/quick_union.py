import pdb

"""
with improvements
"""

class QuickUnion(object):

    def __init__(self, n):
        self.n = n
        self._id = [ i for i in range(0, n) ]
        self.size = [ 1 for i in range(0, n) ]

    def union(self, p, q):
        i = root(p)
        j = root(q)
        if i == j:
            return
        # point the root of the smaller tree to the root of the larger one
        # the update the size of the larger tree, increased by the size of the smaller one
        if self.size[i] < self.size[j]:
            self._id[i] = j
            self.size[j] += self.size[i]
        else:
            self._id[j] = i
            self.size[i] += self.size[j]

    def root(self, i):
        while i != self._id[i]:
            self._id[i] = self._id[self._id[i]]
            i = self._id[i]
        return i

    def connected(self, p, q):
        return root(p) == root(q)


if __name__ == "__main__":
    app = QuickUnion(10)
    print(app._id)
    print(app.size)
    pdb.set_trace()
