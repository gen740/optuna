plot_parallel_coordinate
========================

Compare parameter combinations and objective values on parallel axes.
The example selects ``x`` and ``y`` explicitly; the same interface can
visualize relationships in higher-dimensional search spaces.

.. tab-set::

    .. tab-item:: Plotly

        .. autofunction:: optuna.visualization.plot_parallel_coordinate

        The final ``fig`` expression displays the Plotly figure without
        calling ``plotly.io.show``.

        .. exec-code:: python
            :tag: plot-parallel-coordinate-plotly

            import optuna


            def objective(trial):
                x = trial.suggest_float("x", -100, 100)
                y = trial.suggest_categorical("y", [-1, 0, 1])
                return x**2 + y


            sampler = optuna.samplers.TPESampler(seed=10)
            study = optuna.create_study(sampler=sampler)
            study.optimize(objective, n_trials=10)

            fig = optuna.visualization.plot_parallel_coordinate(study, params=["x", "y"])
            fig

    .. tab-item:: Matplotlib

        .. autofunction:: optuna.visualization.matplotlib.plot_parallel_coordinate

        The final plotting call returns the Matplotlib axes to display.

        .. exec-code:: python
            :tag: plot-parallel-coordinate-matplotlib

            import optuna


            def objective(trial):
                x = trial.suggest_float("x", -100, 100)
                y = trial.suggest_categorical("y", [-1, 0, 1])
                return x**2 + y


            sampler = optuna.samplers.TPESampler(seed=10)
            study = optuna.create_study(sampler=sampler)
            study.optimize(objective, n_trials=10)

            optuna.visualization.matplotlib.plot_parallel_coordinate(study, params=["x", "y"])
