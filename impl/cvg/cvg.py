# Simulated Annealing elements
from core.problem import AbstractProblem
from core.solution import AbstractSolution
from core.transformation import AbstractTransformation

# Conlang elements
from impl.cvg.phonology import levenshtein, phroots, dephonemize

# Utilities
from functools import cache
from enum import Enum
import random

@cache
def element(r1, r2):
  return max(len(r1), len(r2)) / levenshtein(r1, r2)

class Selection(Enum):
   DETERMINISTIC = 0
   PROBABILISTIC = 1
   UNIFORM  = 2

class Chunk:
   
   def __init__(self):
      self.values = None
      self.scores = None
      self.cost = None
      
   @staticmethod
   def new(values: list[str]):
      chunk = Chunk()
      chunk.values = list(values)
      chunk.scores = [0 for _ in values]
      chunk.recompute()
      return chunk
   
   def copy(self):
      chunk = Chunk()
      chunk.values = list(self.values)
      chunk.scores = list(self.scores)
      chunk.cost = self.cost
      return chunk
   
   def recompute(self):
      
      for i in range(len(self.scores)):
         self.scores[i] = 0
      
      for i in range(1, len(self.values)):
         value1 = self.values[i]
         
         for j in range(0, i):
            value2 = self.values[j]
            
            measure = element(value1, value2)
            self.scores[i] = max(self.scores[i], measure)
            self.scores[j] = max(self.scores[j], measure)
            
      self.cost = max(self.scores)
   
   def index(self, selection: Selection) -> int:
      if selection == Selection.DETERMINISTIC:
         i = 0
         for j in range(1, len(self.scores)):
            if self.scores[j] > self.scores[i]:
               i = j
         return i
      elif selection == Selection.PROBABILISTIC:
         return random.choices(range(len(self.scores)),
                               weights=self.scores,
                               k=1)[0]
      elif selection == Selection.UNIFORM:
         return random.choice(range(len(self.scores)))
      else:
         raise Exception(f'Invalid selection type: {selection}.')
   
   def pop(self, selection: Selection) -> str:
      i = self.index(selection)
      self.values[i], self.values[-1] = self.values[-1], self.values[i]
      self.scores[i], self.scores[-1] = self.scores[-1], self.scores[i]
      self.scores.pop()
      return self.values.pop()
   
   def put(self, value: str):
      self.values.append(value)
      self.scores.append(0)
      self.recompute()
   
   def get_values(self) -> list[str]:
      return sorted(map(dephonemize, self.values))

class CvgSolution(AbstractSolution):
   
   def __init__(self):
      self.chunks = None
      self.pool = None
      self.cost = None
   
   @staticmethod
   def new(values, chunk_number, chunk_length, shuffle=True):
      
      if shuffle:
         values = list(values)
         random.shuffle(values)
         
      sol = CvgSolution()
      sol.chunks = [
         Chunk.new(values[i * chunk_length : (i + 1) * chunk_length])
         for i in range(chunk_number)
      ]
      sol.pool = values[chunk_number * chunk_length : ]
      sol.cost = max(chunk.cost for chunk in sol.chunks)
      return sol
      
   def get_cost(self):
      return self.cost
   
   def copy(self, deep=None):
      sol = CvgSolution()
      sol.chunks = list(self.chunks)
      if deep is not None:
         sol.chunks[deep] = sol.chunks[deep].copy()
      sol.pool = list(self.pool)
      sol.cost = self.cost
      return sol
   
   def get_chunks(self):
      return [
         chunk.get_values()
         for chunk in sorted(self.chunks, key=lambda ch: ch.cost)
      ]

class CvgTransformation(AbstractTransformation):
   
   def __init__(self, chunk: Selection,
                      value: Selection,
                      other: Selection):
      self.chunk = chunk
      self.value = value
      self.other = other
   
   def select_chunk(self, sol: CvgSolution) -> int:
      if self.chunk == Selection.DETERMINISTIC:
         i = 0
         for j in range(1, len(sol.chunks)):
            if sol.chunks[j].cost > sol.chunks[i].cost:
               i = j
         return i
      elif self.chunk == Selection.PROBABILISTIC:
         return random.choices(range(len(sol.chunks)),
                               weights=[chunk.cost for chunk in sol.chunks],
                               k=1)[0]
      elif self.chunk == Selection.UNIFORM:
         return random.randrange(len(sol.chunks))
   
   def select_other(self, value: str, pool: list[str]) -> int:
      
      if self.other == Selection.DETERMINISTIC:
         best_index, best_score = 0, element(value, pool[0])
         for index in range(1, len(pool)):
            score = element(value, pool[index])
            if score > best_score:
               best_index, best_score = index, score
         return best_index
      
      elif self.other == Selection.PROBABILISTIC:
         return random.choices(range(len(pool)),
                               weights=[element(value, other) for other in pool],
                               k=1)[0]
      
      elif self.other == Selection.UNIFORM:
         return random.randrange(len(pool))
      
      else:
         raise Exception(f'Invalid selection type: {self.other}.')
   
   def transform(self, s: CvgSolution) -> CvgSolution:
      
      # Select the chunk and make a copy, with the chunk being deep-copied
      chunk_index = self.select_chunk(s)
      sol = s.copy(deep=chunk_index)
      chunk = sol.chunks[chunk_index]
      
      # Select the value from the chunk
      value = chunk.pop(self.value)
      
      # Select the value from the pool
      other_index = self.select_other(value, sol.pool)
      sol.pool[other_index], sol.pool[-1] = sol.pool[-1], sol.pool[other_index]
      other = sol.pool.pop()
      
      # Exchange
      chunk.put(other)
      sol.pool.append(value)
      
      # Update the cost of the solution
      sol.cost = max(chunk.cost for chunk in sol.chunks)
      
      return sol

class CvgProblem(AbstractProblem):
    
   def __init__(self, chunk_number, chunk_length, estimation_length=None):
      self.chunk_number = chunk_number
      self.chunk_length = chunk_length
      self.estimation_length = estimation_length if estimation_length is not None else 10 * chunk_length
   
   def estimate_increment(self) -> float:
       
      sol = self.initial_solution()
      min_cost, max_cost = sol.get_cost(), sol.get_cost()
      
      transformers = self.transformations()
      for _ in range(self.estimation_length):
         sol = random.choice(transformers).transform(sol)
         min_cost = min(min_cost, sol.get_cost())
         max_cost = max(max_cost, sol.get_cost())
      return max_cost - min_cost
   
   def initial_solution(self) -> AbstractSolution:
      return CvgSolution.new(phroots(),
                             self.chunk_number,
                             self.chunk_length,
                             shuffle=True)
       
   def transformations(self) -> list[AbstractTransformation]:
      return [
         CvgTransformation(Selection.DETERMINISTIC, Selection.DETERMINISTIC, Selection.DETERMINISTIC),
         CvgTransformation(Selection.DETERMINISTIC, Selection.DETERMINISTIC, Selection.PROBABILISTIC),
         CvgTransformation(Selection.DETERMINISTIC, Selection.PROBABILISTIC, Selection.DETERMINISTIC),
         CvgTransformation(Selection.DETERMINISTIC, Selection.PROBABILISTIC, Selection.PROBABILISTIC),
         CvgTransformation(Selection.PROBABILISTIC, Selection.DETERMINISTIC, Selection.DETERMINISTIC),
         CvgTransformation(Selection.PROBABILISTIC, Selection.DETERMINISTIC, Selection.PROBABILISTIC),
         CvgTransformation(Selection.PROBABILISTIC, Selection.PROBABILISTIC, Selection.DETERMINISTIC),
         CvgTransformation(Selection.PROBABILISTIC, Selection.PROBABILISTIC, Selection.PROBABILISTIC),
      ]
   
   def suggested_weights(self):
      return None

   
   