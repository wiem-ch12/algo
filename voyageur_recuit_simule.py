import math
import random

def tsp_data():
    n = 8
    matrix = [[math.inf] * n for _ in range(n)]
    edges = {
        (1, 2): 14, (1, 3): 15, (1, 8): 17,
        (2, 3): 13, (2, 4): 14, (2, 5): 20, (2, 8): 21,
        (3, 4): 11, (3, 5): 21, (3, 6): 17, (3, 7): 9, (3, 8): 9,
        (4, 5): 11, (4, 6): 10, (4, 7): 8, (4, 8): 20,
        (5, 6): 15, (5, 7): 18,
        (6, 7): 9,
        (7, 8): 13
    }
    for (a, b), cost in edges.items():
        matrix[a - 1][b - 1] = cost
        matrix[b - 1][a - 1] = cost
    return matrix


def tsp_cost(tour, matrix):
    total = 0
    for i in range(len(tour)):
        cost = matrix[tour[i]][tour[(i + 1) % len(tour)]]
        if math.isinf(cost):
            return math.inf
        total += cost
    return total


def solve_tsp_annealing(iterations=5):
    matrix = tsp_data()
    current = list(range(8))
    current_cost = tsp_cost(current, matrix)
    best = current[:]
    best_cost = current_cost
    temperature = 30.0
    cooling = 0.75
    for _ in range(iterations):
        i, j = sorted(random.sample(range(1, 8), 2))
        candidate = current[:]
        candidate[i], candidate[j] = candidate[j], candidate[i]
        candidate_cost = tsp_cost(candidate, matrix)
        if math.isfinite(candidate_cost):
            difference = candidate_cost - current_cost
            if difference < 0 or random.random() < math.exp(-difference / max(temperature, 1e-9)):
                current = candidate
                current_cost = candidate_cost
                if current_cost < best_cost:
                    best = current[:]
                    best_cost = current_cost
        temperature *= cooling
    print("Exercice 3 - Voyageur de commerce - Recuit simulé")
    print("Circuit :", [x + 1 for x in best] + [best[0] + 1])
    print("Coût :", best_cost)


if __name__ == "__main__":
    solve_tsp_annealing()
