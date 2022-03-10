import numpy as np
import matplotlib.pyplot as plt
import imageio
from random import randint

# Constantes
Nx = Ny = 50
Largura = 1

# Valores iniciais | Padrão de teste: U0 = 2 & V0 = 1 -> Pisca
# U0 = V0 = 1 -> Fica variando as piscadas entre horizontal e vertical
u0 = 1
v0 = 2

t = 0
t_max = 20
dt = 0.1
ds = 1

# a = 1, b = 3
a = 1
b = 1.7

# Constantes dos reagentes e da estabilidade
Du = 0.1
Dv = 1
ku = Du * dt / (ds ** 2)
kv = Dv * dt / (ds ** 2)

# Constantes para gerar o Gif
gif_passo_total = 0  # Intervalo de tempo entre imagens
gif_passo_inicial = 0  # Inicializador
figura = 1  # Nome das figuras
fig_names = []  # Armazenando nome das figuras
fig_atual = 0  # Figura atual
fig_total = t_max / dt  # Quantia de figuras
size = Nx - 1  # Tamanho do range
plot_start = 0   # Começa a plotar a partir deste tempo


# Pedaço da equação sem derivada parcial
def f(u, v):
    return a - (b + 1) * u + u * u * v


# Pedaço da equação sem derivada parcial
def g(u, v):
    return b * u - u * u * v


# vetores no tempo n
u_n = np.zeros((Nx, Ny))
v_n = np.zeros((Nx, Ny))

# vetores no tempo n+1
u_n1 = np.zeros((Nx, Ny))
v_n1 = np.zeros((Nx, Ny))

# Condicoes novas

"""
Esta parte você pode tirar as aspas para gerar uma condição inicial desejada, se quiser pode ativar todas.
A mais interessante na minha opinião é a condição em uma posição aleatória.
"""

# Condição em formato de cruz (U0)
"""
for i in range(Largura):
    # Meio
    u_n[int(Nx / 2), int(Ny / 2)] = u0

    # Laterais
    #       X                   Y
    u_n[int(Nx / 2) + 1, int(Ny / 2)] = u0
    u_n[int(Nx / 2) - 1, int(Ny / 2)] = u0

    # Alturas
    #       X                   Y
    u_n[int(Nx / 2), int(Ny / 2) + 1] = u0
    u_n[int(Nx / 2), int(Ny / 2) - 1] = u0
"""

# Bordas (V0)
"""for i in range(Largura):
    # Sup Esq
    v_n[0, 0] = v0

    # Sup Dir
    v_n[0, Nx - 1] = v0

    # Inf Esq
    v_n[Nx - 1, 0] = v0

    # Inf Dir
    v_n[Nx - 1, Nx - 1] = v0"""

# Aleatório, 10 lugares
"""
for _ in range(randint(int(Nx / 5), Nx)):
    u_n[randint(0, size), randint(0, size)] = u0
for _ in range(randint(int(Nx / 5), Nx)):
    v_n[randint(0, size), randint(0, size)] = v0
"""

"""
meio len/2
meio + lateral = len/2 + len/4
"""

# Nove pontos centrais (u0)
mid = int(Nx / 2)  # Centro
mov = int(Nx / 4)  # Movendo para cima e para os lados

u_n[mid, mid] = u_n[mid + mov, mid + mov] = u_n[mid + mov, mid] = u_n[mid, mid + mov] = u_n[mid + mov, mid - mov] = u0
u_n[mid - mov, mid - mov] = u_n[mid - mov, mid] = u_n[mid, mid - mov] = u_n[mid - mov, mid + mov] = u0

# Toda a borda (v0)
for i in range(Nx):
    v_n[0, i] = v0
    v_n[i, 0] = v0
    v_n[Nx - 1, i] = v0
    v_n[i, Nx - 1] = v0

# Criando listas separadas para plotar os gráficos.
lista_pu = []
lista_pv = []

# Algumas listas são extras, não precisam realmente estar ali, estão apenas para organização.
lista_t = []
lista_u = []
lista_v = []
lista_indices = []
indice = 0

# Plot de concentração de Nx , Ny
lista_mesh_u = np.zeros((Nx, Ny))
lista_mesh_v = np.zeros((Nx, Ny))

# Calculando concentrações com FTCS
while t < t_max:

    for i in range(Nx):
        i_e = (i - 1) % Nx  # vizinho a esquerda de 0 é o da ultima posicao
        i_d = (i + 1) % Nx  # vizinho a direita da ultima posicao é o zero

        for j in range(Ny):
            j_e = (j - 1) % Ny
            j_d = (j + 1) % Ny

            u_n1[i, j] = u_n[i, j] + dt * f(u_n[i, j], v_n[i, j]) \
                         + ku * (u_n[i_e, j] + u_n[i_d, j] + u_n[i, j_e] + u_n[i, j_d] - 4 * u_n[i, j])
            v_n1[i, j] = v_n[i, j] + dt * g(u_n[i, j], v_n[i, j]) \
                         + kv * (v_n[i_e, j] + v_n[i_d, j] + v_n[i, j_e] + v_n[i, j_d] - 4 * v_n[i, j])

            # Lista i, j

            lista_mesh_u[i, j] = u_n1[i, j]
            lista_mesh_v[i, j] = v_n1[i, j]

    lista_u.append(u_n1[0][0])
    lista_v.append(v_n1[0][0])

    # atualizar u_n e v_n
    for i in range(Nx):
        for j in range(Ny):
            u_n[i, j] = u_n1[i, j]
            v_n[i, j] = v_n1[i, j]

    """    # Criar o Gif, caso não queira o gif, apenas apague esta parte
    if t > plot_start:
        if gif_passo_inicial >= gif_passo_total:
            gif_passo_inicial = 0
            plt.imshow(lista_mesh_u, interpolation='none')
            plt.title(f'$u_0$ = {u0} | $v_0$ = {v0} | a = {a} | b = {b} | t: {round(t, 1)}s')

            # Para funcionar você deve colocar onde será salvo as imagens geradas para o gif.
            plt.savefig(f'C:/Users/ericn/PycharmProjects/MetCompC/Brusselator/Figuras/{figura}.png')
            fig_names.append(f'C:/Users/ericn/PycharmProjects/MetCompC/Brusselator/Figuras/{figura}.png')
            fig_atual = figura
            print(f'{round(fig_atual / fig_total * 100, 4)}%')"""

    # Para fazer outro plot
    if gif_passo_inicial > gif_passo_total:
        lista_indices.append(indice)

    indice += 1
    gif_passo_inicial += dt

    figura += 1

    t += dt
    lista_t.append(t)

    print(f'{round(t / t_max * 100, 3)}%')

with imageio.get_writer('BrusselatorGif.gif', mode='I') as writer:
    print('Gifando')
    for filename in fig_names:
        image = imageio.imread(filename)
        writer.append_data(image)

# Plotar UxT animado
nome_plot = []
mistura = [lista_u[i] + lista_v[i] for i in range(len(lista_t))]
for i in lista_indices:
    plt.plot(lista_t, mistura, color='green', label='C')
    plt.plot(lista_t, lista_u, color='red', label='u')
    plt.plot(lista_t, lista_v, color='blue', label='v')
    plt.scatter(lista_t[i], lista_u[i] + lista_v[i], color='black')
    plt.xlabel('tempo')
    plt.ylabel('concentração')
    plt.title(f'Taxa de variação das concentrações. t = {round(lista_t[i], 2)}')
    plt.xticks([i for i in range(0, t_max+1, 5)])
    plt.legend()
    plt.grid(True)
    plt.savefig(f'C:/Users/ericn/PycharmProjects/MetCompC/Brusselator/PlotUT/{i}.png')
    nome_plot.append(f'C:/Users/ericn/PycharmProjects/MetCompC/Brusselator/PlotUT/{i}.png')
    plt.cla()
    print(f'{round(i/lista_indices[-1]*100, 3)}%')


with imageio.get_writer('BrusselatorUTGif.gif', mode='I') as writer:
    print('Gifando')
    for filename in nome_plot:
        image = imageio.imread(filename)
        writer.append_data(image)
