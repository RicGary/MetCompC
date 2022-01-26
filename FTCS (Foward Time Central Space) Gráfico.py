"""
Foward Time Central Space

    j -> é o meu "x"
    n -> é o meu "t"

Lado esquerdo temos

    - Próximo ponto de f em x=j e o t=n+1

    k -> D.dt/(dx)²


Equação da difusão:

    f(x,t) = 1/(4.pi.D.t)^0.5   . exp(-x²/4.D.t)

    onde D é o coeficiênte de difusão (cte)

OBS:

de t: t1 = 0, t2 = dt, ..., tn+1 = n dt
de x: x1 = 0, x2 = dx, ..., xj+1 = j dx
de f: f.j|n = f(xj, tn)

"""

"""
Exemplo 3.1: MétodosC-Scilab - Scherer

Suponhamos que em x = 0 há uma fonte inesgotável de material que
se difunde para x > 0 a partir do instante t = 0, isto é, f(x = 0, t) = 1.
Suponhamos ainda que em x = L há um sumidouro que absorve todo
o material que lá chega, ou seja, f(L, t) = 0. Como condição inicial
supomos que f(x > 0, t = 0) = 0.
"""

"""
Solução da eq. de difisão; condições de contorno:

f(0,t) = 1
f(L,t) = 0  -> Fonte inesgotável em x = 0

sumidouro em L=x; condição inicial: f(x>0, 0) = 0 

dados: comprimento L, tmax e k = D*dt/dx**2

L = 100, tmax = 400, k = 0.4

#################################
OBS: Quando D = 1, dx = 1 -> k~dt
#################################
"""


# Calculando f no x e com t + 1

def __FTSC__(TMAX, k, L, condicoes, otimizar=False):
    """
    Código da difusão utilizando um modelo simples chamado
    Foward Time Central Space, mais conhecido como FTCS.

    No momento o código leva em média 0.19s para rodar no meu computador,
    utilizando um TMAX = (2, 10, 50, 100, 200, 1000, 2000), L = 100 e k = 0.4

    Minhas configurações de Hardware:

    Acer Aspire Nitro 5 com 8 Gb de Ram extra.
    NVidia Gforce GTX 1650, Intel Core i5 9850H, 16 RAM.

    :param TMAX: Lista ou tupla com valores do tempo máximo para plot.
    :param k: Coeficiente que depende de D, dx e dt.
    :param L: Largura total do material.
    :param condicoes: Condições de contorno (por enquanto apenas init e final)
    :param otimizar: Print o tempo que o código levou para ser executado.
    :return: Não retorna nada.
    """

    import matplotlib.pyplot as plt

    if otimizar:
        import time
        start_time = time.time()

    CORES = ('red', 'lime', 'blue',
             'magenta', 'cyan', 'yellow',
             'black', 'orchid', 'gold', 'crimson')

    f = [0 for _ in range(L)]
    g = [0 for _ in range(L)]
    x = [i for i in range(L)]

    # BC esquerda
    f[0] = condicoes[0]
    # BC direita
    f[-1] = condicoes[1]

    for cor, tmax in enumerate(TMAX):
        tempo = 0

        while tempo < tmax:

            for i in range(1, L - 1):
                g[i] = f[i] + k * (f[i - 1] - 2 * f[i] + f[i + 1])

            for i in range(1, L - 1):
                f[i] = g[i]

            # D = 1
            tempo += 0.4

        plt.plot(x, f, color=CORES[cor], label=tmax)

    if otimizar:
        print(f'{round(-start_time + time.time(), 3)}s')

    plt.title(f'Foward Time Central Space (FTCS) || L = {L} , k = {k}')
    plt.xlabel('x')
    plt.ylabel('f(x,t)')
    plt.xticks([i for i in range(0, 100, 10)])
    plt.legend()
    plt.show()


if __name__ == '__main__':
    """
    Local utilizado para testes de otimização.
    """

    TMAX = (200, )
    k = 0.4
    L = 100
    condicoes = (1, 0)

    __FTSC__(TMAX, k, L, condicoes, True)

