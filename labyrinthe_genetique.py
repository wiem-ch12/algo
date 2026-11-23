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


def solve_maze_ga():
    maze = [
        [0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 1, 0, 1, 1, 1, 1],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
        [0, 0, 1, 1, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 1, 1],
        [0, 1, 0, 1, 0, 1, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 1, 0, 0, 0, 0]
    ]
    start = (0, 0)
    end = (9, 9)
    moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    names = ["D", "B", "G", "H"]
    max_steps = 100

    def evaluate(chromosome):
        position = start
        visited = {position}
        valid_steps = 0
        for gene in chromosome:
            dr, dc = moves[gene]
            nxt = (position[0] + dr, position[1] + dc)
            if not (0 <= nxt[0] < 10 and 0 <= nxt[1] < 10):
                break
            if maze[nxt[0]][nxt[1]] == 1 or nxt in visited:
                break
            position = nxt
            visited.add(position)
            valid_steps += 1
            if position == end:
                return 10000 - valid_steps
        distance = abs(position[0] - end[0]) + abs(position[1] - end[1])
        return valid_steps * 2 - distance * 8 + len(visited) * 0.1

    def crossover(a, b):
        point = random.randint(1, max_steps - 1)
        return a[:point] + b[point:], b[:point] + a[point:]

    def mutation(chromosome):
        child = chromosome[:]
        for _ in range(random.randint(1, 4)):
            i = random.randrange(max_steps)
            child[i] = random.randrange(4)
        return child

    population = [[random.randrange(4) for _ in range(max_steps)] for _ in range(250)]
    best = genetic_algorithm(population, evaluate, crossover, mutation, 1200, 0.85, 4)
    position = start
    path = [position]
    visited = {position}
    for gene in best:
        dr, dc = moves[gene]
        nxt = (position[0] + dr, position[1] + dc)
        if not (0 <= nxt[0] < 10 and 0 <= nxt[1] < 10):
            break
        if maze[nxt[0]][nxt[1]] == 1 or nxt in visited:
            break
        position = nxt
        path.append(position)
        visited.add(position)
        if position == end:
            break
    print("Exercice 1 - Labyrinthe")
    print("Chemin :", [(r + 1, c + 1) for r, c in path])
    print("Sortie atteinte :", position == end)
    print("Fitness :", evaluate(best))


if __name__ == "__main__":
    solve_maze_ga()
