
import pdb
import random
import numpy as np

class Percolation(object):

    def __init__(self, n):
        self.n = n
        self.percolation_site = self.PercolationMatrix(n)

    class PercolationMatrix(object):

        def __init__(self, n):

            self.site_matrix = self.build_site_matrix(n)
            self.open_matrix = self.build_open_matrix(n)
            self.size = [ 1 for i in range(0, n**2 + 2) ]

            self.left_side = [ (i*n) + 1 for i in range(0, n) ]
            self.top_side = [ i+1 for i in range(0, n) ]
            self.right_side = [ (i+1) * n for i in range(0, n) ]
            self.bottom_side = [ n**2 - (i) for i in range(0, n) ]

            self.virtual_top = 0
            self.virtual_bottom = n**2 + 1

        def build_site_matrix(self, n):
            return [ i for i in range(0, n**2 + 2) ]

        def build_open_matrix(self, n):
            open_matrix = [ False for i in range(0, n**2) ]
            open_matrix.insert(0, True)
            open_matrix.insert(n**2+1, True)
            return open_matrix

        def union(self, p, q):
            i = self.root(p)
            j = self.root(q)
            if i == j:
                return
            # point the root of the smaller tree to the root of the larger one
            # the update the size of the larger tree, increased by the size of the smaller one
            if self.size[i] < self.size[j]:
                self.site_matrix[i] = j
                self.size[j] += self.size[i]
            else:
                self.site_matrix[j] = i
                self.size[i] += self.size[j]

        def root(self, i):
            while i != self.site_matrix[i]:
                self.site_matrix[i] = self.site_matrix[self.site_matrix[i]]
                i = self.site_matrix[i]
            return i

        def connected(self, p, q):
            return self.root(p) == self.root(q)


    def open(self, coords):
        idx = coords[0]*self.n + coords[1] + 1
        self.percolation_site.open_matrix[idx] = True
        # top side treatment
        if idx in self.percolation_site.top_side:
            adjacents = [ self.percolation_site.virtual_top, idx+self.n ]
            # top left treatment
            if idx in self.percolation_site.left_side:
                adjacents = adjacents + [ idx+1 ]
                for adjacent in adjacents:
                    if self.is_open(adjacent):
                        self.percolation_site.union(idx, adjacent)
            # top right treatment
            elif idx in self.percolation_site.right_side:
                adjacents = adjacents + [ idx-1 ]
                for adjacent in adjacents:
                    if self.is_open(adjacent):
                        self.percolation_site.union(idx, adjacent)
            else:
                adjacents = adjacents + [ idx-1, idx+1 ]
                for adjacent in adjacents:
                    if self.is_open(adjacent):
                        self.percolation_site.union(idx, adjacent)
        # bottom side treatment
        elif idx in self.percolation_site.bottom_side:
            adjacents = [ self.percolation_site.virtual_bottom, idx-self.n ]
            # bottom left treatment
            if idx in self.percolation_site.left_side:
                adjacents = adjacents + [ idx+1 ]
                for adjacent in adjacents:
                    if self.is_open(adjacent):
                        self.percolation_site.union(idx, adjacent)
            # bottom right treatment
            elif idx in self.percolation_site.right_side:
                adjacents = adjacents + [ idx-1 ]
                for adjacent in adjacents:
                    if self.is_open(adjacent):
                        self.percolation_site.union(idx, adjacent)
            else:
                adjacents = adjacents + [ idx+1, idx-1 ]
                for adjacent in adjacents:
                    if self.is_open(adjacent):
                        self.percolation_site.union(idx, adjacent)
        # treatment for everything in between
        else:
            adjacents = [ idx+1, idx-1, idx+self.n, idx-self.n ]
            for adjacent in adjacents:
                if self.is_open(adjacent):
                    self.percolation_site.union(idx, adjacent)

    def is_open(self, idx):
        return self.percolation_site.open_matrix[idx]

    def is_full(self, row, col):
        idx = row*self.n + col + 1
        return self.percolation_site.connected(0, idx)

    def number_of_open_sites(self):
        return self.percolation_site.open_matrix.count(True) - 2

    def percolates(self):
        return self.percolation_site.connected(self.percolation_site.virtual_top, self.percolation_site.virtual_bottom)

class PercolationTest(object):

    def __init__(self, n, number_of_trials):
        self.n = n
        self.number_of_trials = number_of_trials
        pass

    def run_test(self):
        results = []
        for i in range(0, self.number_of_trials):
            print("Trial: {0}".format(i+1))
            percolation = Percolation(self.n)
            all_coordinates = []
            for i in range(0, self.n):
                for j in range(0, self.n):
                    all_coordinates.append((i,j))
            while not percolation.percolates():
                random_coord = random.choice(all_coordinates)
                all_coordinates.pop(all_coordinates.index(random_coord))
                percolation.open(random_coord)

            print("Percolates!")
            number_of_open_sites = percolation.number_of_open_sites()
            percolation_threshold = float(number_of_open_sites)/float(self.n**2)
            print("Number of open sites: {0}".format(number_of_open_sites))
            print("Percolation threshold: {0}".format(percolation_threshold))
            results.append(percolation_threshold)

        data = np.array(results)
        mean = np.mean(data)
        std = np.std(data)

        print("Mean is {0}".format(mean))
        print("Std is {0}".format(std))


if __name__ == "__main__":
    app = PercolationTest(200, 100)
    app.run_test()
