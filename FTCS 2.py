import matplotlib.pyplot as plt

L = 50
k = 0.25
TMAX = [0, 10, 50, 100, 500, 1000]

x = [i for i in range(L)]

for cor, tmax in enumerate(TMAX):

    CORES = ('red', 'lime', 'blue',
             'magenta', 'cyan', 'yellow',
             'black', 'orchid', 'gold', 'crimson')

    f = [0 for _ in range(L)]
    g = [0 for _ in range(L)]

    m1 = L//4
    m2 = 3*L//4

    f[m1:m2] = [1 for _ in range(len(f[m1:m2]))]

    tempo = 0
    while tempo < tmax:
        g[0] = f[0] + k * (f[L - 1] - 2.0 * f[0] + f[1])
        g[L - 1] = f[L - 1] + k * (f[L - 2] - 2.0 * f[L - 1] + f[0])

        for i in range(1, L-1):
            g[i] = f[i] + k * (f[i - 1] - 2.0 * f[i] + f[i + 1])

        for i in range(0, L-1):
            f[i] = g[i]

        tempo += 0.25

    plt.plot(x, f, color=CORES[cor], label=tmax)
plt.title(f'Foward Time Central Space (FTCS) || L = {L} , k = {k}')
plt.xlabel('x')
plt.ylabel('f(x,t)')
plt.legend()
plt.show()