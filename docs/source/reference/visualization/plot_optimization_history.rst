plot_optimization_history
=========================

Follow objective values and the best value found as optimization proceeds.
This example runs ten trials of a quadratic objective with a continuous
parameter and a categorical offset.

.. tab-set::

    .. tab-item:: Plotly

        .. autofunction:: optuna.visualization.plot_optimization_history

        The final ``fig`` expression displays the Plotly figure without
        calling ``plotly.io.show``.

        .. exec-code:: python
            :tag: plot-optimization-history-plotly

            import optuna


            def objective(trial):
                x = trial.suggest_float("x", -100, 100)
                y = trial.suggest_categorical("y", [-1, 0, 1])
                return x**2 + y


            sampler = optuna.samplers.TPESampler(seed=10)
            study = optuna.create_study(sampler=sampler)
            study.optimize(objective, n_trials=10)

            fig = optuna.visualization.plot_optimization_history(study)
            fig

    .. tab-item:: Matplotlib

        .. autofunction:: optuna.visualization.matplotlib.plot_optimization_history

        The final plotting call returns the Matplotlib axes to display.

        .. exec-code:: python
            :tag: plot-optimization-history-matplotlib

            import optuna

            def objective(trial):
                x = trial.suggest_float("x", -100, 100)
                y = trial.suggest_categorical("y", [-1, 0, 1])
                return x**2 + y


            sampler = optuna.samplers.TPESampler(seed=10)
            study = optuna.create_study(sampler=sampler)
            study.optimize(objective, n_trials=10)

            optuna.visualization.matplotlib.plot_optimization_history(study)
