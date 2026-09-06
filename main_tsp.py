from core.sa import SimulatedAnnealing
from core.scheme import LundyMeesScheme, GeometricScheme, LinearScheme
from core.transformation import UniformTransformer, AdaptiveTransformer
from impl.tsp import TspProblem

import argparse
import json

# import sys
# sys.argv.extend(['-ins', './data/tsp/ins/tsp_g05x05.json',
#                  '-sol', './data/tsp/sol/tsp_g05x05',
#                  '-n', '10'])

parser = argparse.ArgumentParser()
parser.add_argument('-ins', type=str, help='instance to be solved')
parser.add_argument('-sol', type=str, help='output file (without .json)')
parser.add_argument('-alg', type=str, help='algorithm configuration')
parser.add_argument('-n', type=int, help='number of runs', default=1)
args = parser.parse_args()

print(f'-ins = {args.ins}')
print(f'-sol = {args.sol}')
print(f'-alg = {args.alg if args.alg is not None else "None"}')
print(f'-n = {args.n}')

with open(args.ins, 'r') as ins_f:
    instance_data = json.load(ins_f)

if args.alg is not None:
    with open(args.alg, 'r') as alg_f:
        alg_cfg = json.load(alg_f)
else:
    alg_cfg = {
        "n_iters": 2500,
        "scheme": 'lundymees',
        "n_epochs": 2000,
        "prob1": 0.95,
        "prob2": 0.05,
        "fraction": 0.0001,
        "transformer": 'adaptive'
    }

n_cities = instance_data["n_cities"]

tsp = TspProblem(n_cities)

distances_dict = instance_data["distances"]
for u, vals in distances_dict.items():
    for v, d in vals.items():
        tsp[int(u), int(v)] = d

scheme = {
    'lundymees': LundyMeesScheme.create,
    'geometric': GeometricScheme.create,
    'linear': LinearScheme.create
}[alg_cfg.pop('scheme', 'lundymees')](**alg_cfg)

transformer = {
    'uniform': UniformTransformer.create,
    'adaptive': AdaptiveTransformer.create
}[alg_cfg.pop('transformer', 'uniform')](**alg_cfg)

sa = SimulatedAnnealing.create(scheme = scheme,
                               transformer = transformer,
                               **alg_cfg)

for n in range(args.n):
    
    print(f'Attempt #{n}...')
    sol = sa.solve(tsp)
    
    print(f'\tCost = {sol.get_cost()}')
    print(f'\tCost = {tsp.compute_cost(sol.cities)}, recomputed')
    
    with open(f'{args.sol}_{n}.json', 'w') as fp:
        json.dump(sol.cities, fp)
    
    print(f'\tSaved as {fp.name}')