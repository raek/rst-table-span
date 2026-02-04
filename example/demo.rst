Demo
****

To build this, run ``rst-table-span-docutils demo.rst --output demo.html`` or ``just`` in this directory.


Grid Table
==========

Code::

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

Output:

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


List Table
==========

Code::

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

Output:

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


CSV Table
=========

Code::

   .. csv-table::
      :header-rows: 1

      "Header row, column 1 (header rows optional)", Header 2, Header 3, Header 4
      "body row 1, column 1", column 2, column 3, column 4
      body row 2, :colspan:`3` Cells may span columns.
      body row 3, :rowspan:`2` Cells may span rows., ":cellspan:`2x2` Corner"
      body row 4

Output:

.. csv-table::
   :header-rows: 1

   "Header row, column 1 (header rows optional)", Header 2, Header 3, Header 4
   "body row 1, column 1", column 2, column 3, column 4
   body row 2, :colspan:`3` Cells may span columns.
   body row 3, :rowspan:`2` Cells may span rows., ":cellspan:`2x2` Corner"
   body row 4
