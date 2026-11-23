import random

# DONNÉES DU PROBLÈME , Format: (Valeur, Poids)
OBJETS = [
    (10, 4), (4, 12), (2, 1), (1, 1), (2, 2),
    (5, 3), (8, 6), (3, 2), (7, 5), (6, 4),
    (12, 8), (9, 7), (4, 3), (15, 9), (5, 2),
    (2, 1), (11, 6), (6, 3), (8, 4), (3, 1)
]
CAPACITE_SAC = 15
N_OBJETS = len(OBJETS)


def evaluer_sac(solution):
    poids_total = 0
    valeur_totale = 0
    for i in range(N_OBJETS):
        if solution[i] == 1:
            poids_total += OBJETS[i][1]
            valeur_totale += OBJETS[i][0]
    if poids_total > CAPACITE_SAC:
        depassement = poids_total - CAPACITE_SAC
        return valeur_totale - (depassement * 10)
    return valeur_totale


def poids_solution(solution):
    return sum(OBJETS[i][1] for i in range(N_OBJETS) if solution[i] == 1)


def selection_roulette(population):
    fitness = [max(0, evaluer_sac(ind)) for ind in population]
    total_fitness = sum(fitness)

    if total_fitness == 0:
        return random.sample(population, len(population))

    probabilites = []
    cumul = 0
    for f in fitness:
        cumul += f
        probabilites.append(cumul / total_fitness)

    selectionnes = []
    for _ in range(len(population)):
        r = random.random()
        for i, p in enumerate(probabilites):
            if r <= p:
                selectionnes.append(population[i])
                break
    return selectionnes


def croisement_simple(p1, p2):
    point = random.randint(1, N_OBJETS - 1)
    enfant1 = p1[:point] + p2[point:]
    enfant2 = p2[:point] + p1[point:]
    return enfant1, enfant2


def mutation_transposition_quelconque(solution, taux_mutation=0.05):
    if random.random() < taux_mutation:
        i, j = random.sample(range(N_OBJETS), 2)
        solution[i], solution[j] = solution[j], solution[i]
    return solution


def algorithme_genetique_sac(pop_size=100, generations=200):
    population = [[random.randint(0, 1) for _ in range(N_OBJETS)] for _ in range(pop_size)]

    for _ in range(generations):
        selectionnes = selection_roulette(population)
        nouvelle_pop = []
        for i in range(0, pop_size, 2):
            p1 = selectionnes[i]
            p2 = selectionnes[(i + 1) % pop_size]
            enfant1, enfant2 = croisement_simple(p1, p2)
            enfant1 = mutation_transposition_quelconque(enfant1)
            enfant2 = mutation_transposition_quelconque(enfant2)
            nouvelle_pop.extend([enfant1, enfant2])
        population = nouvelle_pop[:pop_size]

    solutions_valides = [ind for ind in population if poids_solution(ind) <= CAPACITE_SAC]
    if not solutions_valides:
        return [0] * N_OBJETS, 0  # Sécurité
    meilleure_solution = max(solutions_valides, key=evaluer_sac)
    return meilleure_solution, evaluer_sac(meilleure_solution)


if __name__ == "__main__":
    print("=== SAC À DOS - ALGORITHME GÉNÉTIQUE ===")
    print("Méthodes utilisées :")
    print("- Sélection : Roulette")
    print("- Croisement : Simple (1 point)")
    print("- Mutation : Transposition de deux allèles quelconques")
    sol, val = algorithme_genetique_sac()
    poids = poids_solution(sol)
    print(f"\nMeilleure solution trouvée : {sol}")
    print(f"Valeur maximale            : {val}")
    print(f"Poids total utilisé        : {poids} / {CAPACITE_SAC} kg")
    print(f"Solution valide ?          : {'OUI' if poids <= CAPACITE_SAC else 'NON'}")