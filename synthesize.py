from psrc_synthpop.starter import Starter
from synthpop.synthesizer import synthesize_all, enable_logging
import os
import pandas as pd

def synth_test():
    starter = Starter(os.environ["CENSUS"], "WA", "King County")
    ind = pd.Series(["53", "33", "100", "2006"], index=["state", "county", "tract", "block group"])
    households, persons, fit = synthesize_all(starter, indexes=[ind])
    pass


def synthesize_region(num_geogs=None):
    starter = Starter(os.environ["CENSUS"], "WA")
    households, persons, fit = synthesize_all(starter, num_geogs=num_geogs)
    return (households, persons)

# for testing purposes, this will limit the number of geographies processed
# (the whole region can take a long time to run)
num_geogs = None # set it to a small integer for a test run
num_geogs = 20

# synthesize one county
#starter = Starter(os.environ["CENSUS"], "WA", "Kitsap County")
#hhs, pers, fit = synthesize_all(starter, num_geogs=num_geogs)

# synthesize the whole region
hhs, pers = synthesize_region(num_geogs=num_geogs)

# write results into csv files
del hhs['HHsize'] # redundant column
del pers['age'] # redundant column
hhs.to_csv('households.csv', index=False)
pers.to_csv('persons.csv', index=False)

