from __future__ import annotations

import numpy as np
import pytest
from typing import Any

import sys

# TODO(gen740): Remove the following `if` block after torch supports Python 3.13
if sys.version_info <= (3, 12):
    import torch
    from optuna._gp.gp import _fit_kernel_params
    from optuna._gp.gp import KernelParamsTensor
    import optuna._gp.prior as prior
else:
    torch: Any = None
    _fit_kernel_params: Any = None
    KernelParamsTensor: Any = None
    prior: Any = None

pytestmark = pytest.mark.use_torch

@pytest.mark.parametrize(
    "X, Y, is_categorical",
    [
        (
            np.array([[0.1, 0.2], [0.2, 0.3], [0.3, 0.1]]),
            np.array([1.0, 2.0, 3.0]),
            np.array([False, False]),
        ),
        (
            np.array([[0.1, 0.2, 0.0], [0.2, 0.3, 1.0]]),
            np.array([1.0, 2.0]),
            np.array([False, False, True]),
        ),
        (np.array([[1.0, 0.0], [0.0, 1.0]]), np.array([1.0, 2.0]), np.array([True, True])),
        (np.array([[0.0]]), np.array([0.0]), np.array([True])),
        (np.array([[0.0]]), np.array([0.0]), np.array([False])),
    ],
)
@pytest.mark.parametrize("deterministic_objective", [True, False])
@pytest.mark.parametrize("torch_set_grad_enabled", [True, False])
def test_fit_kernel_params(
    X: np.ndarray,
    Y: np.ndarray,
    is_categorical: np.ndarray,
    deterministic_objective: bool,
    torch_set_grad_enabled: bool,
) -> None:
    with torch.set_grad_enabled(torch_set_grad_enabled):
        log_prior = prior.default_log_prior
        minimum_noise = prior.DEFAULT_MINIMUM_NOISE_VAR
        initial_kernel_params = KernelParamsTensor(
            inverse_squared_lengthscales=torch.ones(X.shape[1], dtype=torch.float64),
            kernel_scale=torch.tensor(1.0, dtype=torch.float64),
            noise_var=torch.tensor(1.0, dtype=torch.float64),
        )
        gtol: float = 1e-2

        kernel_params = _fit_kernel_params(
            X=X,
            Y=Y,
            is_categorical=is_categorical,
            log_prior=log_prior,
            minimum_noise=minimum_noise,
            initial_kernel_params=initial_kernel_params,
            deterministic_objective=deterministic_objective,
            gtol=gtol,
        )

        assert (
            (
                kernel_params.inverse_squared_lengthscales
                != initial_kernel_params.inverse_squared_lengthscales
            ).sum()
            + (kernel_params.kernel_scale != initial_kernel_params.kernel_scale).sum()
            + (kernel_params.noise_var != initial_kernel_params.noise_var).sum()
        )
