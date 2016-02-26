
# coding: utf-8

from psrc_synthpop.starter_weight_new import Starter
from synthpop.synthesizer import synthesize_all
import pandas as pd
import os
import sys

#state_abbr = sys.argv[1]
#county_name = sys.argv[2]

control_totals = pd.read_csv(r'D:\Stefan\synthpop_2014\psrc_synthpop\data\OFM_Data2014.csv', dtype={'county': 'str', 'tract' : 'str', 'state' : 'str', 'block_group' : 'str'})
control_totals['block group'] = control_totals['block_group']
control_totals.drop('block_group', axis=1, inplace = True)


state_abbr = 53
county_name_list = [35, 53, 61, 33]
#starter = Starter(os.environ["CENSUS"],control_totals, state_abbr, county_name)

person_results_dict = {}
household_results_dict = {}
for county_name in county_name_list:
    starter = Starter(os.environ["CENSUS"], control_totals, state_abbr, county_name)

    if len(sys.argv) > 3:
        state, county, tract, block_group = sys.argv[3:]

        indexes = [pd.Series(
            [state, county, tract, block_group],
            index=["state", "county", "tract", "block group"])]
    else:
        indexes = None

    households, people, fit_quality = synthesize_all(starter, indexes=indexes)
    person_results_dict[county_name] = people
    household_results_dict[county_name] = households
    
    for geo, qual in fit_quality.items():
        print 'Geography: {} {} {} {}'.format(
            geo.state, geo.county, geo.tract, geo.block_group)
        # print '    household chisq: {}'.format(qual.household_chisq)
        # print '    household p:     {}'.format(qual.household_p)
        print '    people chisq:    {}'.format(qual.people_chisq)
        print '    people p:        {}'.format(qual.people_p)
test = list(person_results_dict.values.t)
people_df = pd.concat(list(person_results_dict.itervalues()))
households_df = pd.concat(list(household_results_dict.itervalues()))