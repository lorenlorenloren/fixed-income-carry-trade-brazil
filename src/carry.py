import numpy as np


def compute_spreads_stats(maturities, y_br, y_us):
    spread = y_br - y_us
    return {
        "mean": float(spread.mean()),
        "min": float(spread.min()),
        "max": float(spread.max()),
        "std": float(spread.std()),
    }


def compute_real_carry_10y(curve_br, curve_us, infl_br=0.055, infl_us=0.025):
    """
    Approximate real carry BR vs US at ~10Y maturity.
    """
    m = curve_br["maturity"].values
    y_br = curve_br["yield"].values
    y_us = curve_us["yield"].values

    idx_br = np.argmin(np.abs(m - 10.0))
    idx_us = np.argmin(np.abs(curve_us["maturity"].values - 10.0))

    real_br = y_br[idx_br] - infl_br
    real_us = curve_us["yield"].values[idx_us] - infl_us

    return float(real_br - real_us)
