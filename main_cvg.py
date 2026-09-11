from impl.cvg.cvg import CvgProblem
from impl.cvg.phonology import roots
from core.sa import SimulatedAnnealing
from core.scheme import LundyMeesScheme
from core.transformation import AdaptiveTransformer

import json
import os

class Callback:
    
    def __init__(self):
        self.iter = 0
        self.last = None
    
    def __call__(self, best, curr):
        if self.last is None or best != self.last:
            print(f'{self.iter:6d}. best={best.get_cost():.2f}')
            self.last = best
        self.iter += 1

class AdaptiveTransformerCallback:
    
    def __init__(self, k = 1000, m = 100, n = 1000):
        self.i = 0
        self.k = k
        self.m = m
        self.n = n
    
    def __call__(self, at):
        if self.i % (self.m if self.i < self.k else self.n) == 0:
            print(f'{self.i:6d}. weights=[', end='')
            for i, weight in enumerate(at.weights):
                print(f'{weight:5.3f}', end=' ' if i < len(at.weights) - 1 else '')
            print(']')
        self.i += 1
 
POOL = roots()
print(len(POOL))

FOLDER = './conlang100x40-2/'

if not os.path.exists(FOLDER):
    os.mkdir(FOLDER)

with open(FOLDER + 'roots.json', 'w') as file:
   json.dump(sorted(POOL), file)
print(f'Saved all the roots, in alphabetical order, in "{FOLDER}roots.json".')

sa = SimulatedAnnealing(500,
                        scheme=LundyMeesScheme(500, 0.95, 0.05, 0.001),
                        transformer=AdaptiveTransformer(initial_weight=100,
                                                        min_weight=1,
                                                        max_weight=10000,
                                                        positive_feedback=1.05,
                                                        negative_feedback=1.05,
                                                        callback=AdaptiveTransformerCallback()),
                        callback=Callback(),
                        threshold=4/3)
cvg = CvgProblem(chunk_number=100, chunk_length=40, estimation_length=500)
sol = sa.solve(cvg)

chunks = sol.get_chunks()

with open(FOLDER + 'chunks.json', 'w') as file:
    json.dump(chunks, file)

print(f'Saved the chunks in "{FOLDER}chunks.json".')

for i, chunk in enumerate(chunks):
    print(f'CHUNK {i}')
    for value in chunk:
        print(value, end=' ')
    print()
    
print(f'COST {sol.get_cost()}')