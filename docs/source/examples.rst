Examples
========

Basic run
---------

.. code-block:: bash

   python -m adm1dae.simulate --influ src/adm1dae/data/AD_constinfluent_bsm2.npz --t_end 10 --dt 0.1 --out adm1_dae_test.npz

The influent NPZ can contain either:

- ``(n, 94)`` = time + 93 influent columns
- ``(n, 93)`` = 93 influent columns aligned to the simulation grid
