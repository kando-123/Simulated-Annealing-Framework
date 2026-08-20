from core.problem import AbstractProblem
from core.solution import AbstractSolution
from core.scheme import GeometricScheme, LundyMeesScheme, LinearScheme
from core.transformation import AbstractTransformer, UniformTransformer, AdaptiveTransformer

import math
import random



class SimulatedAnnealing:
    
    # Keyword arguments:
    # - n_iters = numer of iterations per cooling scheme epoch, default 1000
    # - scheme = type of cooling scheme: 'lundymees' (default), 'geometric',
    #   'linear'; see the respective class for required additional kwargs
    # - transformer = type of transformation pool: 'uniform' (default),
    #   'adaptive'; see the respective class for required additional kwargs
    # - callback (optional) = callable invoked with the best and the current
    #   solution at the end of every iteration, the call should execute quickly
    def __init__(self, **kwargs):
        self.n_iters = kwargs.get('n_iters', 1000)
        self.scheme = SimulatedAnnealing.make_scheme(**kwargs)
        self.transformer = SimulatedAnnealing.make_transformer(**kwargs)
        self.callback = kwargs.get('callback')
    
    SCHEME_CREATORS = {
        'geometric': GeometricScheme.create,
        'lundymees': LundyMeesScheme.create,
        'linear':    LinearScheme.create
    }
    
    @staticmethod
    def make_scheme(**kwargs):
        creator = SimulatedAnnealing.SCHEME_CREATORS.get(kwargs.get('scheme', 'lundymees'))
        if creator is not None:
            return creator(**kwargs)
        else:
            raise Exception(f"Unknown cooling scheme type: '{kwargs['scheme']}'")
    
    TRANSFORMER_CREATORS = {
        'uniform': UniformTransformer.create,
        'adaptive': AdaptiveTransformer.create
    }
    
    @staticmethod
    def make_transformer(**kwargs) -> AbstractTransformer:
        creator = SimulatedAnnealing.TRANSFORMER_CREATORS.get(kwargs.get('transformer', 'uniform'))
        if creator is not None:
            return creator(**kwargs)
        else:
            raise Exception(f"Unknown transformer type: '{kwargs['transformer']}'")
    
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