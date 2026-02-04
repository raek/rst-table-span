**************
rst-table-span
**************

reStructuredText provides four syntaxes for tables:

* Grid tables
* Simple tables
* List tables
* CSV tables

However, only grid and simple tables support cells spanning multiple columns, and only
grid tables support cells spanning multiple rows.

The ``rst-table-span`` package adds the ``:colspan:`C```, ``:rowspan:`R```, and
``:cellspan:`CxR``` roles which add support for column and row span *to all
existing RST table types*.

This project was inspired by the ``flat-table`` directive from the LinuxDoc_ project.

.. _LinuxDoc: https://return42.github.io/linuxdoc/linuxdoc-howto/table-markup.html#flat-table


Example
=======

To produce a table like this:

.. table::

   +------------------------+------------+----------+----------+
   | Header row, column 1   | Header 2   | Header 3 | Header 4 |
   | (header rows optional) |            |          |          |
   +========================+============+==========+==========+
   | body row 1, column 1   | column 2   | column 3 | column 4 |
   +------------------------+------------+----------+----------+
   | body row 2             | Cells may span columns.          |
   +------------------------+------------+---------------------+
   | body row 3             | Cells may  | Corner              |
   +------------------------+ span rows. |                     |
   | body row 4             |            |                     |
   +------------------------+------------+---------------------+

You would normally need to write this::

   +------------------------+------------+----------+----------+
   | Header row, column 1   | Header 2   | Header 3 | Header 4 |
   | (header rows optional) |            |          |          |
   +========================+============+==========+==========+
   | body row 1, column 1   | column 2   | column 3 | column 4 |
   +------------------------+------------+----------+----------+
   | body row 2             | Cells may span columns.          |
   +------------------------+------------+---------------------+
   | body row 3             | Cells may  | Corner              |
   +------------------------+ span rows. |                     |
   | body row 4             |            |                     |
   +------------------------+------------+---------------------+

But with ``rst-table-span`` you can instead write it using a ``csv-table``::

   .. csv-table::
      :header-rows: 1

      "Header row, column 1 (header rows optional)", Header 2, Header 3, Header 4
      "body row 1, column 1", column 2, column 3, column 4
      body row 2, :colspan:`3` Cells may span columns.
      body row 3, :rowspan:`2` Cells may span rows., :cellspan:`2x2` Corner
      body row 4

Or a ``list-table``::

   .. list-table::
      :header-rows: 1

      * - Header row, column 1 (header rows optional)
        - Header 2
        - Header 3
        - Header 4
      * - body row 1, column 1
        - column 2
        - column 3
        - column 4
      * - body row 2
        - :colspan:`3` Cells may span columns.
        -
        -
      * - body row 3
        - :rowspan:`2` Cells may span rows.
        - :cellspan:`2x2` Corner
        -
      * - body row 4
        -
        -
        -


Installation and Usage
======================

Install the package using pip::

   pip install rst-table-span

or add the ``rst-table-span`` package to your project or environment dependency
list (eg. ``pyproject.toml``, ``requirements.txt``, or similar).


Sphinx
------

Also add the ``rst_table_span`` module to your list of extensions in your
``conf.py`` settings::

   extensions = [
       "rst_table_span",
   ]


Docutils
--------

.. _Publisher API: https://docutils.sourceforge.io/docs/api/publisher.html

Docutils doesn't provide a declarative extension mechanism, as far as I know. If
you invoke docutils programatically using its `Publisher API`_, then a global
function is provided to register the roles. Call it before setting up the publisher::

   import sys
   import docutils.__main__
   import rst_table_span

   rst_table_span.register_docutils_roles()
   sys.exit(docutils.__main__.main())

For convenience, this package installs the above script as the
``rst-table-span-docutils`` executable. It behaves the same way as the standard
``docutils`` executable. It can then be used used like this::

   rst-table-span-docutils demo.rst --output demo.html


License
=======

This library is released under the **MIT license** (see the ``LICENSE`` file in
the source code).
