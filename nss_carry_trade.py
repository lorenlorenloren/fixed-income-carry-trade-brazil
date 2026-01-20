#!/usr/bin/env python
"""
Main script: NSS + BR-US carry trade + bond options (Black-76) + summary.
"""

import numpy as np
import pandas as pd
from pathlib import Path

from src.nss_model import fit_nss_curve, nss_yield
from src.carry import compute_spreads_stats, compute_real_carry_10y
from src.options import price_bond_option_black76
from src.utils import load_yield_data, save_summary_json


DATA_DIR = Path("data")
RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)


def main():
    # 1) Load data
    us = load_yield_data(DATA_DIR / "yields_us_jan2026.csv")
    br = load_yield_data(DATA_DIR / "yields_br_jan2026.csv")

    # 2) Fit NSS for US and BR
    params_us, rmse_us = fit_nss_curve(us["maturity"].values, us["yield"].values)
    params_br, rmse_br = fit_nss_curve(br["maturity"].values, br["yield"].values)

    # 3) Spread and carry analysis
    maturities = br["maturity"].values
    y_us_fit = nss_yield(maturities, params_us)
    y_br_fit = nss_yield(maturities, params_br)

    spread_stats = compute_spreads_stats(maturities, y_br_fit, y_us_fit)
    real_carry_10y = compute_real_carry_10y(br, us)

    # 4) Example bond option pricing (10Y BR)
    F_10y_br = float(y_br_fit[np.argmin(np.abs(maturities - 10.0))])
    K_atm = F_10y_br
    T = 1.0
    r = F_10y_br
    sigma_y = 0.15

    call_price = price_bond_option_black76(F_10y_br, K_atm, T, r, sigma_y, call=True)
    put_price = price_bond_option_black76(F_10y_br, K_atm, T, r, sigma_y, call=False)

    # 5) Build summary dict
    summary = {
        "analysis_date": "2026-01-20",
        "nss_us_rmse": rmse_us,
        "nss_br_rmse": rmse_br,
        "spread_stats": spread_stats,
        "real_carry_10y_br": real_carry_10y,
        "bond_call_10y_br_1y": call_price,
        "bond_put_10y_br_1y": put_price,
    }

    save_summary_json(summary, RESULTS_DIR / "summary_20jan2026.json")

    print("\n================ EXECUTION SUMMARY ================")
    print(f"Analysis date............... {summary['analysis_date']}")
    print(f"NSS US RMSE................. {rmse_us:.4%}")
    print(f"NSS BR RMSE................. {rmse_br:.4%}")
    print(f"BR-US Spread Mean........... {spread_stats['mean']:.2%}")
    print(f"Real Carry Brazil 10Y....... {real_carry_10y:.2%}")
    print(f"Bond Call (10Y BR, 1Y).....  {call_price:.4f}")
    print(f"Bond Put  (10Y BR, 1Y).....  {put_price:.4f}")
    print("===================================================\n")


if __name__ == "__main__":
    main()
