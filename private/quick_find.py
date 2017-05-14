import pdb

class QuickFind(object):

    def __init__(self, n):
        self.n = n
        self._id = [ i for i in range(0, n) ]

    def union(self, p, q):
        pid = self._id[p]
        qid = self._id[q]
        for i in range(0, self.n):
            if self._id[i] == pid:
                self._id[i] = qid

    def connected(self, p, q):
        return self._id[p] == self._id[q]

if __name__ == "__main__":
    app = QuickFind(10)
    print(app._id)
    pdb.set_trace()


