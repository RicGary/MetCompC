import numpy as np
import matplotlib.pyplot as plt
import imageio
from random import randint

# Constantes
Nx = Ny = 25

# Valores iniciais | Padrão de teste: U0 = 2 & V0 = 1 -> Pisca
# U0 = V0 = 1 -> Fica variando as piscadas entre horizontal e vertical
u0 = 1
v0 = 2

t = 0
t_max = 40
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

# Algumas listas são extras, não precisam realmente estar ali, estão apenas para organização.
lista_t = []
lista_u = []
lista_v = []

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

    lista_u.append(u_n1[0][0])
    lista_v.append(v_n1[0][0])

    # atualizar u_n e v_n
    for i in range(Nx):
        for j in range(Ny):
            u_n[i, j] = u_n1[i, j]
            v_n[i, j] = v_n1[i, j]

    t += dt
    lista_t.append(t)

    print(f'{round(t / t_max * 100, 3)}%')

max_u = max(lista_u)
indice = lista_u.index(max_u)
min_v = min(lista_v)
indice_v = lista_v.index(min_v)

plt.plot(lista_t, lista_u, color='red', label='u(t)')
plt.plot(lista_t, lista_v, color='blue', label='v(t)')
plt.grid(True)
plt.suptitle(f'Reação-Difusão')
plt.title(f'$u_0$ = {u0} | $v_0$ = {v0} | a = {a} | b = {b}')
plt.xlabel('Tempo')
plt.ylabel('Concentrações')
plt.legend()
plt.savefig('Reação-Difusão')
plt.show()

plt.plot(lista_u, lista_v, color='darkviolet')
plt.xlabel('u')
plt.ylabel('v')
plt.suptitle('Diagrama de fase')
plt.title(f'$u_0$ = {u0} | $v_0$ = {v0} | a = {a} | b = {b}')
plt.grid(True)
plt.savefig('DiagramaDeFase')
plt.show()
