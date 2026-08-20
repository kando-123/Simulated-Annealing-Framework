from core.problem import AbstractProblem
from core.solution import AbstractSolution
from core.scheme import GeometricScheme, LundyMeesScheme, LinearScheme
from core.transformation import AbstractTransformer, UniformTransformer, AdaptiveTransformer

import math
import random



class SimulatedAnnealing:
    
    def __init__(self, n_iters, scheme, transformer, callback = None):
        self.n_iters = n_iters
        self.scheme = scheme
        self.transformer = transformer
        self.callback = callback
    
    def solve(self, problem: AbstractProblem) -> AbstractSolution:
        
        # Tracking variables
        current = problem.initial_solution()
        best = current
        
        # Prepare the cooling scheme
        increment = problem.estimate_increment()
        self.scheme.reset(increment)
        def probability(delta):
            return math.exp(-delta / self.scheme.temperature())
        
        # Prepare the transformer
        transformations = problem.transformations()
        self.transformer.reset(transformations)
        
        # Search loop
        while not self.scheme.is_minimal():
            for _ in range(self.n_iters):
                
                # Transform
                candidate = self.transformer.transform(current)
                
                # Unconditional update
                if candidate.get_cost() < current.get_cost():
                    current = candidate
                    if current.get_cost() < best.get_cost():
                        best = current
                
                # Probabilistic update
                else:
                    increment = candidate.get_cost() - current.get_cost()
                    chance = probability(increment)
                    if random.random() < chance:
                        current = candidate
                
                if self.callback is not None:
                    self.callback(best, current)
            
            self.scheme.decrease()
            
        return best