import numpy as np
from src.nss_model import fit_nss_curve, nss_yield


def test_nss_fit_reduces_rmse():
    maturities = np.array([0.25, 1.0, 2.0, 5.0, 10.0])
    true_params = (0.10, -0.02, 0.01, 0.00, 1.0, 5.0)
    y_true = nss_yield(maturities, true_params)

    params_fit, rmse_fit = fit_nss_curve(maturities, y_true + 0.0001 * np.random.randn(len(maturities)))

    assert rmse_fit < 0.01
    assert len(params_fit) == 6
