from core.sa import SimulatedAnnealing
from core.scheme import LundyMeesScheme
from core.transformation import UniformTransformer

from impl.dvg import PlvProblem

import json

class Callback:
    
    def __init__(self, N=10000):
        self.N = N
        self.n = 0
    
    def __call__(self, best, curr):
        if self.n % self.N == 0:
            print(f'{self.n}. best={best.get_cost():.3f}, curr={curr.get_cost():.3f}')
        self.n += 1

sa = SimulatedAnnealing(n_iters=1000,
                        scheme=LundyMeesScheme(n_epochs=1000,
                                               prob1=0.95,
                                               prob2=0.05,
                                               fraction=0.001),
                        transformer=UniformTransformer(),
                        callback=Callback())
solution = sa.solve(PlvProblem(500, estimation_len=100))
with open('plv-4.json', 'w') as fp:
    json.dump(solution.elements(), fp)
