plot_intermediate_values
========================

Inspect the intermediate objective values reported during each trial.
The objective uses gradient descent with a sampled learning rate and
reports up to 128 steps, allowing the study to prune unpromising trials.

.. tab-set::

    .. tab-item:: Plotly

        .. autofunction:: optuna.visualization.plot_intermediate_values

        The final ``fig`` expression displays the Plotly figure without
        calling ``plotly.io.show``.

        .. exec-code:: python
            :tag: plot-intermediate-values-plotly

            import optuna


            def f(x):
                return (x - 2) ** 2


            def df(x):
                return 2 * x - 4


            def objective(trial):
                lr = trial.suggest_float("lr", 1e-5, 1e-1, log=True)

                x = 3
                for step in range(128):
                    y = f(x)

                    trial.report(y, step=step)
                    if trial.should_prune():
                        raise optuna.TrialPruned()

                    gy = df(x)
                    x -= gy * lr

                return y


            sampler = optuna.samplers.TPESampler(seed=10)
            study = optuna.create_study(sampler=sampler)
            study.optimize(objective, n_trials=16)

            fig = optuna.visualization.plot_intermediate_values(study)
            fig

    .. tab-item:: Matplotlib

        .. autofunction:: optuna.visualization.matplotlib.plot_intermediate_values

        The final plotting call returns the Matplotlib axes to display.

        .. exec-code:: python
            :tag: plot-intermediate-values-matplotlib

            import optuna


            def f(x):
                return (x - 2) ** 2


            def df(x):
                return 2 * x - 4


            def objective(trial):
                lr = trial.suggest_float("lr", 1e-5, 1e-1, log=True)

                x = 3
                for step in range(128):
                    y = f(x)

                    trial.report(y, step=step)
                    if trial.should_prune():
                        raise optuna.TrialPruned()

                    gy = df(x)
                    x -= gy * lr

                return y


            sampler = optuna.samplers.TPESampler(seed=10)
            study = optuna.create_study(sampler=sampler)
            study.optimize(objective, n_trials=16)

            optuna.visualization.matplotlib.plot_intermediate_values(study)
