Troubleshooting
===============

Common Issues
-------------

**Problem:** Graph window doesn’t show up.  
**Solution:** Ensure matplotlib backend is set correctly, e.g.:

.. code-block:: python

   import matplotlib
   matplotlib.use("TkAgg")

---

**Problem:** Installation fails.  
**Solution:** Upgrade pip:

.. code-block:: bash

   pip install --upgrade pip
