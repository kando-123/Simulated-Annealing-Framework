import math
import random
import json

def generate_grid_tsp(n_rows, n_cols, unit=1) -> dict[str, object]:
    
    vertices = [ (col * unit, row * unit) for col in range(n_cols) for row in range(n_rows) ]
    n = len(vertices)
    tsp = { "n_cities": n, "coords": vertices }
    distances = dict()
    for i in range(n):
        distances[i] = {}
        for j in range(i):
            x1, y1 = vertices[i]
            x2, y2 = vertices[j]
            distances[i][j] = math.hypot(x1 - x2, y1 - y2)
    tsp["distances"] = distances
    return tsp

def generate_random_tsp(n, width, height):
    
    vertices = set()
    while len(vertices) < n:
        x = round(random.random() * width, 3)
        y = round(random.random() * height, 3)
        v = (x, y)
        vertices.add(v)
    
    vertices = list(vertices)
    tsp = { "n_cities": n, "coords": vertices }
    distances = dict()
    for i in range(n):
        distances[i] = {}
        for j in range(i):
            x1, y1 = vertices[i]
            x2, y2 = vertices[j]
            distances[i][j] = math.hypot(x1 - x2, y1 - y2)
    tsp["distances"] = distances
    return tsp

instances = {
    'tsp_g05x05': generate_grid_tsp( 5,  5),
    'tsp_g06x06': generate_grid_tsp( 6,  6),
    'tsp_g07x07': generate_grid_tsp( 7,  7),
    'tsp_g08x08': generate_grid_tsp( 8,  8),
    'tsp_g09x09': generate_grid_tsp( 9,  9),
    'tsp_g10x10': generate_grid_tsp(10, 10),
    'tsp_g11x11': generate_grid_tsp(11, 11),
    'tsp_g12x12': generate_grid_tsp(12, 12),
    'tsp_g15x15': generate_grid_tsp(15, 15),
    'tsp_g20x20': generate_grid_tsp(20, 20),
    
    'tsp_r025_1': generate_random_tsp( 25, 10, 10),
    'tsp_r025_2': generate_random_tsp( 25, 10, 10),
    'tsp_r025_3': generate_random_tsp( 25, 10, 10),
    
    'tsp_r036_1': generate_random_tsp( 36, 10, 10),
    'tsp_r036_2': generate_random_tsp( 36, 10, 10),
    'tsp_r036_3': generate_random_tsp( 36, 10, 10),
    
    'tsp_r049_1': generate_random_tsp( 49, 10, 10),
    'tsp_r049_2': generate_random_tsp( 49, 10, 10),
    'tsp_r049_3': generate_random_tsp( 49, 10, 10),
    
    'tsp_r064_1': generate_random_tsp( 64, 10, 10),
    'tsp_r064_2': generate_random_tsp( 64, 10, 10),
    'tsp_r064_3': generate_random_tsp( 64, 10, 10),
    
    'tsp_r081_1': generate_random_tsp( 81, 10, 10),
    'tsp_r081_2': generate_random_tsp( 81, 10, 10),
    'tsp_r081_3': generate_random_tsp( 81, 10, 10),
    
    'tsp_r100_1': generate_random_tsp(100, 10, 10),
    'tsp_r100_2': generate_random_tsp(100, 10, 10),
    'tsp_r100_3': generate_random_tsp(100, 10, 10),
    
    'tsp_r121_1': generate_random_tsp(121, 10, 10),
    'tsp_r121_2': generate_random_tsp(121, 10, 10),
    'tsp_r121_3': generate_random_tsp(121, 10, 10),
    
    'tsp_r144_1': generate_random_tsp(144, 10, 10),
    'tsp_r144_2': generate_random_tsp(144, 10, 10),
    'tsp_r144_3': generate_random_tsp(144, 10, 10),
    
    'tsp_r225_1': generate_random_tsp(225, 10, 10),
    'tsp_r225_2': generate_random_tsp(225, 10, 10),
    'tsp_r225_3': generate_random_tsp(225, 10, 10),
    
    'tsp_r400_1': generate_random_tsp(400, 10, 10),
    'tsp_r400_2': generate_random_tsp(400, 10, 10),
    'tsp_r400_3': generate_random_tsp(400, 10, 10),
}

for filename, contents in instances.items():
    
    with open(f'../ins/{filename}.json', 'w') as fp:
        json.dump(contents, fp, indent=2)