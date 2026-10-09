plot_param_importances
======================

Estimate how strongly each hyperparameter affects the objective.
The example runs 100 randomly sampled trials of a function with quadratic,
cubic, and quartic terms before plotting the parameter importances.

.. tab-set::

    .. tab-item:: Plotly

        .. autofunction:: optuna.visualization.plot_param_importances

        The final ``fig`` expression displays the Plotly figure without
        calling ``plotly.io.show``.

        .. exec-code:: python
            :tag: plot-param-importances-plotly

            import optuna


            def objective(trial):
                x = trial.suggest_int("x", 0, 2)
                y = trial.suggest_float("y", -1.0, 1.0)
                z = trial.suggest_float("z", 0.0, 1.5)
                return x**2 + y**3 - z**4


            sampler = optuna.samplers.RandomSampler(seed=10)
            study = optuna.create_study(sampler=sampler)
            study.optimize(objective, n_trials=100)

            fig = optuna.visualization.plot_param_importances(study)
            fig

    .. tab-item:: Matplotlib

        .. autofunction:: optuna.visualization.matplotlib.plot_param_importances

        The final plotting call returns the Matplotlib axes to display.

        .. exec-code:: python
            :tag: plot-param-importances-matplotlib

            import optuna


            def objective(trial):
                x = trial.suggest_int("x", 0, 2)
                y = trial.suggest_float("y", -1.0, 1.0)
                z = trial.suggest_float("z", 0.0, 1.5)
                return x**2 + y**3 - z**4


            sampler = optuna.samplers.RandomSampler(seed=10)
            study = optuna.create_study(sampler=sampler)
            study.optimize(objective, n_trials=100)

            optuna.visualization.matplotlib.plot_param_importances(study)
