import numpy as np
import matplotlib.pyplot as plt

# Stochastic Differential Equation (SDE):
# dS(t) = mu S(t) dt + sigma S(t) dW(t)

# Explicit Expression:
# S(t) = S0 exp( (mu - sigma^2/2) t + sigma W(t) )


######## Cte's ########

# drift coefficent // 0.1
mu = 0.02789207065791821
# number of steps // 100
n = 100
# time in years // 1
T = 1
# number of sims // 100
M = 1000
# initial stock price // 100
S0 = 21.84
# volatility // 0.3
sigma = 4.577154499212863/10

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

plt.plot(tt, St)
plt.xlabel("Years $(t)$")
plt.ylabel("Stock Price $(S_t)$")
plt.title(
    "Realizations of Geometric Brownian Motion\n $dS_t = \mu S_t dt + \sigma S_t dW_t$\n $S_0 = {0}, \mu = {1}, \sigma = {2}$".format(
        S0, mu, sigma)
)
plt.show()
