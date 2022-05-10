import numpy as np
import matplotlib.pyplot as plt

"""
Previsão do valor de mercado MAGLU3

Data inicial: 02/01/2019
Data final: 19/04/2022
"""

Untreated = []

# Data original
OriginalDate = []
# Colocando o Valor do final do dia.
OriginalStockPrice = []

"""
Coluna | Significado
0      | Data
1      | Hora
2      | Open
3      | High
4      | Low
5      | Close
6      | Volume
"""

with open('STOCK.csv', 'r', encoding='utf8') as f:
    for line in f:
        Untreated.append(line.split(','))

Untreated.pop(0)

for i in Untreated:
    """
    Open = float(i[1])
    High = float(i[2])
    Low = float(i[3])
    """
    Close = float(i[4])

    OriginalDate.append(i[0][0:9])
    OriginalStockPrice.append(Close)

# Data para monte carlo
Date = OriginalDate[0:int(len(OriginalDate) / 2)]
# Stock final do dia monte carlo
StockPrice = OriginalStockPrice[0:int(len(OriginalDate) / 2)]

mean = np.nanmean(StockPrice)
std = np.nanstd(StockPrice)
var = np.nanstd(StockPrice) ** 2

#######################

# Stochastic Differential Equation (SDE):
# dS(t) = mu S(t) dt + sigma S(t) dW(t)

# Explicit Expression:
# S(t) = S0 exp( (mu - sigma^2/2) t + sigma W(t) )


######## Cte's ########

# drift coefficent
mu = mean - 0.5 * var
# number of steps
n = 100
# time in years
T = 1
# number of sims
M = 500
# initial stock price
S0 = StockPrice[-1]
# volatility
sigma = 0.3

######## Simulating GBM Paths ########

# calc each time step
dt = T / n

# simulation using numpy arrays
St = np.exp(
    (mu - sigma ** 2 / 2) * dt
    + sigma * np.random.normal(0, np.sqrt(dt), size=(M, n)).T
)

# include array of 1's
St = np.vstack([np.ones(M), St])

# multiply through by S0 and return the cumulative product of elements along a given simulation path (axis=0).
St = S0 * St.cumprod(axis=0)

######## Consider time intervals in years. ########

# Define time interval correctly
time = np.linspace(0, T, n + 1)

# Require numpy array that is the same shape as St
tt = np.full(shape=(M, n + 1), fill_value=time).T


######## Plotting. ########

def OriginalPlot(graph=False):
    plt.figure(figsize=(19, 10))
    Date_in_slice = np.linspace(0, 2, num=len(OriginalDate))
    plt.plot(Date_in_slice, OriginalStockPrice)
    plt.title(f'MGLU3 - 2 Years.\nStart: {OriginalDate[0]}\nEnd: {OriginalDate[-1]}')
    plt.xticks([0, 1, 2], [Date[0], Date[int(len(Date) / 2)], Date[-1]])
    plt.xlabel('Date')
    plt.ylabel('Stock Price R$')
    plt.vlines(1, 0, 60, colors='black')
    plt.ylim(0, 50)
    plt.savefig("1OriginalPlot.jpeg")
    if graph:
        plt.show()


def FinalPlot(graph=False):
    plt.figure(figsize=(19, 10))
    Date_in_slice = np.linspace(-1, 0, num=int(len(OriginalDate) / 2))
    plt.plot(Date_in_slice, StockPrice)

    plt.plot(tt, St)
    plt.xlabel("Date")
    plt.ylabel("Stock Price $(S_t)$ R\$")

    plt.xticks([-1, 0, 1], [Date[0], Date[int(len(Date) / 2)], Date[-1]])

    # "Realizations of Geometric Brownian Motion for Stock Price $dS_t = \mu S_t dt + \sigma S_t dW_t$\n $S_0 = R${0}, \mu = {1}, \sigma = {2}$"
    # $ for itallic, \sigma, \mu

    plt.title(f"Realizations of Geometric Brownian Motion for Stock Price\n"
              f"$dS_t = \mu S_t dt + \sigma S_t dW_t$\n"
              f"$S\u2080$ = {StockPrice[-1]:.2f}   $\u03BC$ = {mu:.2f}   \u03C3 = {sigma}")
    plt.ylim(0, 50)
    plt.vlines(0, 0, 60, colors='black')
    plt.savefig('2SimulationPlot.jpeg')

    if graph:
        plt.show()


OriginalPlot()
FinalPlot()
