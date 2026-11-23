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


def solve_tokens_ga(n=5, k=10):
    cells = n * n

    def create_individual():
        chosen = random.sample(range(cells), k)
        return set(chosen)

    def fitness(individual):
        rows = [0] * n
        cols = [0] * n
        for cell in individual:
            r, c = divmod(cell, n)
            rows[r] += 1
            cols[c] += 1
        odd = sum(x % 2 for x in rows) + sum(x % 2 for x in cols)
        return -odd

    def crossover(a, b):
        union = list(a | b)
        random.shuffle(union)
        child1 = set(union[:k])
        union2 = list(a | b)
        random.shuffle(union2)
        child2 = set(union2[:k])
        return child1, child2

    def mutation(individual):
        child = set(individual)
        if random.random() < 0.8:
            occupied = list(child)
            free = list(set(range(cells)) - child)
            if occupied and free:
                child.remove(random.choice(occupied))
                child.add(random.choice(free))
        return child

    population = [create_individual() for _ in range(200)]
    best = genetic_algorithm(population, fitness, crossover, mutation, 1000, 0.85, 4)
    board = [[0] * n for _ in range(n)]
    for cell in best:
        r, c = divmod(cell, n)
        board[r][c] = 1
    print("Exercice 2 - Jetons")
    for row in board:
        print(row)
    print("Fitness :", fitness(best))
    print("Solution faisable :", fitness(best) == 0)


if __name__ == "__main__":
    solve_tokens_ga()
