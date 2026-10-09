plot_hypervolume_history
========================

Track the hypervolume attained during a two-objective optimization.
Both objectives are minimized, and the reference point ``[100, 50]``
defines the region used to measure progress.

.. tab-set::

    .. tab-item:: Plotly

        .. autofunction:: optuna.visualization.plot_hypervolume_history

        The final ``fig`` expression displays the Plotly figure without
        calling ``plotly.io.show``.

        .. exec-code:: python
            :tag: plot-hypervolume-history-plotly

            import optuna


            def objective(trial):
                x = trial.suggest_float("x", 0, 5)
                y = trial.suggest_float("y", 0, 3)

                v0 = 4 * x**2 + 4 * y**2
                v1 = (x - 5) ** 2 + (y - 5) ** 2
                return v0, v1


            study = optuna.create_study(directions=["minimize", "minimize"])
            study.optimize(objective, n_trials=50)

            reference_point = [100.0, 50.0]
            fig = optuna.visualization.plot_hypervolume_history(study, reference_point)
            fig

    .. tab-item:: Matplotlib

        .. autofunction:: optuna.visualization.matplotlib.plot_hypervolume_history

        The final ``plt.gcf()`` expression captures the figure after
        applying the original ``plt.tight_layout()`` adjustment.

        .. exec-code:: python
            :tag: plot-hypervolume-history-matplotlib

            import optuna
            import matplotlib.pyplot as plt


            def objective(trial):
                x = trial.suggest_float("x", 0, 5)
                y = trial.suggest_float("y", 0, 3)

                v0 = 4 * x ** 2 + 4 * y ** 2
                v1 = (x - 5) ** 2 + (y - 5) ** 2
                return v0, v1


            study = optuna.create_study(directions=["minimize", "minimize"])
            study.optimize(objective, n_trials=50)

            reference_point=[100, 50]
            optuna.visualization.matplotlib.plot_hypervolume_history(study, reference_point)
            plt.tight_layout()
            plt.gcf()
