This is a python package that contains PSRC-specfic modifications to the SynthPop package developed by Synthicity.

.. However, the original synthpop repository contains some outdated URLs. Therefore an updated version is at
.. https://github.com/hanase/synthpop

**Requirements:**

1. Install the Synthicity's package: https://github.com/synthicity/synthpop
#. Obtain a key from the US Census Bureau by registering at http://api.census.gov/data/key_signup.html
#. Set the environmental variable CENSUS to that key.


Use the script synthesize.py to run the synthesizer. It uses marginals and PUMA data from the data sub-directory. When updating those data and/or creating new categories, modify the script psrc_synthpop/starter.py appropriately. 
