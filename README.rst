This is a python package that contains PSRC-specfic modifications to the SynthPop package developed by Synthicity.

.. However, the original synthpop repository contains some outdated URLs. Therefore an updated version is at
.. https://github.com/hanase/synthpop

**Requirements:**

1. Install the Synthicity's package: https://github.com/synthicity/synthpop
#. Obtain a key from the US Census Bureau by registering at http://api.census.gov/data/key_signup.html
#. Set the environmental variable CENSUS to that key.


Use the script synthesize.py to run the synthesizer. It uses marginals and PUMA data from the data sub-directory. When updating those data and/or creating new categories, modify the script psrc_synthpop/starter.py appropriately. 

**Note for a Windows installation:**
We experienced problems with installing the "us" package required by the "census" package which is in turn required by "synthpop". The "us" package requires a specific version of the "jellyfish" package which fails on our Windows systems. The modelsrv3 has a patched copy of the "us" package in D:/synthicity/python-us. If you need it, copy that directory to your machine and install using::

pip install -e c:/synthicity/python-us

(replace the path with wherever you copied the package). Then install the "census" package with::

pip install census


