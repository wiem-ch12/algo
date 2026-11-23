import random
from collections import deque

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

def generer_voisins_sac(solution):
    voisins = []
    for i in range(N_OBJETS):
        voisin = solution[:]
        voisin[i] = 1 - voisin[i]
        voisins.append(voisin)
    return voisins

def tabou_sac(iterations=1000, taille_tabou=20):
    solution_actuelle = [random.randint(0, 1) for _ in range(N_OBJETS)]
    meilleure_solution = solution_actuelle[:]
    meilleure_valeur = evaluer_sac(solution_actuelle)
    tabou_list = deque(maxlen=taille_tabou)
    non_amelioration = 0

    for _ in range(iterations):
        voisins = generer_voisins_sac(solution_actuelle)
        voisins = [v for v in voisins if v not in tabou_list]
        if not voisins:
            break

        solution_actuelle = max(voisins, key=evaluer_sac)
        valeur_actuelle = evaluer_sac(solution_actuelle)
        tabou_list.append(solution_actuelle)

        if valeur_actuelle > meilleure_valeur and poids_solution(solution_actuelle) <= CAPACITE_SAC:
            meilleure_solution = solution_actuelle[:]
            meilleure_valeur = valeur_actuelle
            non_amelioration = 0
        else:
            non_amelioration += 1

        if non_amelioration > 100:
            solution_actuelle = [random.randint(0, 1) for _ in range(N_OBJETS)]
            non_amelioration = 0
            tabou_list.clear()

    return meilleure_solution, meilleure_valeur

if __name__ == "__main__":
    print("=== SAC À DOS - RECHERCHE TABOU ===")
    sol, val = tabou_sac()
    poids = poids_solution(sol)
    print(f"Meilleure solution trouvée : {sol}")
    print(f"Valeur maximale            : {val}")
    print(f"Poids total utilisé        : {poids} / {CAPACITE_SAC} kg")
    print(f"Solution valide ?          : {'OUI' if poids <= CAPACITE_SAC else 'NON'}")