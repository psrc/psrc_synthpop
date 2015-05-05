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

#starter = Starter(os.environ["CENSUS"], "WA", "Kitsap County")
#hhs, pers, fit = synthesize_all(starter, num_geogs=20)
hhs, pers = synthesize_region()
del hhs['HHsize']
del pers['age']
hhs.to_csv('households.csv', index=False)
pers.to_csv('persons.csv', index=False)

