import pytest

import optuna.logging


# Disable Optuna's default handler so pytest can capture or silence logs on CI.
optuna.logging.disable_default_handler()


pytest.register_assert_rewrite("optuna.testing.pytest_storages")
