Tagged plot prototype
=====================

Loading and dependencies
------------------------

Add this directory to ``sys.path`` in ``conf.py`` and add ``"tagged_plot"``
to ``extensions``::

    from pathlib import Path
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent / "_ext"))
    extensions = ["tagged_plot"]  # Append to the project's existing list.

No extension-specific configuration is required. Use a serial Sphinx build
(``-j 1``, the default); both parallel safety flags are false. Set
``MPLBACKEND=Agg`` before building in a headless environment. The prototype
uses Sphinx/Docutils, Matplotlib, and Plotly already used by the documentation.
It was tested with Python 3.12, Sphinx 9.1, Matplotlib 3.11, and both Plotly
7.1 and the project's minimum Plotly 4.9.0. Older Sphinx versions are not
verified. Plotly interactivity requires an HTML-family builder. Non-HTML
builders retain source/output and Matplotlib images; Plotly displays a paragraph
noting that the interactive plot is HTML-only. No static Plotly export,
Kaleido invocation, iframe, or Plotly output-asset copy is attempted there.

Directive contract
------------------

Only explicit ``exec-code`` blocks execute. They run trusted Python in the
Sphinx process, not in a sandbox or kernel. Do not enable this extension for
untrusted documentation. Normal Python side effects, imports, and errors
apply. The extension does not change the working directory.

Blocks on the same document share one namespace during that document's read;
different documents do not share variables. A temporary registered Python
module supports dataclass introspection, and compiler ``__future__`` flags
persist across blocks on the page. Neither modules nor flags carry across
pages. Untagged blocks allow preparation.
A tagged block must end with an expression returning a Matplotlib ``Figure``
or ``Axes``, or a Plotly ``Figure``. The final expression is evaluated once,
not executed and then evaluated again. Untagged final expressions are also
evaluated once, with their return values discarded. Every block displays its
Python source and any captured stdout/stderr as ordinary literal nodes;
stdout and stderr are combined in write order. Execution or rendering failures
abort the build with the source location, exception, and captured output.

For example::

    .. exec-code:: python

       import matplotlib.pyplot as plt
       values = [1, 3, 2]

    .. exec-code:: python
       :tag: objective-history

       fig, ax = plt.subplots()
       ax.plot(values)
       ax

    .. exec-code:: python
       :tag: interactive-history

       import plotly.graph_objects as go
       go.Figure(go.Scatter(y=values))

Tags are globally unique and match ``[a-z][a-z0-9_-]*``. Duplicate tags,
unsafe tags, missing tags, unsupported return values, and non-expression
endings are explicit errors. Figures remain open between blocks for same-page
reuse. New pyplot figure managers are closed after the document is read
(and after a failed build); figures already open before the page are preserved.
Close figures explicitly within long pages if necessary.

A different page can display the existing Matplotlib PNG without running
another example::

    .. artifact-thumbnail:: objective-history

``artifact-thumbnail`` currently accepts only a tag, and only Matplotlib
artifacts. It uses the saved full PNG, with no separate Pillow thumbnail or
implicit hyperlink. It can appear in an index read before the producer.
Resolution and image registration occur after all pages have been read,
so strict builds do not issue premature missing-image warnings.

Artifacts and incremental builds
--------------------------------

Owned artifacts live in ``<doctreedir>/tagged_plot/<tag>.png`` or
``<tag>.html``, with one shared ``plotly.min.js``. Paths are deterministic;
Plotly's generated internal HTML identifiers need not be. PNGs go through
Sphinx's image registry and normal ``_images`` copying. Plotly HTML and its
local JavaScript are copied to ``<outdir>/_tagged_plots`` and displayed in
iframes with builder-relative URLs, including nested ``dirhtml`` pages.
There are no CDN script dependencies, private renderer hooks, Kaleido,
``show()`` calls, or assumptions about the newer ``to_html(div_id=...)``
parameter. Plotly uses public ``to_html(include_plotlyjs="directory")`` and
``plotly.offline.get_plotlyjs()``.

Execution namespaces live only on the application during reading and are
released at the end of each document read, including its temporary module.
Doctrees hold literal source/output and serializable
artifact placeholders, never Figure objects or namespaces. The environment
stores tag ownership, artifact paths, and reference metadata only, alongside
Sphinx's normal image/dependency records.

This is ordinary Sphinx incremental reading, not dependency-aware execution
caching:
changed producer sources execute again, and missing owned PNG/HTML/JavaScript
files force producer rereads. Regenerating Plotly HTML compares and refreshes
the shared JavaScript against the installed Plotly version, including on a
fresh ``-E`` build. Unchanged producers do not execute on warm
builds. Reference pages are rewritten on warm builds, images registered before
asset copying, and Plotly output assets recopied, so deleting copied output
assets is recoverable without reexecuting examples. External input files,
imported module changes, package upgrades, and stochastic results are not
tracked; use a fresh environment (``-E``) when needed. Obsolete artifacts are
not garbage-collected. There is no notebook pipeline or cross-page execution.
