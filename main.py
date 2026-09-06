from impl.cvg import POOL, DELETION_COST, INSERTION_COST, TRANSPOSITION_COST, substitution_cost

import random

def levenshtein_matrix(root1, root2):
    
    n_rows, n_cols = len(root1) + 1, len(root2) + 1
    
    matrix = [[0 for col in range(n_cols)] for row in range(n_rows)]
    
    for row in range(n_rows): matrix[row][0] = row
    for col in range(n_cols): matrix[0][col] = col
    
    for row in range(1, n_rows):
        for col in range(1, n_cols):
            deletion     = matrix[row - 1][col] + DELETION_COST
            insertion    = matrix[row][col - 1] + INSERTION_COST
            substitution = matrix[row - 1][col - 1] + substitution_cost(root1[row - 1], root2[col - 1])
            distance = min(deletion, insertion, substitution)
            if row >= 2 and col >= 2:
                transposition = (matrix[row - 2][col - 2]
                                 + substitution_cost(root1[row - 1], root2[col - 2])
                                 + substitution_cost(root1[row - 2], root2[col - 1])
                                 + TRANSPOSITION_COST)
                distance = min(distance, transposition)
            matrix[row][col] = distance
    
    return matrix

import math
from impl.cvg import POOL, DELETION_COST, INSERTION_COST, TRANSPOSITION_COST, substitution_cost

def get_mutations(root1: str, root2: str, matrix: list[list[float]]) -> list[str]:
    """
    Odtwarza optymalną ścieżkę przekształcenia rdzenia root1 w root2
    na podstawie wypełnionej macierzy Damerau-Levenshteina.
    """
    mutations = []
    row, col = len(root1), len(root2)
    EPSILON = 1e-5  # Tolerancja dla porównań zmiennopozycyjnych

    while row > 0 or col > 0:
        current_val = matrix[row][col]

        # 1. WARUNEK TRANSPOZYCJI (zamiana/modyfikacja pary sąsiadujących znaków)
        if row >= 2 and col >= 2:
            cost_trans = (
                matrix[row - 2][col - 2]
                + substitution_cost(root1[row - 1], root2[col - 2])
                + substitution_cost(root1[row - 2], root2[col - 1])
                + TRANSPOSITION_COST
            )
            if math.isclose(current_val, cost_trans, abs_tol=EPSILON):
                src_pair = root1[row - 2 : row]
                tgt_pair = root2[col - 2 : col]
                mutations.append(f"{src_pair}~{tgt_pair}")
                row -= 2
                col -= 2
                continue

        # 2. WARUNEK SUBSTYTUCJI / TOŻSAMOŚCI (zamiana pojedynczego znaku)
        if row >= 1 and col >= 1:
            cost_sub = matrix[row - 1][col - 1] + substitution_cost(root1[row - 1], root2[col - 1])
            if math.isclose(current_val, cost_sub, abs_tol=EPSILON):
                mutations.append(f"{root1[row - 1]}:{root2[col - 1]}")
                row -= 1
                col -= 1
                continue

        # 3. WARUNEK USUNIĘCIA (Deletion)
        if row >= 1:
            cost_del = matrix[row - 1][col] + DELETION_COST
            if math.isclose(current_val, cost_del, abs_tol=EPSILON):
                mutations.append(f"-{root1[row - 1]}")
                row -= 1
                continue

        # 4. WARUNEK WSTAWIENIA (Insertion)
        if col >= 1:
            cost_ins = matrix[row][col - 1] + INSERTION_COST
            if math.isclose(current_val, cost_ins, abs_tol=EPSILON):
                mutations.append(f"+{root2[col - 1]}")
                col -= 1
                continue

        # Zabezpieczenie przed pętlą nieskończoną w przypadku błędu macierzy
        raise ValueError(f"Nie udało się odtworzyć kroku dla współrzędnych ({row}, {col}).")

    mutations.reverse()
    return mutations

pool = sorted(POOL)
random.shuffle(pool)
subpool = pool[:5]

for root1 in subpool:
    for root2 in subpool:
        matrix = levenshtein_matrix(root1, root2)
        mutations = get_mutations(root1, root2, matrix)
        print(f'{root1:5s}:{root2:5s} = {matrix[-1][-1]:2.3f} | {mutations}')