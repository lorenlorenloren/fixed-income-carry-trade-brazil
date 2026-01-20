import numpy as np
from scipy.stats import norm


def price_bond_option_black76(F, K, T, r, sigma, call=True):
    """
    Black-76 option on a forward (bond) price F.
    F, K: forward and strike yield or price
    T: time to maturity (years)
    r: discount rate
    sigma: volatility
    """
    if T <= 0 or sigma <= 0:
        return max(0.0, (F - K) if call else (K - F))

    d1 = (np.log(F / K) + 0.5 * sigma ** 2 * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    df = np.exp(-r * T)

    if call:
        price = df * (F * norm.cdf(d1) - K * norm.cdf(d2))
    else:
        price = df * (K * norm.cdf(-d2) - F * norm.cdf(-d1))

    return float(price)
