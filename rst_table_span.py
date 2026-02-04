"""Support for colspan and rowspan in RST tables for docutils and Sphinx"""

__version__ = "1.0.0"


import re

import docutils.nodes as nodes
from docutils.transforms import Transform, TransformError


def col_span_role(role, rawtext, text, lineno, inliner, options=None, content=None):
    if not text.isnumeric() or int(text) < 1:
        return None, [inliner.reporter.error("colspan must be a positive integer", line=lineno)]
    return make_pending_nodes(inliner, int(text), 1)


def row_span_role(role, rawtext, text, lineno, inliner, options=None, content=None):
    if not text.isnumeric() or int(text) < 1:
        return None, [inliner.reporter.error("colspan must be a positive integer", line=lineno)]
    return make_pending_nodes(inliner, 1, int(text))


def cell_span_role(role, rawtext, text, lineno, inliner, options=None, content=None):
    m = re.match(r"(?P<cols>[1-9][0-9]*)x(?P<rows>[1-9][0-9]*)", text)
    if not m:
        return None, [inliner.reporter.error("cellspan must be of format <COLS>x<ROWS>", line=lineno)]
    return make_pending_nodes(inliner, int(m.group("cols")), int(m.group("rows")))


def make_pending_nodes(inliner, cols, rows):
    details = dict(cols=cols, rows=rows)
    mark = nodes.pending(CellSpanMarkTransform, details)
    inliner.document.note_pending(mark)
    sweep = nodes.pending(CellSpanSweepTransform)
    inliner.document.note_pending(sweep)
    return [mark, sweep], []


class CellSpanMarkTransform(Transform):
    default_priority = 213

    def apply(self):
        col_span = self.startnode.details["cols"]
        row_span = self.startnode.details["rows"]
        cell_node = pop_pending_and_find_cell(self.startnode)
        row_node = cell_node.parent
        table_node = row_node.parent
        col_index = row_node.children.index(cell_node)
        row_index = table_node.children.index(row_node)
        if col_index + col_span > len(row_node.children):
            raise TransformError("colspan extending outside table")
        if row_index + row_span > len(table_node.children):
            raise TransformError("colspan extending outside table")

        table_node["needs_sweep"] = True
        for i in range(row_span):
            loop_row = table_node.children[row_index + i]
            for j in range(col_span):
                loop_cell = loop_row.children[col_index + j]
                if i == 0 and j == 0:
                    # The top left cell of the span rectangle contains the
                    # contents. Keep it and set its "more" attributes.
                    loop_cell["morecols"] = col_span - 1
                    loop_cell["morerows"] = row_span - 1
                else:
                    # Other cells in the span rectangle shall be removed.
                    loop_cell["sweep"] = True


class CellSpanSweepTransform(Transform):
    default_priority = 214

    def apply(self):
        cell_node = pop_pending_and_find_cell(self.startnode)
        row_node = cell_node.parent
        table_node = row_node.parent

        if not table_node.attributes.get("needs_sweep", False):
            return
        for row in table_node.children:
            to_sweep = [entry for entry in row.children
                        if entry.attributes.get("sweep", False)]
            for entry in to_sweep:
                row.children.remove(entry)
        del table_node.attributes["needs_sweep"]


def pop_pending_and_find_cell(pending):
    node = pending.parent
    pending.parent.remove(pending)
    while True:
        if node is None:
            raise TransformError("colspan, rowspan, and cellspan roles must be used in table cells")
        elif isinstance(node, nodes.entry):
            break
        else:
            node = node.parent
    return node


# Entrypoint for the Sphinx extension mechanism
def setup(app):
    app.add_role("colspan", col_span_role)
    app.add_role("rowspan", row_span_role)
    app.add_role("cellspan", cell_span_role)

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }


# Entrypoint for docutils-style command line utility
def main():
    import sys
    from docutils.__main__ import main
    register_docutils_roles()
    sys.exit(main())


def register_docutils_roles():
    from docutils.parsers.rst import roles
    roles.register_canonical_role("colspan", col_span_role)
    roles.register_canonical_role("rowspan", row_span_role)
    roles.register_canonical_role("cellspan", cell_span_role)
