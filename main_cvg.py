from impl.cvg import CvgProblem, POOL
from core.sa import SimulatedAnnealing
from core.scheme import LundyMeesScheme
from core.transformation import AdaptiveTransformer

import json

class Callback:
    
    def __init__(self):
        self.iter = 0
        self.last = None
    
    def __call__(self, best, curr):
        if self.last is None or best != self.last:
            print(f'{self.iter:6d}. best={best.get_cost():.6f}, curr={curr.get_cost():.6f}')
            self.last = best
        self.iter += 1

print(len(POOL))

# with open('roots.json', 'w') as file:
#    json.dump(sorted(POOL), file)
# print('Saved all the roots, in alphabetical order, in "roots.json".')

sa = SimulatedAnnealing(1000,
                        scheme=LundyMeesScheme(1000, 0.95, 0.05, 0.001),
                        transformer=AdaptiveTransformer(),
                        callback=Callback())

cvg = CvgProblem(chunk_number=50, chunk_length=80)
sol = sa.solve(cvg)

chunks = sol.get_chunks()

with open('chunks.json', 'w') as file:
    json.dump(chunks, file)

print('Saved the chunks in "chunks.json".')

for i, chunk in enumerate(chunks):
    print(f'CHUNK {i}')
    for value in chunk:
        print(value, end=' ')
    print()
    
print(f'COST {sol.get_cost()}')