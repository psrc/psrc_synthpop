from synthpop import categorizer as cat
from psrc_synthpop.census_helpers import Census
from psrc_synthpop.weight_acs_variables import *
import pandas as pd
import numpy as np
import pickle
import os

# TODO DOCSTRINGS!!
class Starter:
    """
    This is a recipe for getting the marginals and  distributions to use
    to pass to the synthesizer using simple categorjointies - population, age,
    race, and sex for people, and children, income, cars, and workers for
    households.  This module is responsible for

    Parameters
    ----------
    c : object
        census_helpers.Census object
    state : string
        FIPS code the state
    county : string
        FIPS code for the county
    tract : string, optional
        FIPS code for a specific track or None for all tracts in the county

    Returns
    -------
    household_marginals : DataFrame
        Marginals per block group for the household data (from ACS)
    person_marginals : DataFrame
        Marginals per block group for the person data (from ACS)
    household_jointdist : DataFrame
        joint distributions for the households (from PUMS), one joint
        distribution for each PUMA (one row per PUMA)
    person_jointdist : DataFrame
        joint distributions for the persons (from PUMS), one joint
        distribution for each PUMA (one row per PUMA)
    tract_to_puma_map : dictionary
        keys are tract ids and pumas are puma ids
    """
    def __init__(self, key, control_totals, acs_ouput_dir, hh_size_2010, state, county, tract=None):
        self.c = c = Census(key)
        self.state = state
        self.county = county
        self.tract = tract
        self.income_adjustment_factors = {1094136 : (1.007624 * 1.08585701), 1071861 : (1.018237 * 1.05266344), 1041654 : (1.010207 * 1.03112956), 
                                          1024037 : (1.007549 * 1.01636470), 1008425 : (1.008425 * 1.00000000)}

        income_columns = ['B19001_0%02dE' % i for i in range(1, 18)]
        #hh_size_columns = ['B11016_0%02dE' % i for i in range(1, 17)]
        vehicle_columns = ['B08201_0%02dE' % i for i in range(1, 7)]
        workers_columns = ['B08202_0%02dE' % i for i in range(1, 6)]
        families_columns = ['B11001_001E', 'B11001_002E', 'B11001_007E']
        block_group_columns = income_columns + families_columns 
        tract_columns = vehicle_columns + workers_columns
        h_acs = c.block_group_and_tract_query(
            block_group_columns, tract_columns, state, county,
            merge_columns=['tract', 'county', 'state'],
            block_group_size_attr="B11001_001E",
            tract_size_attr="B08201_001E",
            tract=tract)
       
        h_acs = h_acs.merge(control_totals, how ='left', on = ['state', 'county', 'tract', 'block group'])
        h_acs = h_acs.merge(hh_size_2010, how ='left', on = ['state', 'county', 'tract', 'block group'])
        h_acs_cat = cat.categorize(h_acs, {
            ("totals", 'total households'): ('households'),
            ("family", "is_family"): "B11001_002E",
            ("family", "not_family"): "B11001_007E",
            ("workers", "none"): "B08202_002E",
            ("workers", "one"): "B08202_003E",
            ("workers", "two or more"): "B08202_004E + B08202_005E",
            ("income", "lt15"): "B19001_002E + B19001_003E",
            ("income", "gt15-lt30"): "B19001_004E + B19001_005E + B19001_006E",
            ("income", "gt30-lt60"): "B19001_007E + B19001_008E + B19001_009E + B19001_010E + B19001_011E",
            ("income", "gt60-lt100"): "B19001_012E + B19001_013E",
            ("income", "gt100"): "B19001_014E + B19001_015E + B19001_016E + B19001_017E",
            ("cars", "no_car"): "B08201_002E",
            ("cars", "one_car"): "B08201_003E",
            ("cars", "two_or_more_cars"): "B08201_004E + B08201_005E + B08201_006E",
            ("hh_size", "one"): "HH1p",
            ("hh_size", "two"): "HH2p",
            ("hh_size", "three"): "HH3p",
            ("hh_size", "four"): "HH4p",
            ("hh_size", "five"): "HH5p",
            ("hh_size", "six"): "HH6p",
            ("hh_size", "seven or more"): "HH7p",
        }, index_cols=['state', 'county', 'tract', 'block group'])
        
        self.h_acs_cat = weight_samples(h_acs_cat, ['workers', 'family', 'income', 'cars', 'hh_size'], 'total households')
        
        # Save the ACS data to compare to results:
        print('''
The current working directory is
{0}
'''.format(os.getcwd()))
        
        f = open(os.getcwd() + '/' +  acs_ouput_dir + 'h_acs_cat_' + str(county) + '.pickle' , 'wb')
        pickle.dump(self.h_acs_cat, f)
        f.close()

        population = ['B01001_001E']
        sex = ['B01001_001E','B01001_002E', 'B01001_026E']
        race = ['B02001_0%02dE' % i for i in range(1, 11)]
        male_age_columns = ['B01001_0%02dE' % i for i in range(3, 26)]
        female_age_columns = ['B01001_0%02dE' % i for i in range(27, 50)]
        work_status_columns = ['B17004_0%02dE' % i for i in range(1, 20)]
        school_enrollment_columns = ['B14001_001E', 'B14001_002E', 'B14001_010E']
        group_quarters = ['B26001_001E']
        block_group_columns2 = population + sex + race + male_age_columns + \
            female_age_columns 
        tract_columns2 = work_status_columns + group_quarters + school_enrollment_columns + ['B01003_001E']
       
        p_acs = c.block_group_and_tract_query(
            block_group_columns2, tract_columns2, state, county,
            merge_columns=['tract', 'county', 'state'],
            block_group_size_attr='B01001_001E',
            tract_size_attr='B01003_001E',
            tract=tract)
        
        #Merge the control totals dataframe to p_acs:
        p_acs = p_acs.merge(control_totals, how ='left', on = ['state', 'county', 'tract', 'block group'])
        
        p_acs_cat = cat.categorize(p_acs, {
            ("totals", 'total pop'): ('pop_no_gq'),
            ("school_enrollment", "yes_school") : ("B14001_002E"),
            ("school_enrollment", "no_school") : ("B01001_001E - B14001_002E"),
            ("age", "19 and under"): (
                "B01001_003E + B01001_004E + B01001_005E + "
                "B01001_006E + B01001_007E + B01001_027E + "
                "B01001_028E + B01001_029E + B01001_030E + "
                "B01001_031E"),
            ("age", "20 to 35"): "B01001_008E + B01001_009E + B01001_010E + "
                                 "B01001_011E + B01001_012E + B01001_032E + "
                                 "B01001_033E + B01001_034E + B01001_035E + "
                                 "B01001_036E",
            ("age", "35 to 60"): "B01001_013E + B01001_014E + B01001_015E + "
                                 "B01001_016E + B01001_017E + B01001_037E + "
                                 "B01001_038E + B01001_039E + B01001_040E + "
                                 "B01001_041E",
            ("age", "above 60"): "B01001_018E + B01001_019E + B01001_020E + "
                                 "B01001_021E + B01001_022E + B01001_023E + "
                                 "B01001_024E + B01001_025E + B01001_042E + "
                                 "B01001_043E + B01001_044E + B01001_045E + "
                                 "B01001_046E + B01001_047E + B01001_048E + "
                                 "B01001_049E",
            ("sex", "male"):     "B01001_002E",
            ("sex", "female"):   "B01001_026E"
        }, index_cols=['state', 'county', 'tract', 'block group'])
        
        self.p_acs_cat = weight_samples(p_acs_cat, ['school_enrollment', 'age', 'sex'], 'total pop')
        
        # Save the ACS data to compare to results:
        f = open(os.getcwd() + '/' + acs_ouput_dir + 'p_acs_cat_' + str(county) + '.pickle' , 'wb')
        pickle.dump(self.p_acs_cat, f)
        f.close()

    def get_geography_name(self):
        # this synthesis is at the block group level for most variables
        return "block_group"

    def get_num_geographies(self):
        return len(self.p_acs_cat)

    def get_available_geography_ids(self):
        # return the ids of the geographies, in this case a state, county,
        # tract, block_group id tuple
        for tup in self.p_acs_cat.index:
            yield pd.Series(tup, index=self.p_acs_cat.index.names)

    def get_household_marginal_for_geography(self, ind):
        return self.h_acs_cat.loc[tuple(ind.values)]

    def get_person_marginal_for_geography(self, ind):
        return self.p_acs_cat.loc[tuple(ind.values)]

    def get_household_joint_dist_for_geography(self, ind):
        c = self.c

        puma10, puma00 = c.tract_to_puma(ind.state, ind.county, ind.tract)
        # this is cached so won't download more than once
        if type(puma00) == str:
            h_pums = self.c.download_household_pums(ind.state, puma10, puma00)
        elif np.isnan(puma00):  # only puma10 available
            h_pums = self.c.download_household_pums(ind.state, puma10, None)

        def cars_cat(r):
            if r.VEH == 0:
                return "no_car"
            elif r.VEH == 1:
                return "one_car"
            return "two_or_more_cars"

        def children_cat(r):
            if r.NOC > 0:
                return "have_children"
            return "no_children"

        def family_cat(r):
            if r.HHT > 0 and r.HHT<=3:
                return "is_family"
            elif r.HHT > 3:
                return "not_family"

        def income_cat(r):
            adj_factor = self.income_adjustment_factors[r.ADJINC]
            income = r.HINCP * adj_factor
            if income > 100000:
                return "gt100"
            elif income > 60000:
                return "gt60-lt100"
            elif income > 30000:
                return "gt30-lt60"
            elif income > 15000:
                return "gt15-lt30"
            return "lt15"

        def workers_cat(r):
            if r.num_workers >= 2:
                return "two or more"
            elif r.num_workers == 1:
                return "one"
            return "none"

        def hh_size_cat(r):
            if r.NP == 1:
                return "one"
            elif r.NP == 2:
                return "two"
            elif r.NP == 3:
                return "three"
            elif r.NP == 4:
                return "four"
            elif r.NP == 5:
                return "five"
            elif r.NP == 6:
                return "six"
            return "seven or more"

        h_pums, jd_households = cat.joint_distribution(
            h_pums,
            cat.category_combinations(self.h_acs_cat.columns),
            {"workers" : workers_cat, "cars": cars_cat, "income": income_cat, "hh_size": hh_size_cat, "family" : family_cat, "children" : children_cat}
        )
        return h_pums, jd_households

    def get_person_joint_dist_for_geography(self, ind):
        c = self.c

        puma10, puma00 = c.tract_to_puma(ind.state, ind.county, ind.tract)
        # this is cached so won't download more than once
        if type(puma00) == str:
            p_pums = self.c.download_population_pums(ind.state, puma10, puma00)
        elif np.isnan(puma00):  # only puma10 available
            p_pums = self.c.download_population_pums(ind.state, puma10, None)

        def age_cat(r):
            if r.AGEP <= 19:
                return "19 and under"
            elif r.AGEP <= 35:
                return "20 to 35"
            elif r.AGEP <= 60:
                return "35 to 60"
            return "above 60"
        
        def school_enrollment_cat(r):
            if r.SCH > 1:
                return "yes_school"
            else:
                return "no_school"

        def race_cat(r):
            if r.RAC1P == 1:
                return "white"
            elif r.RAC1P == 2:
                return "black"
            elif r.RAC1P == 6:
                return "asian"
            return "other"

        def sex_cat(r):
            if r.SEX == 1:
                return "male"
            return "female"

        def work_status_cat(r):
            if r.WKHP >=35 and r.WKW < 3:
                return "full-time"
            elif r.WKHP != r.WKHP:
                return "non-worker"
            elif r.WKW == 6:
                "non-worker"
            return "part-time"

        p_pums, jd_persons = cat.joint_distribution(
            p_pums,
            cat.category_combinations(self.p_acs_cat.columns),
            {"school_enrollment" : school_enrollment_cat, "age" : age_cat, "sex": sex_cat,}
        )
        return p_pums, jd_persons
