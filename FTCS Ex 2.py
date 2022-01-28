"""
Exemplo 2 da aula.

Não está em forma de função pois pretendo unificar os FTSC.
"""
import matplotlib.pyplot as plt

CORES = ('red', 'lime', 'blue',
         'magenta', 'cyan', 'yellow',
         'black', 'orchid', 'gold', 'crimson')

L = 50

k = 0.25

TMAX = [0, 10, 50, 100, 500, 1000]

x = [i for i in range(L)]

for cor, tmax in enumerate(TMAX):

    f = [0 for _ in range(L)]
    g = [0 for _ in range(L)]

    m1 = int(L/4)
    m2 = int(3*L/4)

    for i in range(m1, m2 + 1):
        f[i] = 1

    tempo = 0
    while tempo < tmax:

        for i in range(1, L - 1):
            g[i] = f[i] + k * (f[i - 1] - 2 * f[i] + f[i + 1])

        for i in range(1, L - 1):
            f[i] = g[i]

        # D = 1
        tempo += 0.25

    print(f)

    plt.plot(x, f, color=CORES[cor], label=tmax)
plt.title(f'Foward Time Central Space (FTCS) || L = {L} , k = {k}')
plt.xlabel('x')
plt.ylabel('f(x,t)')
plt.legend()
plt.show()
