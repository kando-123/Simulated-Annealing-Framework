from core.problem import AbstractProblem
from core.solution import AbstractSolution
from core.transformation import AbstractTransformation

import random



class TspSolution(AbstractSolution):
    
    def __init__(self, n_cities: int):
        self.n_cities = n_cities
        self.cities = []
        self.cost = None
    
    def __getitem__(self, pos: int) -> int:
        return self.cities[pos]
    
    def is_well_defined(self):
        if self.cost is None or not self.cost > 0.0:
            return False
        else:
            s = set(self.cities)
            s.discard(None)
            return len(s) == self.n_cities
    
    def get_copy(self):
        copy = TspSolution(self.n_cities)
        copy.cities = list(self.cities)
        copy.cost = self.cost
        return copy
    
    def get_cost(self):
        return self.cost



class TspMoveTransformation(AbstractTransformation):
    
    def __init__(self, problem):
        self.problem = problem
    
    def transform(self, s1: TspSolution) -> TspSolution:
        
        # The new solution
        s2 = s1.get_copy()
        
        # Shorthands
        tsp = self.problem
        n = tsp.n_cities; assert s1.n_cities == n and s2.n_cities == n
        
        # Removal
        i = random.randrange(n) # i = 0, ..., n-1

        c1, c2 = s2.cities[(i - 1) % n], s2.cities[(i + 1) % n]
        c = s2.cities.pop(i) # Now, s2.cities has n-1 elements!
        
        s2.cost -= tsp[c1, c] + tsp[c, c2]
        s2.cost += tsp[c1, c2]
        
        # Reinsertion
        j = random.randrange(n - 2) # j = 0, ..., n-3
        if j >= i:
            j += 1 # j = 0, ..., i-1, i+1, ..., n-2
        
        s2.cities.insert(j, c)        
        c1, c2 = s2.cities[(j - 1) % n], s2.cities[(j + 1) % n]
        
        s2.cost -= tsp[c1, c2]
        s2.cost += tsp[c1, c] + tsp[c, c2]
        
        return s2



class TspSwapTransformation(AbstractTransformation):
    
    def __init__(self, problem):
        self.problem = problem
    
    def transform(self, s1: TspSolution) -> TspSolution:
        
        # The new solution
        s2 = s1.get_copy()
        
        # Shorthands
        tsp = self.problem
        n = tsp.n_cities; assert s1.n_cities == n and s2.n_cities == n
        
        # Indices
        i, j = sorted(random.sample(range(n), 2))
        
        if j == i + 1:
            o1, o2 = s2.cities[(i - 1) % n], s2.cities[(j + 1) % n]
            i1, i2 = s2.cities[i], s2.cities[j]
            s2.cost -= tsp[o1, i1] + tsp[i2, o2]
            s2.cost += tsp[o1, i2] + tsp[i1, o2]
        elif j == n - 1 and i == 0:
            o1, o2 = s2.cities[(j - 1) % n], s2.cities[(i + 1) % n]
            i1, i2 = s2.cities[j], s2.cities[i]
            s2.cost -= tsp[o1, i1] + tsp[i2, o2]
            s2.cost += tsp[o1, i2] + tsp[i1, o2]
        else:
            b1, c1, a1 = s2.cities[(i - 1) % n], s2.cities[i], s2.cities[(i + 1) % n]
            b2, c2, a2 = s2.cities[(j - 1) % n], s2.cities[j], s2.cities[(j + 1) % n]
            s2.cost -= tsp[b1, c1] + tsp[c1, a1]
            s2.cost -= tsp[b2, c2] + tsp[c2, a2]
            s2.cost += tsp[b1, c2] + tsp[c2, a1]
            s2.cost += tsp[b2, c1] + tsp[c1, a2]
        
        # Swap
        s2.cities[i], s2.cities[j] = s2.cities[j], s2.cities[i]
        
        # # City values: before (b), the city (c), after (a)
        # b1, c1, a1 = s2.cities[(i - 1) % n], s2.cities[i], s2.cities[(i + 1) % n]
        # b2, c2, a2 = s2.cities[(j - 1) % n], s2.cities[j], s2.cities[(j + 1) % n]
        # 
        # # Remove the old edges' costs
        # old_edges = { (b1, c1), (c1, a1), (b2, c2), (c2, a2) }
        # for edge in old_edges:
        #     s2.cost -= tsp[edge]
        # 
        # # Swap
        # s2.cities[i], s2.cities[j] = s2.cities[j], s2.cities[i]
        # 
        # # Add the new edges' costs
        # new_edges = { (b1, c2), (c2, a1), (b2, c1), (c1, a2) }
        # for edge in new_edges:
        #     s2.cost += tsp[edge]
        
        return s2



class Tsp2OptTransformation(AbstractTransformation):
    
    def __init__(self, problem):
        self.problem = problem
    
    def transform(self, s1: TspSolution) -> TspSolution:
        
        # Copy
        s2 = s1.get_copy()
        
        # Shorthands
        tsp = self.problem;
        n = tsp.n_cities; assert s1.n_cities == n and s2.n_cities == n
        
        # Indices
        i = random.randrange(n)
        j = random.randrange(n - 3)
        if   i == n - 1:   j += 1   # j = 0,...,n-4 >> j = 1,...,n-3; j != n-2, n-1, 0
        elif i == 0:       j += 2   # j = 0,...,n-4 >> j = 2,...,n-2; j != n-1, 0, 1
        else:
            if j >= i - 1: j += 3   # j = 0,...,n-4 >> j = 0,...,i-2,i+2,...,n-1; j != i-1, i, i+1
        
        i, j = sorted((i, j))
        
        # City values: o - outer, i - inner
        o1 = s2.cities[(i - 1) % n]
        i1 = s2.cities[i]
        i2 = s2.cities[(j - 1) % n]
        o2 = s2.cities[j]
        
        # Subtract the removed edges
        s2.cost -= tsp[o1, i1] + tsp[i2, o2]
        
        # Revert
        s2.cities[i:j] = s2.cities[i:j][::-1]
        
        # Add the new created edges
        s2.cost += tsp[o1, i2] + tsp[i1, o2]
        
        return s2



class Tsp3OptTransformation(AbstractTransformation):
    
    def __init__(self, problem):
        self.problem = problem
    
    def transform(self, s1: TspSolution) -> TspSolution:
        
        # Copy
        s2 = s1.get_copy()
        
        # Shorthands
        tsp = self.problem
        n = tsp.n_cities; assert s1.n_cities == n and s2.n_cities == n
        
        i, j, k = sorted(random.sample(range(n), k=3))
        
        A = s2.cities[i:j]
        B = s2.cities[j:k]
        C = s2.cities[k:] + s2.cities[:i]
        
        a1, a2 = A[0], A[-1]
        b1, b2 = B[0], B[-1]
        c1, c2 = C[0], C[-1]
        
        s2.cost -= tsp[a2, b1] + tsp[b2, c1] + tsp[c2, a1]
        
        variant = random.randint(1, 4)
        if variant == 1:
            s2.cities = A + C + B
            s2.cost += tsp[a2, c1] + tsp[c2, b1] + tsp[b2, a1]
        elif variant == 2:
            s2.cities = A + C + B[::-1]
            s2.cost += tsp[a2, c1] + tsp[c2, b2] + tsp[b1, a1]
        elif variant == 3:
            s2.cities = A + C[::-1] + B
            s2.cost += tsp[a2, c2] + tsp[c1, b1] + tsp[b2, a1]
        else:
            s2.cities = A + B[::-1] + C[::-1]
            s2.cost += tsp[a2, b2] + tsp[b1, c2] + tsp[c1, a1]
            
        return s2



class TspDoubleBridgeTransformation(AbstractTransformation):
    
    def __init__(self, problem):
        self.problem = problem
    
    def transform(self, s1: TspSolution) -> TspSolution:
        
        # Copy
        s2 = s1.get_copy()
        
        # Shorthands
        tsp = self.problem
        n = tsp.n_cities; assert s1.n_cities == n and s2.n_cities == n
        
        # Indices
        i1, i2, i3, i4 = sorted(random.sample(range(n), k=4))
        
        # Segments
        A = s2.cities[i1:i2]
        B = s2.cities[i2:i3]
        C = s2.cities[i3:i4]
        D = s2.cities[i4:] + s2.cities[:i1]
        
        # Cities
        a1, a2 = A[0], A[-1]
        b1, b2 = B[0], B[-1]
        c1, c2 = C[0], C[-1]
        d1, d2 = D[0], D[-1]
        
        # Remove the old edges
        s2.cost -= tsp[a2, b1] + tsp[b2, c1] + tsp[c2, d1] + tsp[d2, a1]
        
        
        # Do the SHUFFLE!
        s2.cities = A + D + C + B
        
        # Add the new edges
        s2.cost += tsp[a2, d1] + tsp[d2, c1] + tsp[c2, b1] + tsp[b2, a1]
        
        return s2



class TspProblem(AbstractProblem):
    
    def __init__(self, n_cities: int, **kwargs):
        self.n_cities = n_cities
        self.distances = dict() # keys: tuples (row, col), row < col
        self.estimation_len = kwargs.get('estimation_len', 10 * n_cities)
    
    def __setitem__(self, indices: tuple[int, int], distance: float):
        row, col = indices
        if row == col and distance != 0:
            raise Exception(f"Distance from {row} to itself must be 0.")
        elif row < 0 or row >= self.n_cities or col < 0 or col >= self.n_cities:
            raise Exception(f"Indices ({row}, {col}) out of range for number of cities {self.n_cities}.")
        elif not distance > 0 or distance == float('inf') or distance != distance:
            raise Exception(f"Distance {distance} is invalid, it shall be finite and positive.")
        else:
            if row > col:
                indices = (col, row)
            self.distances[indices] = distance
    
    def __getitem__(self, indices: tuple[int, int]) -> float:
        row, col = indices
        if row == col:
            return 0
        elif row < 0 or row >= self.n_cities or col < 0 or col >= self.n_cities:
            raise Exception(f"Indices ({row}, {col}) out of range for number of cities {self.n_cities}.")
        else:
            if row > col:
                indices = (col, row)
            return self.distances[indices]
    
    def is_well_defined(self) -> bool:
        for col in range(1, self.n_cities):
            for row in range(0, col):
                if (row, col) not in self.distances:
                    return False
        return True
    
    def compute_cost(self, cities: list[int]):
        cost = 0
        for i in range(0, len(cities)):
            cost += self[cities[i - 1], cities[i]]
        return cost
    
    def random_solution(self) -> TspSolution:
        sol = TspSolution(self.n_cities)
        sol.cities = [city for city in range(self.n_cities)]
        random.shuffle(sol.cities)
        sol.cost = self.compute_cost(sol.cities)
        return sol
    
    def nearest_neighbor(self) -> TspSolution:
        start = random.randrange(self.n_cities)
        sol = TspSolution(self.n_cities)
        sol.cities.append(start)
        sol.cost = 0
        pool = set(range(self.n_cities))
        pool.remove(start)
        while pool:
            best, incr = None, float('inf')
            for city in pool:
                dist = self[sol.cities[-1], city]
                if best is None or dist < incr:
                    best = city
                    incr = dist
            pool.remove(best)
            sol.cities.append(best)
            sol.cost += incr
        sol.cost += self[sol.cities[-1], sol.cities[0]]
        return sol
    
    def initial_solution(self) -> TspSolution:
        return self.nearest_neighbor()
    
    def estimate_increment(self) -> float:
        solution = self.nearest_neighbor() # Probably relatively low
        min_cost = solution.get_cost()
        max_cost = solution.get_cost()
        for _ in range(self.estimation_len):
            solution = self.random_solution() # Probably relatively high
            min_cost = min(solution.get_cost(), min_cost)
            max_cost = max(solution.get_cost(), max_cost)
        return max_cost - min_cost
    
    def transformations(self) -> list[AbstractTransformation]:
        return [
            # TspMoveTransformation(self),
            # TspSwapTransformation(self),
            # Tsp2OptTransformation(self),
            # Tsp3OptTransformation(self),
            TspDoubleBridgeTransformation(self)
        ]
