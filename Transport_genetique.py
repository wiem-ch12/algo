# ================= Exercice 2 : Transport (Tabou) =================
import math
import random

C = [[5, 3, 4], [6, 7, 2]]          # couts D1, D2 -> M1, M2, M3
cout = lambda x: sum(C[i][j] * x[i][j] for i in range(2) for j in range(3))

x = [[4, 4, 0], [0, 1, 8]]          # solution initiale (coin Nord-Ouest)
best, bc, tabou = x, cout(x), []
for it in range(10):
    cand = None
    for j1 in range(3):
        for j2 in range(3):
            if j1 != j2 and x[0][j1] > 0 and x[1][j2] > 0:   # cycle D1/D2 x Mj1/Mj2
                y = [r[:] for r in x]
                y[0][j1] -= 1; y[0][j2] += 1; y[1][j1] += 1; y[1][j2] -= 1
                c = cout(y)
                if (j1, j2) in tabou and c >= bc: continue    # aspiration
                if cand is None or c < cand[0]: cand = (c, y, (j1, j2))
    if cand is None: break
    c, x, (j1, j2) = cand
    tabou = (tabou + [(j2, j1)])[-3:]
    if c < bc: best, bc = x, c
    print(f"it {it+1}: cout = {c} | meilleur = {bc}")
print("Ex2 -> meilleure solution :", best, "cout =", bc)

# ================= Exercice 3 : Voyageur de commerce =================
INF = 10**4
D = [[INF] * 9 for _ in range(9)]
for i, j, d in [(1,2,14),(1,3,15),(1,8,17),(2,3,13),(2,4,14),(2,5,20),(2,8,21),
                (3,4,11),(3,5,21),(3,6,17),(3,7,9),(3,8,9),(4,5,11),(4,6,10),
                (4,7,8),(4,8,20),(5,6,15),(5,7,18),(6,7,9),(7,8,13)]:
    D[i][j] = D[j][i] = d
L = lambda t: sum(D[t[k]][t[(k + 1) % 8]] for k in range(8))
inv = lambda t, i, j: t[:i] + t[i:j + 1][::-1] + t[j + 1:]       # 2-opt
show = lambda t: "-".join(map(str, t + [t[0]]))

# --- 1) Tabou ---
t = list(range(1, 9)); bt, bl, tabou = t, L(t), []
print("\nTabou, initiale", show(t), "L =", bl)
for it in range(10):
    cand = None
    for i in range(1, 7):
        for j in range(i + 1, 8):
            v = inv(t, i, j); l = L(v); mv = (t[i], t[j])
            if mv in tabou and l >= bl: continue
            if cand is None or l < cand[0]: cand = (l, v, mv)
    l, t, mv = cand
    tabou = (tabou + [mv])[-3:]
    if l < bl: bt, bl = t, l
    print(f"it {it+1}: {show(t)} L = {l} | meilleur = {bl}")
print("Ex3 Tabou ->", show(bt), "L =", bl)

# --- 2) Recuit simule (5 iterations, T <- 0.7 T) ---
random.seed(32)
t = list(range(1, 9)); l = L(t); bt, bl, T = t, l, 10
print("\nRecuit, initiale", show(t), "L =", l)
for it in range(5):
    i, j = sorted(random.sample(range(1, 8), 2))
    v = inv(t, i, j); d = L(v) - l
    p = 1 if d <= 0 else math.exp(-d / T)
    ok = random.random() < p
    if ok: t, l = v, L(v)
    if l < bl: bt, bl = t, l
    print(f"it {it+1}: T = {T:.2f} | {show(v)} | delta = {d} | p = {p:.2f} | {'accepte' if ok else 'refuse'} | L = {l}")
    T *= 0.7
print("Ex3 Recuit ->", show(bt), "L =", bl)