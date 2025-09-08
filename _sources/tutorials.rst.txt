Tutorials
=========

This section walks you through the basics of using JsonGrapher.

Load and Visualize JSON
-----------------------

.. code-block:: python

   from jsongrapher import JsonGrapher

   data = {
       "name": "Alice",
       "friends": ["Bob", "Charlie"]
   }

   grapher = JsonGrapher(data)
   grapher.visualize()

Saving a Graph
--------------

.. code-block:: python

   grapher.to_png("graph.png")
