plot_slice
==========

Inspect the relationship between each selected parameter and the objective
value in separate slice plots. This example selects both ``x`` and ``y``
from a ten-trial study.

.. tab-set::

    .. tab-item:: Plotly

        .. autofunction:: optuna.visualization.plot_slice

        The final ``fig`` expression displays the Plotly figure without
        calling ``plotly.io.show``.

        .. exec-code:: python
            :tag: plot-slice-plotly

            import optuna


            def objective(trial):
                x = trial.suggest_float("x", -100, 100)
                y = trial.suggest_categorical("y", [-1, 0, 1])
                return x**2 + y


            sampler = optuna.samplers.TPESampler(seed=10)
            study = optuna.create_study(sampler=sampler)
            study.optimize(objective, n_trials=10)

            fig = optuna.visualization.plot_slice(study, params=["x", "y"])
            fig

    .. tab-item:: Matplotlib

        .. autofunction:: optuna.visualization.matplotlib.plot_slice

        This call returns an array of axes. The final ``plt.gcf()``
        expression captures their single containing figure.

        .. exec-code:: python
            :tag: plot-slice-matplotlib

            import optuna
            import matplotlib.pyplot as plt


            def objective(trial):
                x = trial.suggest_float("x", -100, 100)
                y = trial.suggest_categorical("y", [-1, 0, 1])
                return x**2 + y


            sampler = optuna.samplers.TPESampler(seed=10)
            study = optuna.create_study(sampler=sampler)
            study.optimize(objective, n_trials=10)

            optuna.visualization.matplotlib.plot_slice(study, params=["x", "y"])
            plt.gcf()
