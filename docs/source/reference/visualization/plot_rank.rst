plot_rank
=========

Compare parameter combinations using colors that indicate objective ranks.
The example records the constraint ``400 - (x + y) ** 2`` on each trial
and plots the continuous parameter ``x`` against the categorical ``y``.

.. tab-set::

    .. tab-item:: Plotly

        .. autofunction:: optuna.visualization.plot_rank

        The final ``fig`` expression displays the Plotly figure without
        calling ``plotly.io.show``.

        .. exec-code:: python
            :tag: plot-rank-plotly

            import optuna


            def objective(trial):
                x = trial.suggest_float("x", -100, 100)
                y = trial.suggest_categorical("y", [-1, 0, 1])

                c0 = 400 - (x + y) ** 2
                trial.set_constraint("c0", c0)

                return x**2 + y


            sampler = optuna.samplers.TPESampler(seed=10)
            study = optuna.create_study(sampler=sampler)
            study.optimize(objective, n_trials=30)

            fig = optuna.visualization.plot_rank(study, params=["x", "y"])
            fig

    .. tab-item:: Matplotlib

        .. autofunction:: optuna.visualization.matplotlib.plot_rank

        The final plotting call returns the Matplotlib axes to display.

        .. exec-code:: python
            :tag: plot-rank-matplotlib

            import optuna


            def objective(trial):
                x = trial.suggest_float("x", -100, 100)
                y = trial.suggest_categorical("y", [-1, 0, 1])

                c0 = 400 - (x + y) ** 2
                trial.set_constraint("c0", c0)

                return x**2 + y


            sampler = optuna.samplers.TPESampler(seed=10)
            study = optuna.create_study(sampler=sampler)
            study.optimize(objective, n_trials=30)

            optuna.visualization.matplotlib.plot_rank(study, params=["x", "y"])
