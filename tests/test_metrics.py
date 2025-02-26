import pytest
import numpy as np

import fmskill.metrics as mtr


def test_nse_optimal():

    np.random.seed(42)
    obs = np.random.uniform(size=100)

    assert mtr.nash_sutcliffe_efficiency(obs, obs) == 1.0


def test_nse_suboptimal():

    obs = np.array([1.0, 0.5, 0])
    mod = np.array([1.0, 0.0, 0.5])

    assert mtr.nash_sutcliffe_efficiency(obs, mod) == 0.0


def test_mef_suboptimal():

    obs = np.array([1.0, 0.5, 0])
    mod = np.array([1.0, 0.0, 0.5])

    assert mtr.model_efficiency_factor(obs, mod) > 0.0
    assert mtr.model_efficiency_factor(obs, mod) == (
        1 - np.sqrt(mtr.nash_sutcliffe_efficiency(obs, mod))
    )


def test_bias():
    obs = np.arange(100)
    mod = obs + 1.0

    assert mtr.bias(obs, mod) == 1.0


def test_rmse():
    obs = np.arange(100)
    mod = obs + 1.0

    rmse = mtr.root_mean_squared_error(obs, mod)
    assert rmse == 1.0

    rmse = mtr.root_mean_squared_error(obs, mod, weights=obs)
    assert rmse == 1.0

    rmse = mtr.root_mean_squared_error(obs, mod, unbiased=True)
    assert rmse == 0.0


def test_mae():
    obs = np.arange(100)
    mod = obs + 1.0

    mae = mtr.mean_absolute_error(obs, mod)

    assert mae == 1.0


def test_corrcoef():

    obs = np.arange(100)
    mod = obs + 1.0

    r = mtr.corrcoef(obs, mod)
    assert -1.0 <= r <= 1.0

    r = mtr.corrcoef(obs, mod, weights=obs)
    assert -1.0 <= r <= 1.0


def test_scatter_index():

    obs = np.arange(100)
    mod = obs + 1.0

    si = mtr.scatter_index(obs, mod)

    assert si >= 0.0


def test_r2():

    obs = np.arange(100)
    mod = obs + 1.0

    res = mtr.r2(obs, mod)
    assert np.isscalar(res)
    assert 0.0 <= res <= 1.0


def test_mape():

    obs = np.arange(1, 100)
    mod = obs + 1.0

    res = mtr.mean_absolute_percentage_error(obs, mod)
    assert np.isscalar(res)
    assert 0.0 <= res <= 100.0

    obs = np.ones(10)
    obs[5] = 0.0  # MAPE does not like zeros
    mod = obs + 1.0

    with pytest.warns(
        UserWarning,
        match="Observation is zero, consider to use another metric than MAPE",
    ):
        res = mtr.mean_absolute_percentage_error(obs, mod)

    assert np.isnan(res)


def test_max_error():
    obs = np.array([1.0, 0.5, 0])
    mod = np.array([1.0, 0.0, 0.5])

    assert mtr.max_error(obs, mod) == 0.5


def test_willmott():
    obs = np.array([1.0, 0.5, 0])  # mean 0.5
    mod = np.array([1.0, 0.0, 0.5])  # mean 0.5

    assert mtr.willmott(obs, mod) == pytest.approx(1 - 0.5 / 1.5)
