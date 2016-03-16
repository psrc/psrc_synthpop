from psrc_synthpop.starter_ofm_weighted import Starter
from synthpop.synthesizer import synthesize_all
import pandas as pd
import os
import sys

input_dir = 'data/'
output_dir = 'results/'

control_totals = pd.read_csv(input_dir + 'OFM_Data2014.csv', dtype={'county': 'str', 'tract' : 'str', 'state' : 'str', 'block_group' : 'str'})
control_totals['block group'] = control_totals['block_group']
control_totals.drop('block_group', axis=1, inplace = True)

hh_size = pd.read_csv(input_dir + 'HH_Size_2010.csv', dtype={'county': 'str', 'tract' : 'str', 'state' : 'str', 'block_group' : 'str'})
hh_size['block group'] = hh_size['block_group']
hh_size.drop('block_group', axis=1, inplace = True)


state_abbr = 53
county_name_list = [35, 53, 61, 33]

person_results_dict = {}
household_results_dict = {}
for county_name in county_name_list:
    starter = Starter(os.environ["CENSUS"], control_totals, output_dir, hh_size, state_abbr, county_name)

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
    

people_df = pd.concat(list(person_results_dict.itervalues()))
people = people_df[['serialno', 'age', 'school_enrollment', 'hh_id', 'sex', 'state', 'county', 'tract', 'block group']]
households_df = pd.concat(list(household_results_dict.itervalues()))
people_df.to_csv(output_dir + 'people_region_all_vars.csv')
people.to_csv(output_dir + 'people_region.csv')
households_df.to_csv(output_dir + 'households_region.csv')