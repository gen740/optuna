plot_terminator_improvement
===========================

Compare estimated improvement potentials with cross-validation errors.
Each backend example runs 30 trials tuning a LightGBM classifier on the
wine dataset, reports scores from five-fold cross-validation, and plots
the error estimates alongside the improvement potentials.

These examples require LightGBM, scikit-learn, and the dependencies of the
default terminator improvement evaluator. Training and evaluating the
improvement potentials can take substantially longer than the other
visualization examples; both backend examples execute the full study.

.. tab-set::

    .. tab-item:: Plotly

        .. autofunction:: optuna.visualization.plot_terminator_improvement

        The final ``fig`` expression displays the Plotly figure without
        calling ``plotly.io.show``.

        .. exec-code:: python
            :tag: plot-terminator-improvement-plotly

            from lightgbm import LGBMClassifier
            from sklearn.datasets import load_wine
            from sklearn.model_selection import cross_val_score
            from sklearn.model_selection import KFold
            import optuna
            from optuna.terminator import report_cross_validation_scores
            from optuna.visualization import plot_terminator_improvement


            def objective(trial):
                X, y = load_wine(return_X_y=True)
                clf = LGBMClassifier(
                    reg_alpha=trial.suggest_float("reg_alpha", 1e-8, 10.0, log=True),
                    reg_lambda=trial.suggest_float("reg_lambda", 1e-8, 10.0, log=True),
                    num_leaves=trial.suggest_int("num_leaves", 2, 256),
                    colsample_bytree=trial.suggest_float("colsample_bytree", 0.4, 1.0),
                    subsample=trial.suggest_float("subsample", 0.4, 1.0),
                    subsample_freq=trial.suggest_int("subsample_freq", 1, 7),
                    min_child_samples=trial.suggest_int("min_child_samples", 5, 100),
                )
                scores = cross_val_score(clf, X, y, cv=KFold(n_splits=5, shuffle=True))
                report_cross_validation_scores(trial, scores)
                return scores.mean()


            study = optuna.create_study()
            study.optimize(objective, n_trials=30)

            fig = plot_terminator_improvement(study, plot_error=True)
            fig

    .. tab-item:: Matplotlib

        .. autofunction:: optuna.visualization.matplotlib.plot_terminator_improvement

        The final plotting call returns the Matplotlib axes to display.

        .. exec-code:: python
            :tag: plot-terminator-improvement-matplotlib

            from lightgbm import LGBMClassifier
            from sklearn.datasets import load_wine
            from sklearn.model_selection import cross_val_score
            from sklearn.model_selection import KFold
            import optuna
            from optuna.terminator import report_cross_validation_scores
            from optuna.visualization.matplotlib import plot_terminator_improvement


            def objective(trial):
                X, y = load_wine(return_X_y=True)
                clf = LGBMClassifier(
                    reg_alpha=trial.suggest_float("reg_alpha", 1e-8, 10.0, log=True),
                    reg_lambda=trial.suggest_float("reg_lambda", 1e-8, 10.0, log=True),
                    num_leaves=trial.suggest_int("num_leaves", 2, 256),
                    colsample_bytree=trial.suggest_float("colsample_bytree", 0.4, 1.0),
                    subsample=trial.suggest_float("subsample", 0.4, 1.0),
                    subsample_freq=trial.suggest_int("subsample_freq", 1, 7),
                    min_child_samples=trial.suggest_int("min_child_samples", 5, 100),
                )
                scores = cross_val_score(clf, X, y, cv=KFold(n_splits=5, shuffle=True))
                report_cross_validation_scores(trial, scores)
                return scores.mean()


            study = optuna.create_study()
            study.optimize(objective, n_trials=30)

            plot_terminator_improvement(study, plot_error=True)
