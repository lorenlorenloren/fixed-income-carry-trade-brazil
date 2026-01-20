import numpy as np
from scipy.optimize import minimize


def nss_yield(maturities, params):
    """
    Nelson-Siegel-Svensson zero-coupon yield curve.

    params = (beta0, beta1, beta2, beta3, tau1, tau2)
    """
    beta0, beta1, beta2, beta3, tau1, tau2 = params
    m = np.array(maturities, dtype=float)

    def _component(m, tau):
        x = m / tau
        return (1 - np.exp(-x)) / x

    c1 = _component(m, tau1)
    c2 = c1 - np.exp(-m / tau1)
    c3 = _component(m, tau2) - np.exp(-m / tau2)

    return beta0 + beta1 * c1 + beta2 * c2 + beta3 * c3


def _nss_rmse(params, maturities, yields):
    model = nss_yield(maturities, params)
    return np.sqrt(np.mean((model - yields) ** 2))


def fit_nss_curve(maturities, yields):
    """
    Fit NSS parameters by minimizing RMSE.
    """
    maturities = np.asarray(maturities, dtype=float)
    yields = np.asarray(yields, dtype=float)

    x0 = np.array([yields.mean(), -1.0, 1.0, 0.5, 1.0, 5.0])

    bounds = [
        (None, None),  # beta0
        (None, None),  # beta1
        (None, None),  # beta2
        (None, None),  # beta3
        (1e-3, None),  # tau1
        (1e-3, None),  # tau2
    ]

    res = minimize(
        _nss_rmse,
        x0,
        args=(maturities, yields),
        bounds=bounds,
        method="L-BFGS-B",
    )

    return res.x, _nss_rmse(res.x, maturities, yields)
