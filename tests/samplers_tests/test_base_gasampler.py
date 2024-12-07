from typing import Any
import pytest
import optuna
import random
from optuna.distributions import BaseDistribution
from optuna.samplers._random import RandomSampler
from optuna.study.study import Study
from optuna.trial import FrozenTrial

from optuna.samplers._ga._base import BaseGASampler
from unittest.mock import MagicMock, Mock, create_autospec

from optuna.trial._state import TrialState


class BaseGASAmplerTestSampler(BaseGASampler):
    def __init__(self, population_size: int):
        super().__init__(population_size=population_size)
        self._random_sampler = RandomSampler()

    def select_parent(self, study: optuna.Study, generation: int) -> list[FrozenTrial]:
        return []

    def sample_relative(
        self,
        study: optuna.Study,
        trial: FrozenTrial,
        search_space: dict[str, BaseDistribution],
    ) -> dict[str, Any]:
        return {}

    def sample_independent(
        self,
        study: Study,
        trial: FrozenTrial,
        param_name: str,
        param_distribution: BaseDistribution,
    ) -> Any:
        return self._random_sampler.sample_independent(
            study, trial, param_name, param_distribution
        )

    def infer_relative_search_space(
        self, study: Study, trial: FrozenTrial
    ) -> dict[str, BaseDistribution]:
        search_space: dict[str, BaseDistribution] = {}
        return search_space



def test_systemattr_keys():
    assert (
        BaseGASAmplerTestSampler._get_generation_key()
        == "BaseGASAmplerTestSampler:generation"
    )
    assert (
        BaseGASAmplerTestSampler._get_parent_cache_key_prefix()
        == "BaseGASAmplerTestSampler:parent:"
    )

    test_sampler = BaseGASAmplerTestSampler(population_size=42)

    assert test_sampler.population_size == 42


@pytest.mark.parametrize(
    "args",
    [
        {
            "population_size": 3,
            "trials": [],
            "generation": 0,
        },
        {
            "population_size": 4,
            "trials": [0, 0, 0, 0],
            "generation": 1,
        },
        {
            "population_size": 3,
            "trials": [0, 0, 0, 1, 1, 1, 1, 2, 2, 2],
            "generation": 3,
        },
        {
            "population_size": 3,
            "trials": [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 1, 1, 2],
            "generation": 3,
        },
    ],
)
def test_get_generation(args):
    test_sampler = BaseGASAmplerTestSampler(population_size=args["population_size"])
    mock_study = Mock(
        _get_trials=Mock(
            return_value=[
                Mock(system_attrs={"BaseGASAmplerTestSampler:generation": i})
                for i in args["trials"]
            ]
        )
    )
    mock_trial = Mock(system_attrs={})

    assert test_sampler.get_generation(mock_study, mock_trial) == args["generation"]

    mock_study._get_trials.assert_called_once_with(
        deepcopy=False, states=[TrialState.COMPLETE], use_cache=True
    )
    mock_study._storage.set_trial_system_attr.assert_called_once_with(
        mock_trial._trial_id,
        "BaseGASAmplerTestSampler:generation",
        args["generation"],
    )
    assert (
        len(mock_study.mock_calls) == 2
    )  # Check if only the two calls above were made
    assert len(mock_trial.mock_calls) == 0


def test_get_generation_already_set():
    test_sampler = BaseGASAmplerTestSampler(population_size=42)

    mock_study = MagicMock()
    mock_trial = MagicMock()

    mock_trial.system_attrs = {test_sampler._get_generation_key(): 42}

    assert test_sampler.get_generation(mock_study, mock_trial) == 42


@pytest.mark.parametrize(
    "args",
    [
        {
            "population_size": 3,
            "trials": [],
            "generation": 0,
            "length": 0,
        },
        {
            "population_size": 4,
            "trials": [0, 0, 0, 0],
            "generation": 0,
            "length": 4,
        },
        {
            "population_size": 3,
            "trials": [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2],
            "generation": 0,
            "length": 4,
        },
        {
            "population_size": 3,
            "trials": [0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2],
            "generation": 1,
            "length": 5,
        },
    ],
)
def test_get_population(args):
    test_sampler = BaseGASAmplerTestSampler(population_size=args["population_size"])
    mock_study = Mock(
        _get_trials=Mock(
            return_value=[
                Mock(system_attrs={"BaseGASAmplerTestSampler:generation": i})
                for i in args["trials"]
            ]
        )
    )
    mock_trial = Mock(system_attrs={})

    population = test_sampler.get_population(mock_study, args["generation"])

    assert all(
        [
            trial.system_attrs["BaseGASAmplerTestSampler:generation"]
            == args["generation"]
            for trial in population
        ]
    )
    assert len(population) == args["length"]
    assert mock_study._get_trials.call_count == 1
    assert mock_trial.mock_calls == []


@pytest.mark.parametrize(
    "args",
    [
        # {
        #     "system_attrs": {
        #         BaseGASAmplerTestSampler._get_parent_cache_key_prefix() + "0": [0, 1, 2]
        #     },
        #     "trials": [],
        #     "generation": 0,
        # },
        {
            "study_system_attrs": {
                BaseGASAmplerTestSampler._get_parent_cache_key_prefix() + "1": [0, 1, 2]
            },
            "trials": [],
            "generation": 1,
        },
    ],
)
def test_get_parent_population(args):
    test_sampler = BaseGASAmplerTestSampler(population_size=3)

    mock_study = MagicMock()
    mock_study._storage.get_study_system_attrs.return_value = args["study_system_attrs"]

    print(test_sampler.get_parent_population(mock_study, args["generation"]))

    # with patch
