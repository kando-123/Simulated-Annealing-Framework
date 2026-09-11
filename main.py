import random

from impl.cvg.phonology import phonemize, dephonemize
from impl.cvg.cvg import element, Chunk

import json

with open('./conlang100x40-2/chunks.json', 'r') as file:
   chunks = json.load(file)


max_cost = 0
for values in chunks:
   chunk = Chunk.new(list(map(phonemize, values)))
   if chunk.cost > max_cost:
      max_cost = chunk.cost
      i, j = 0, len(chunk.scores) - 1
      while chunk.scores[i] < max_cost:
         i += 1
      while chunk.scores[j] < max_cost:
         j -= 1
      value1 = dephonemize(chunk.values[i])
      value2 = dephonemize(chunk.values[j])
      print(f'{value1} : {value2} = {chunk.scores[i]:.4f} | {chunk.scores[j]:.4f} ({element(value1, value2)})')

print(max_cost)