plot_pareto_front
=================

Inspect trade-offs between objectives in a multi-objective study.
The examples first plot a two-objective Pareto front. The Plotly tab also
shows how to select two objectives from a three-objective study.

.. tab-set::

    .. tab-item:: Plotly

        .. autofunction:: optuna.visualization.plot_pareto_front

        The final ``fig`` expression displays the Plotly figure without
        calling ``plotly.io.show``.

        .. exec-code:: python
            :tag: plot-pareto-front-plotly

            import optuna


            def objective(trial):
                x = trial.suggest_float("x", 0, 5)
                y = trial.suggest_float("y", 0, 3)

                v0 = 4 * x**2 + 4 * y**2
                v1 = (x - 5) ** 2 + (y - 5) ** 2
                return v0, v1


            study = optuna.create_study(directions=["minimize", "minimize"])
            study.optimize(objective, n_trials=50)

            fig = optuna.visualization.plot_pareto_front(study)
            fig

        The following code snippet shows how to plot a 2-dimensional Pareto front
        of a 3-dimensional study.
        This example is scalable, e.g., for plotting a 2- or 3-dimensional Pareto front
        of a 4-dimensional study and so on.

        .. exec-code:: python
            :tag: plot-pareto-front-plotly-projection

            import optuna


            def objective(trial):
                x = trial.suggest_float("x", 0, 5)
                y = trial.suggest_float("y", 0, 3)
                v0 = 5 * x**2 + 3 * y**2
                v1 = (x - 10) ** 2 + (y - 10) ** 2
                v2 = x + y

                return v0, v1, v2


            study = optuna.create_study(directions=["minimize", "minimize", "minimize"])

            study.optimize(objective, n_trials=100)

            fig = optuna.visualization.plot_pareto_front(
                study,
                targets=lambda t: (t.values[0], t.values[1]),
                target_names=["Objective 0", "Objective 1"],
            )

            fig

    .. tab-item:: Matplotlib

        .. autofunction:: optuna.visualization.matplotlib.plot_pareto_front

        The final plotting call returns the Matplotlib axes to display.

        .. exec-code:: python
            :tag: plot-pareto-front-matplotlib

            import optuna


            def objective(trial):
                x = trial.suggest_float("x", 0, 5)
                y = trial.suggest_float("y", 0, 3)

                v0 = 4 * x**2 + 4 * y**2
                v1 = (x - 5) ** 2 + (y - 5) ** 2
                return v0, v1


            study = optuna.create_study(directions=["minimize", "minimize"])
            study.optimize(objective, n_trials=50)

            optuna.visualization.matplotlib.plot_pareto_front(study)
