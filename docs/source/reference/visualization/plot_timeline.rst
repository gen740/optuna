plot_timeline
=============

Inspect trial execution times and states, including overlapping trials.
The example runs 50 trials with two parallel workers, sleeps for a sampled
duration, and deliberately produces completed, pruned, and failed trials.
The study catches ``ValueError`` so that failed trials do not stop the run.

.. tab-set::

    .. tab-item:: Plotly

        .. autofunction:: optuna.visualization.plot_timeline

        The final ``fig`` expression displays the Plotly figure without
        calling ``plotly.io.show``.

        .. exec-code:: python
            :tag: plot-timeline-plotly

            import time

            import optuna


            def objective(trial):
                x = trial.suggest_float("x", 0, 1)
                time.sleep(x * 0.1)
                if x > 0.8:
                    raise ValueError()
                if x > 0.4:
                    raise optuna.TrialPruned()
                return x ** 2


            study = optuna.create_study(direction="minimize")
            study.optimize(
                objective, n_trials=50, n_jobs=2, catch=(ValueError,)
            )

            fig = optuna.visualization.plot_timeline(study)
            fig

    .. tab-item:: Matplotlib

        .. autofunction:: optuna.visualization.matplotlib.plot_timeline

        The final plotting call returns the Matplotlib axes to display.

        .. exec-code:: python
            :tag: plot-timeline-matplotlib

            import time
            import optuna


            def objective(trial):
                x = trial.suggest_float("x", 0, 1)
                time.sleep(x * 0.1)
                if x > 0.8:
                    raise ValueError()
                if x > 0.4:
                    raise optuna.TrialPruned()
                return x**2


            study = optuna.create_study(direction="minimize")
            study.optimize(objective, n_trials=50, n_jobs=2, catch=(ValueError,))

            optuna.visualization.matplotlib.plot_timeline(study)
