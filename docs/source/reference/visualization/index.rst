.. _visualization-examples-index:

.. _general_visualization_examples:

.. module:: optuna.visualization

.. module:: optuna.visualization.matplotlib

optuna.visualization
====================

The :mod:`optuna.visualization` module provides functions for plotting the
optimization process with Plotly. The :mod:`optuna.visualization.matplotlib`
module provides corresponding functions with Matplotlib as the backend.
Each page below documents both APIs and includes executable examples in
backend-specific tabs. Plotting functions generally take a
:class:`~optuna.study.Study`; functions that select parameters accept a list
in the ``params`` argument.

The previews reuse the tagged Matplotlib example figures from these pages.

.. grid:: 3
    :gutter: 2

    .. grid-item-card:: plot_contour
        :link: plot_contour
        :link-type: doc

        .. artifact-thumbnail:: plot-contour-matplotlib

    .. grid-item-card:: plot_edf
        :link: plot_edf
        :link-type: doc

        .. artifact-thumbnail:: plot-edf-matplotlib

    .. grid-item-card:: plot_hypervolume_history
        :link: plot_hypervolume_history
        :link-type: doc

        .. artifact-thumbnail:: plot-hypervolume-history-matplotlib

    .. grid-item-card:: plot_intermediate_values
        :link: plot_intermediate_values
        :link-type: doc

        .. artifact-thumbnail:: plot-intermediate-values-matplotlib

    .. grid-item-card:: plot_optimization_history
        :link: plot_optimization_history
        :link-type: doc

        .. artifact-thumbnail:: plot-optimization-history-matplotlib

    .. grid-item-card:: plot_parallel_coordinate
        :link: plot_parallel_coordinate
        :link-type: doc

        .. artifact-thumbnail:: plot-parallel-coordinate-matplotlib

    .. grid-item-card:: plot_param_importances
        :link: plot_param_importances
        :link-type: doc

        .. artifact-thumbnail:: plot-param-importances-matplotlib

    .. grid-item-card:: plot_pareto_front
        :link: plot_pareto_front
        :link-type: doc

        .. artifact-thumbnail:: plot-pareto-front-matplotlib

    .. grid-item-card:: plot_rank
        :link: plot_rank
        :link-type: doc

        .. artifact-thumbnail:: plot-rank-matplotlib

    .. grid-item-card:: plot_slice
        :link: plot_slice
        :link-type: doc

        .. artifact-thumbnail:: plot-slice-matplotlib

    .. grid-item-card:: plot_terminator_improvement
        :link: plot_terminator_improvement
        :link-type: doc

        .. artifact-thumbnail:: plot-terminator-improvement-matplotlib

    .. grid-item-card:: plot_timeline
        :link: plot_timeline
        :link-type: doc

        .. artifact-thumbnail:: plot-timeline-matplotlib

.. note::
    Plotly figures require a compatible renderer in interactive environments.
    If using `JupyterLab <https://github.com/jupyterlab/jupyterlab>`_, follow
    the `Plotly installation guide <https://github.com/plotly/plotly.py#jupyterlab-support>`_
    to configure figure display.

.. toctree::
    :hidden:

    plot_contour
    plot_edf
    plot_hypervolume_history
    plot_intermediate_values
    plot_optimization_history
    plot_parallel_coordinate
    plot_param_importances
    plot_pareto_front
    plot_rank
    plot_slice
    plot_terminator_improvement
    plot_timeline
    matplotlib/index

.. seealso::
    The :ref:`visualization` tutorial provides use-cases with examples.
