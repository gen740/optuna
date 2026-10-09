"""Execute trusted page-local Python and reuse tagged plot artifacts (serial only)."""

import ast
import __future__
from contextlib import redirect_stderr, redirect_stdout
import hashlib
import html
import io
import os
from pathlib import Path
import posixpath
import re
import shutil
import sys
import types

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.errors import SphinxError
from sphinx.util.docutils import SphinxDirective


_TAG = re.compile(r"[a-z][a-z0-9_-]*\Z")
_FUTURE_FLAGS = sum(getattr(__future__, name).compiler_flag
                    for name in __future__.all_feature_names)


class Artifact(nodes.General, nodes.Element):
    """A serializable placeholder, resolved after every producer has been read."""


def _state(env):
    if not hasattr(env, "tagged_plot_state"):
        env.tagged_plot_state = {"tags": {}, "references": {}}
    return env.tagged_plot_state


def _directory(app):
    path = Path(app.doctreedir) / "tagged_plot"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _relative(app, path):
    return Path(os.path.relpath(path, app.srcdir)).as_posix()


def _validate(tag):
    if not _TAG.fullmatch(tag):
        raise SphinxError(f"tagged_plot: unsafe tag {tag!r}; use [a-z][a-z0-9_-]*")


def _image(record, tag):
    uri = record["path"]
    # ImageCollector has already run for deferred references. Register them in
    # env-updated and supply its normal, source-relative candidate representation.
    return nodes.image(uri=uri, candidates={"*": uri}, alt=tag)


class ExecCode(SphinxDirective):
    required_arguments = 1
    has_content = True
    option_spec = {"tag": directives.unchanged_required}

    def run(self):
        if self.arguments != ["python"]:
            raise self.error("exec-code supports only python")
        self.assert_has_content()
        app = self.env.app
        state = _state(self.env)
        tag = self.options.get("tag")
        location = f"{self.get_source_info()[0]}:{self.lineno}"
        if tag is not None:
            _validate(tag)
            if tag in state["tags"]:
                previous = state["tags"][tag]
                raise SphinxError(
                    f"{location}: duplicate plot tag {tag!r} (owned by {previous['docname']})"
                )
        namespaces = app._tagged_plot_namespaces
        if self.env.docname not in namespaces:
            identity = f"{app.srcdir}:{self.env.docname}".encode()
            name = "_tagged_plot_" + hashlib.sha256(identity).hexdigest()
            module = types.ModuleType(name)
            module.__file__ = str(self.env.doc2path(self.env.docname))
            sys.modules[name] = module  # Required by dataclasses and similar introspection.
            pyplot = sys.modules.get("matplotlib.pyplot")
            namespaces[self.env.docname] = {
                "module": module, "flags": 0,
                "figures_before": set(pyplot.get_fignums()) if pyplot else set(),
            }
        page = namespaces[self.env.docname]
        namespace = page["module"].__dict__
        code = "\n".join(self.content)
        output = io.StringIO()
        try:
            tree = compile(code, location, "exec", page["flags"] | ast.PyCF_ONLY_AST,
                           dont_inherit=True)
            if tag is not None and (not tree.body or not isinstance(tree.body[-1], ast.Expr)):
                raise ValueError("a tagged block must end with a Figure/Axes expression")
            with redirect_stdout(output), redirect_stderr(output):
                value = None
                if tree.body and isinstance(tree.body[-1], ast.Expr):
                    final = tree.body.pop()
                    prefix = compile(tree, location, "exec", page["flags"], dont_inherit=True)
                    page["flags"] |= prefix.co_flags & _FUTURE_FLAGS
                    exec(prefix, namespace)
                    expression = compile(ast.Expression(final.value), location, "eval",
                                         page["flags"], dont_inherit=True)
                    value = eval(expression, namespace)
                else:
                    compiled = compile(tree, location, "exec", page["flags"], dont_inherit=True)
                    page["flags"] |= compiled.co_flags & _FUTURE_FLAGS
                    exec(compiled, namespace)
                if tag is not None:
                    record = self._save(app, tag, value)
                    record.update(docname=self.env.docname, line=self.lineno)
                    state["tags"][tag] = record
        except Exception as exc:
            captured = output.getvalue()
            raise SphinxError(
                f"{location}: exec-code failed: {type(exc).__name__}: {exc}"
                + (f"\nCaptured output:\n{captured}" if captured else "")
            ) from exc
        literal = nodes.literal_block(code, code, language="python")
        self.set_source_info(literal)
        result = [literal]
        if output.getvalue():
            result.append(nodes.literal_block(output.getvalue(), output.getvalue(),
                                              classes=["exec-code-output"]))
        if tag is not None:
            if record["kind"] == "png":
                # Collector expects a source-root-relative URI at read time.
                result.append(nodes.image(uri="/" + record["path"], alt=tag))
            else:
                result.append(Artifact(tag=tag))
        return result

    def _save(self, app, tag, value):
        # Lazy imports keep untagged preparation independent of plotting libraries.
        from matplotlib.axes import Axes
        from matplotlib.figure import Figure

        directory = _directory(app)
        if isinstance(value, (Figure, Axes)):
            path = directory / f"{tag}.png"
            figure = value.figure if isinstance(value, Axes) else value
            figure.savefig(path, format="png")
            return {"kind": "png", "path": _relative(app, path)}
        from plotly.graph_objects import Figure as PlotlyFigure
        from plotly.io import to_html
        from plotly.offline import get_plotlyjs

        if isinstance(value, PlotlyFigure):
            path = directory / f"{tag}.html"
            # Public APIs available in Plotly 4.9; no div_id or private renderer.
            path.write_text(to_html(value, full_html=True, include_plotlyjs="directory"),
                            encoding="utf-8")
            javascript = directory / "plotly.min.js"
            script = get_plotlyjs()
            if not javascript.exists() or javascript.read_text(encoding="utf-8") != script:
                javascript.write_text(script, encoding="utf-8")
            return {"kind": "html", "path": _relative(app, path),
                    "javascript": _relative(app, javascript)}
        raise TypeError("tagged final expression must return a Matplotlib Figure/Axes "
                        "or Plotly Figure")


class ArtifactThumbnail(SphinxDirective):
    required_arguments = 1

    def run(self):
        tag = self.arguments[0]
        _validate(tag)
        references = _state(self.env)["references"].setdefault(self.env.docname, [])
        references.append({"tag": tag, "line": self.lineno})
        node = Artifact(tag=tag, thumbnail=True)
        self.set_source_info(node)
        return [node]


def _release_page(app, docname):
    page = app._tagged_plot_namespaces.pop(docname, None)
    if page is not None:
        pyplot = sys.modules.get("matplotlib.pyplot")
        if pyplot:
            for number in set(pyplot.get_fignums()) - page["figures_before"]:
                pyplot.close(number)
        sys.modules.pop(page["module"].__name__, None)


def _read_finished(app, doctree):
    _release_page(app, app.env.docname)


def _purge(app, env, docname):
    state = _state(env)
    state["tags"] = {tag: record for tag, record in state["tags"].items()
                     if record["docname"] != docname}
    state["references"].pop(docname, None)
    _release_page(app, docname)


def _before_read(app, env, docnames):
    # Purge all changing owners before any directive runs (also allows moving tags).
    for docname in docnames:
        _purge(app, env, docname)


def _outdated(app, env, added, changed, removed):
    # No execution cache: ordinary Sphinx incremental reads, plus regeneration
    # when owned artifacts disappear even though their producer source is unchanged.
    return sorted({record["docname"] for record in _state(env)["tags"].values()
                   if any(not (Path(app.srcdir) / record[key]).is_file()
                          for key in ("path", "javascript") if key in record)})


def _updated(app, env):
    for docname in list(app._tagged_plot_namespaces):
        _release_page(app, docname)
    state = _state(env)
    for docname, references in state["references"].items():
        for reference in references:
            tag = reference["tag"]
            record = state["tags"].get(tag)
            location = f"{env.doc2path(docname)}:{reference['line']}"
            if record is None:
                raise SphinxError(f"{location}: unknown plot tag {tag!r}")
            if record["kind"] != "png":
                raise SphinxError(
                    f"{location}: artifact-thumbnail requires a Matplotlib tag: {tag!r}"
                )
            env.images.add_file(docname, record["path"])
            env.note_dependency(record["path"], docname=docname)
            env.note_dependency(env.doc2path(record["docname"]), docname=docname)
    html_records = [record for record in state["tags"].values() if record["kind"] == "html"]
    if html_records and app.builder.format == "html":
        destination = Path(app.outdir) / "_tagged_plots"
        destination.mkdir(parents=True, exist_ok=True)
        for record in html_records:
            for key in ("path", "javascript"):
                source = Path(app.srcdir) / record[key]
                shutil.copyfile(source, destination / source.name)
    # Rewrite references even on a warm build: a producer may have changed without
    # its consumer being read. This does not execute the consumer a second time.
    return sorted(state["references"])


def _resolve(app, doctree, docname):
    for node in list(doctree.findall(Artifact)):
        tag = node["tag"]
        record = _state(app.env)["tags"][tag]
        if record["kind"] == "png":
            replacement = _image(record, tag)
        elif app.builder.format != "html":
            replacement = nodes.paragraph(
                "", f"Interactive Plotly plot {tag!r} is available only in HTML documentation."
            )
        else:
            target = f"_tagged_plots/{tag}.html"
            parent = posixpath.dirname(app.builder.get_target_uri(docname)) or "."
            uri = posixpath.relpath(target, parent)
            markup = (f'<iframe src="{html.escape(uri, quote=True)}" '
                      f'title="{html.escape(tag, quote=True)}" width="100%" height="500" '
                      'loading="lazy"></iframe>')
            replacement = nodes.raw("", markup, format="html")
        replacement.source, replacement.line = node.source, node.line
        node.replace_self(replacement)


def _build_finished(app, exception):
    # Also release a partially executed page after a failed build.
    for docname in list(app._tagged_plot_namespaces):
        _release_page(app, docname)


def setup(app):
    app._tagged_plot_namespaces = {}
    app.add_node(Artifact)
    app.add_directive("exec-code", ExecCode)
    app.add_directive("artifact-thumbnail", ArtifactThumbnail)
    app.connect("env-get-outdated", _outdated)
    app.connect("env-before-read-docs", _before_read)
    app.connect("env-purge-doc", _purge)
    app.connect("doctree-read", _read_finished, priority=999)
    app.connect("env-updated", _updated)
    app.connect("doctree-resolved", _resolve)
    app.connect("build-finished", _build_finished)
    return {"version": "0.1", "env_version": 1,
            "parallel_read_safe": False, "parallel_write_safe": False}
