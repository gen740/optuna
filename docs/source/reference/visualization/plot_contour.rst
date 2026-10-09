plot_contour
============

Compare pairs of parameters with contours of the objective value.
This example combines a continuous parameter ``x`` with a categorical
parameter ``y`` and selects both explicitly with ``params``.

.. tab-set::

    .. tab-item:: Plotly

        .. autofunction:: optuna.visualization.plot_contour

        The final ``fig`` expression displays the Plotly figure without
        calling ``plotly.io.show``.

        .. exec-code:: python
            :tag: plot-contour-plotly

            import optuna


            def objective(trial):
                x = trial.suggest_float("x", -100, 100)
                y = trial.suggest_categorical("y", [-1, 0, 1])
                return x**2 + y


            sampler = optuna.samplers.TPESampler(seed=10)
            study = optuna.create_study(sampler=sampler)
            study.optimize(objective, n_trials=30)

            fig = optuna.visualization.plot_contour(study, params=["x", "y"])
            fig

    .. tab-item:: Matplotlib

        .. autofunction:: optuna.visualization.matplotlib.plot_contour

        The final plotting call returns the Matplotlib axes to display.

        .. exec-code:: python
            :tag: plot-contour-matplotlib

            import optuna


            def objective(trial):
                x = trial.suggest_float("x", -100, 100)
                y = trial.suggest_categorical("y", [-1, 0, 1])
                return x**2 + y


            sampler = optuna.samplers.TPESampler(seed=10)
            study = optuna.create_study(sampler=sampler)
            study.optimize(objective, n_trials=30)

            optuna.visualization.matplotlib.plot_contour(study, params=["x", "y"])
