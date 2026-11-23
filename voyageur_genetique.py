import math
import random
import copy

def genetic_algorithm(population, fitness, crossover, mutation, generations=300, rate=0.8, elite=2):
    population = [copy.deepcopy(x) for x in population]
    best = max(population, key=fitness)
    for _ in range(generations):
        population.sort(key=fitness, reverse=True)
        if fitness(population[0]) > fitness(best):
            best = copy.deepcopy(population[0])
        new_population = [copy.deepcopy(x) for x in population[:elite]]
        while len(new_population) < len(population):
            p1 = random.choice(population[:max(2, len(population) // 2)])
            p2 = random.choice(population[:max(2, len(population) // 2)])
            if random.random() < rate:
                c1, c2 = crossover(p1, p2)
            else:
                c1, c2 = copy.deepcopy(p1), copy.deepcopy(p2)
            new_population.append(mutation(c1))
            if len(new_population) < len(population):
                new_population.append(mutation(c2))
        population = new_population
    return max([best] + population, key=fitness)


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


def solve_tsp_ga(generations=1000):
    matrix = tsp_data()

    def create_individual():
        tail = list(range(1, 8))
        random.shuffle(tail)
        return [0] + tail

    def fitness(route):
        cost = tsp_cost(route, matrix)
        return 0 if math.isinf(cost) else 1 / (1 + cost)

    def crossover(a, b):
        left, right = sorted(random.sample(range(1, 8), 2))
        child1 = [None] * 8
        child2 = [None] * 8
        child1[0] = child2[0] = 0
        child1[left:right] = a[left:right]
        child2[left:right] = b[left:right]
        fill1 = [x for x in b[1:] if x not in child1]
        fill2 = [x for x in a[1:] if x not in child2]
        p = 1
        for i in range(1, 8):
            if child1[i] is None:
                child1[i] = fill1[p - 1]
                p += 1
        p = 1
        for i in range(1, 8):
            if child2[i] is None:
                child2[i] = fill2[p - 1]
                p += 1
        return child1, child2

    def mutation(route):
        child = route[:]
        i, j = random.sample(range(1, 8), 2)
        child[i], child[j] = child[j], child[i]
        return child

    population = [create_individual() for _ in range(200)]
    best = genetic_algorithm(population, fitness, crossover, mutation, generations, 0.85, 4)
    print("Exercice 3 - Voyageur de commerce - Algorithme génétique")
    print("Circuit :", [x + 1 for x in best] + [best[0] + 1])
    print("Coût :", tsp_cost(best, matrix))


if __name__ == "__main__":
    solve_tsp_ga()
