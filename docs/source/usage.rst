Usage
=====

Python API
----------

.. code-block:: python

   from adm1dae import simulate

Command line
------------

.. code-block:: bash

   python -m adm1dae.simulate --influ path/to/AD_constinfluent_bsm2.npz --t_end 10 --dt 0.1 --out adm1_dae_test.npz

Driver summary
--------------

The packaged driver performs fixed major-step integration with discrete updates of the pH and H2 algebraic solvers around the main ADM1 DAE reactor kernel.
