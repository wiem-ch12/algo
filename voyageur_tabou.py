import math

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


def solve_tsp_tabu(iterations=2000, tabu_size=30):
    matrix = tsp_data()
    current = list(range(8))
    best = current[:]
    tabu = []
    for _ in range(iterations):
        candidates = []
        for i in range(1, 7):
            for j in range(i + 1, 8):
                candidate = current[:]
                candidate[i], candidate[j] = candidate[j], candidate[i]
                value = tsp_cost(candidate, matrix)
                move = (min(current[i], current[j]), max(current[i], current[j]))
                if math.isfinite(value) and (move not in tabu or value < tsp_cost(best, matrix)):
                    candidates.append((value, candidate, move))
        if not candidates:
            break
        value, current, move = min(candidates, key=lambda x: x[0])
        tabu.append(move)
        if len(tabu) > tabu_size:
            tabu.pop(0)
        if value < tsp_cost(best, matrix):
            best = current[:]
    print("Exercice 3 - Voyageur de commerce - Recherche taboue")
    print("Circuit :", [x + 1 for x in best] + [best[0] + 1])
    print("Coût :", tsp_cost(best, matrix))


if __name__ == "__main__":
    solve_tsp_tabu()
