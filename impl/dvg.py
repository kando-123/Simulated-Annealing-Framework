from core.problem import AbstractProblem
from core.solution import AbstractSolution
from core.transformation import AbstractTransformation

import random



# DVG = DIVERSE VALUES GENERATION

class DvgSolution(AbstractSolution):
    
    def __init__(self,
                 size,  # number of elements in the subset
                 pool): # the list of all possible values
        self.size = size
        self.pool = list(pool)
        self.cost = None
    
    def get_copy(self):
        copy = DvgSolution(self.size, self.pool)
        copy.cost = self.cost
        return copy
    
    def get_cost(self) -> float:
        return self.cost
    
    def elements(self):
        return self.pool[:self.size]



class DvgSwapTransformation(AbstractTransformation):
    
    def __init__(self, problem):
        self.problem = problem
    
    def transform(self, s1: DvgSolution) -> DvgSolution:
        
        # Copy
        s2 = s1.get_copy()
        
        # Shorthands
        dist_func = self.problem.dist
        n = s2.size
        N = len(s2.pool)
        
        # Indices
        i, j = random.randrange(0, n), random.randrange(n, N)
        
        # Cost update
        old, new = s2.pool[i], s2.pool[j]
        for e, elem in enumerate(s2.pool[:n]):
            if e == i: continue
            s2.cost -= 1 / dist_func(elem, old)
            s2.cost += 1 / dist_func(elem, new)
        
        # Swap
        s2.pool[i], s2.pool[j] = new, old
        
        return s2


class DvgProblem(AbstractProblem):
    
    def __init__(self, size, pool, dist, **kwargs):
        self.size = size
        self.pool = pool
        self.dist = dist
        self.estimation_len = kwargs.get('estimation_len', size)
        if self.size >= len(self.pool):
            raise Exception('The size of the result shall be (preferably much) less than the size of the input pool.')
    
    def compute_cost(self, elems: list) -> float:
        cost = 0
        for i in range(1, len(elems)):
            lhs = elems[i]
            for j in range(0, i):
                rhs = elems[j]
                dist = self.dist(lhs, rhs)
                cost += 1 / dist
        return cost
    
    def estimate_increment(self) -> float:
        
        solution = self.initial_solution()
        min_cost = solution.get_cost()
        max_cost = solution.get_cost()
        transformation = DvgSwapTransformation(self)
        for _ in range(self.estimation_len):
            solution = transformation.transform(solution)
            min_cost = min(solution.get_cost(), min_cost)
            max_cost = max(solution.get_cost(), max_cost)
        return max_cost - min_cost
    
    def initial_solution(self) -> AbstractSolution:
        solution = DvgSolution(self.size, self.pool)
        random.shuffle(solution.pool)
        solution.cost = self.compute_cost(solution.pool[:solution.size])
        return solution
    
    def transformations(self) -> list[AbstractTransformation]:
        return [
            DvgSwapTransformation(self)
        ]



# PLV = PARROT LANGUAGE VOCABULARY

C_VALS = ['h', 'j', 'k', 'l', 'n', 'r', 's', 't', 'w']
C_DIST = {
    ('h', 'k'): 0.3, ('h', 's'): 0.5, ('h', 't'): 0.7,
    ('j', 'n'): 0.7, ('j', 'l'): 0.7, ('j', 'r'): 0.7, ('j', 'w'): 0.5,
    ('k', 's'): 0.7, ('k', 't'): 0.5,
    ('l', 'n'): 0.7, ('l', 'r'): 0.3,
    ('n', 'r'): 0.7,
    ('s', 't'): 0.5,
    ('w', 'n'): 0.7, ('w', 'l'): 0.7, ('w', 'r'): 0.7
}

V_VALS = ['a', 'e', 'i', 'o', 'u']
V_DIST = {
    ('a', 'e'): 0.5, ('a', 'o'): 0.5,
    ('e', 'i'): 0.5, ('o', 'u'): 0.5
}

T_VALS = ['1', '2', '3', '4']
T_DIST = {
    ('1', '3'): 0.7,
    ('2', '4'): 0.7
}



class PlvProblem(DvgProblem):
    
    @staticmethod
    def cdist(c1, c2):
        if c1 == c2:
            return 0
        else:
            return C_DIST.get((c1, c2), C_DIST.get((c2, c1), 1.0))
    
    
    @staticmethod
    def vdist(v1, v2):
        if v1 == v2:
            return 0
        else:
            return V_DIST.get((v1, v2), V_DIST.get((v2, v1), 1.0))
    
    @staticmethod
    def tdist(t1, t2):
        if t1 == t2:
            return 0
        else:
            return T_DIST.get((t1, t2), T_DIST.get((t2, t1), 1.0))
    
    SYLLABLES = { f'{c}{v}{t}' for c in C_VALS for v in V_VALS for t in T_VALS
                  if (c, v) not in {('j', 'i'), ('w', 'u')}}
    SYLLABLE_DISTANCE = None
    
    def __init__(self, size, **kwargs):
        
        if PlvProblem.SYLLABLE_DISTANCE is None:
            PlvProblem.SYLLABLE_DISTANCE = {
                (lhs, rhs): (PlvProblem.cdist(lhs[0], rhs[0]) +
                             PlvProblem.vdist(lhs[1], rhs[1]) +
                             PlvProblem.tdist(lhs[2], rhs[2]))
                for lhs in PlvProblem.SYLLABLES
                for rhs in PlvProblem.SYLLABLES
            }
        
        pool = [
            (s1, s2)
            for s1 in PlvProblem.SYLLABLES
            for s2 in PlvProblem.SYLLABLES
            if ((s1[2], s2[2]) in {
                    ('1', '2'), ('1', '3'),
                    ('2', '1'), ('2', '3'),
                    ('3', '1'), ('3', '4'),
                    ('4', '1'), ('4', '3')
            }
            and (s1[0], s1[1], s2[0]) not in {
                ('h', 'u', 'j'),
                ('s', 'u', 'k')
            })
            and (s1[0], s1[1], s2[0], s2[1]) != ('s', 'a', 't', 'a')
        ]
        
        if size >= len(pool):
            raise Exception(f'Size {size} too large for pool of size {len(pool)}')
        
        super().__init__(size, pool, PlvProblem.distance, **kwargs)
    
    def distance(elem1, elem2):
        syl11, syl12 = elem1
        syl21, syl22 = elem2
        return (PlvProblem.SYLLABLE_DISTANCE[syl11, syl21] +
                PlvProblem.SYLLABLE_DISTANCE[syl12, syl22])



