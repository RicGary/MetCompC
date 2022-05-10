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

with open('../STOCK.csv', 'r', encoding='utf8') as f:
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
Date = OriginalDate[0:int(len(OriginalDate)/2)]
# Stock final do dia monte carlo
StockPrice = OriginalStockPrice[0:int(len(OriginalDate)/2)]


# Gráfico completo para comparação.
def OriginalPlot():
    Date_in_slice = np.linspace(0, 2, num=len(OriginalDate))
    plt.plot(Date_in_slice, OriginalStockPrice)
    plt.title(f'MGLU3 - 2 Anos.\nInício: {OriginalDate[0]}\nFim: {OriginalDate[-1]}')
    plt.xlabel('Anos')
    plt.ylabel('Preço')
    plt.vlines(1, min(OriginalStockPrice), max(OriginalStockPrice), colors='black')
    plt.show()


# Metade do plot
def PlotMiddle(show=True):
    Date_in_slice = np.linspace(0, 1, num=int(len(OriginalDate)/2))
    plt.plot(Date_in_slice, StockPrice)
    plt.xlim(0, 2)
    if show:
        plt.show()


# Starting Monte Carlo SiM

mean = np.nanmean(StockPrice)
std = np.nanstd(StockPrice)
var = np.nanstd(StockPrice)**2

# Drift OK
drift = mean - 0.5 * var

# Generate Data
StockForecast = []

actual_price = StockPrice[-1]
for i in range(len(OriginalStockPrice)-len(StockPrice)):

    future_price = actual_price * np.exp(drift + std * np.random.normal(0, 1))
    StockForecast.append(future_price)
    actual_price = future_price

print(drift, var, StockPrice[-1])
