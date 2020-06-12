This is a tiny importable Python wrapper for the `Environment Modules
<https://modules.readthedocs.io/en/latest/>`_ system - the ``module load``
command often used in the shell on HPC systems.

Installation::

    pip install envmodules

Usage::

    import envmodules
    envmodules.load('gcc/6.1.1')

Loading modules like this mostly affects external programs which you
run in subprocesses.
Most modules won't have much effect on Python code in the same process.
