from core.solution import AbstractSolution

import random



# Single transformation operator. If the solution caches the cost, the transformation
# shall update the cost (which will probably be quicker than full reevaluation).
class AbstractTransformation:
    
    def transform(self, s: AbstractSolution) -> AbstractSolution:
        pass



class AbstractTransformer:
    
    @staticmethod
    def create(**kwargs):
        pass
    
    def reset(self, t: list[AbstractTransformation]):
        pass
    
    def transform(self, s: AbstractSolution) -> AbstractSolution:
        pass



class UniformTransformer(AbstractTransformer):
    
    @staticmethod
    def create(**kwargs):
        return UniformTransformer()
    
    def __init__(self):
        self.pool = []
    
    def reset(self, transformations: list[AbstractTransformation]):
        self.pool = list(transformations)
    
    def transform(self, s: AbstractSolution) -> AbstractSolution:
        return random.choice(self.pool).transform(s)



# Adaptive weighted transformer. Selects transformations in a weighted manner.
#
# Upon transforming a solution, the weight is updated based on whether the solution
# obtained is better than the given one. If yes, the weight is multiplied by given
# positive feedback multiplier; if it is worse, the weight is divided by the negative
# feedback divisor.
#
# Minimal and maximal values for the weights are assumed to prevent a few transformations
# from dominating the pool.
class AdaptiveTransformer(AbstractTransformer):
    
    @staticmethod
    def create(**kwargs):
        return AdaptiveTransformer(kwargs)
    
    # Keyword arguments:
    # - positive_feedback = multiplier applied on the weights in case of improvement,
    #   >1.0, default 1.10 (i.e. +10%)
    # - negative_feedback = divisor applied on the weights in case of worsening,
    #   >1.0, default 1.01 (i.e. -1%)
    # - initial_weight = the initial weight, >0.0, default 1.0
    # - min_weight = the lower bound for the weights, >=0.0 (0.0 turns the lower
    #   bound mechanism off), default 0.1
    # - max_weight = the upper bound for the weights, >>min_weight (infinity turns
    #   the upper bound mechanism off), default 10
    def __init__(self, **kwargs):
        
        self.initial_weight = kwargs.get('initial_weight', 1.0)        
        self.positive_feedback = kwargs.get('positive_feedback', 1.10) # MULTIPLIER
        self.negative_feedback = kwargs.get('negative_feedback', 1.01) # DIVISOR!!!
        self.min_weight = kwargs.get('min_weight', 0.10)
        self.max_weight = kwargs.get('max_weight', 10.0)
        self.check_args()
        
        self.pool = None
        self.indices = None
        self.weights = None
    
    def check_args(self):
        if (val := self.positive_feedback) <= 1.0 or val == float('inf') or val != val: # the self-inequality detects NaN
            raise Exception(f"Value {val} is illegal for the positive feedback multiplier, shall be finite and >1.0")
        if (val := self.negative_feedback) <= 1.0 or val == float('inf') or val != val:
            raise Exception(f"Value {val} is illegal for the negative feedback multiplier, shall be finite and >1.0")
        if (val := self.initial_weight <= 0.0) or val == float('inf') or val != val:
            raise Exception(f"Value {val} is illegal for the initial weight, shall be finite and positive.")
        if (val := self.min_weight < 0.0) or val == float('inf') or val != val:
            raise Exception(f"Value {val} is illegal for the minimal weight, shall be finite and nonnegative.")
        if (val := self.max_weight < self.min_weight) or val != val:
            raise Exception(f"Value {val} is illegal for the maximal weight, shall be greater than the minimal weight, and not NaN.")
        
    def reset(self, transformations: list[AbstractTransformation]):
        self.pool = list(transformations)
        self.indices = [i for i in range(len(self.pool))]
        self.weights = [self.initial_weight for transformation in self.pool]
    
    def transform(self, s1: AbstractSolution) -> AbstractSolution:
        
        # Transformation
        index = random.choices(self.indices, self.weights, k=1)[0]
        s2 = self.pool[index].transform(s1)
        
        # Adaptation
        if s2.get_cost() < s1.get_cost():
            self.weights[index] = min(self.weights[index] * self.positive_feedback, self.max_weight)
        elif s2.get_cost() > s1.get_cost():
            self.weights[index] = max(self.weights[index] / self.negative_feedback, self.min_weight)
        
        return s2