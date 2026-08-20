from core.solution import AbstractSolution
from core.transformation import AbstractTransformation



class AbstractProblem:
    
    # Performs random walk to estimate upper bound for cost increment.
    def estimate_increment(self) -> float:
        pass
    
    # Returns a solution (random, heuristic, deterministic, whatever).
    def initial_solution(self) -> AbstractSolution:
        pass
    
    # Returns problem-specific transformations applicable to the solutions.
    def transformations(self) -> list[AbstractTransformation]:
        pass