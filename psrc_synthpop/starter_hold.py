from synthpop import categorizer as cat
from psrc_synthpop.census_helpers import Census
import pandas as pd
import numpy as np


# TODO DOCSTRINGS!!
class Starter:
    """
    This is a recipe for getting the marginals and joint distributions to use
    to pass to the synthesizer using simple categories - population, age,
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
    def __init__(self, key, state, county, tract=None):
        self.c = c = Census(key)
        self.state = state
        self.county = county
        self.tract = tract

        income_columns = ['B19001_0%02dE' % i for i in range(1, 18)]
        vehicle_columns = ['B08201_0%02dE' % i for i in range(1, 7)]
        workers_columns = ['B08202_0%02dE' % i for i in range(1, 6)]
        families_columns = ['B11001_001E', 'B11001_002E']
        hh_size_columns = ['B25009_0%02dE' % i for i in range(1, 18)]
        block_group_columns = income_columns + families_columns
        tract_columns = vehicle_columns + workers_columns + hh_size_columns
        h_acs = c.block_group_and_tract_query(
            block_group_columns, tract_columns, state, county,
            merge_columns=['tract', 'county', 'state'],
            block_group_size_attr="B11001_001E",
            tract_size_attr="B08201_001E",
            tract=tract)
        h_acs.to_csv('d:/acs_households.csv')

        self.h_acs_cat = cat.categorize(h_acs, {
            ("children", "yes"): "B11001_002E",
            ("children", "no"): "B11001_001E - B11001_002E",
            ("income", "lt15"): "B19001_002E + B19001_003E",
            ("income", "gt15-lt30"): "B19001_004E + B19001_005E + B19001_006E",
            ("income", "gt30-lt60"): "B19001_007E + B19001_008E + B19001_009E + B19001_010E + B19001_011E",
            ("income", "gt60-lt100"): "B19001_012E + B19001_013E",
            ("income", "gt100"): "B19001_014E + B19001_015E + B19001_016E + B19001_017E",
            ("cars", "none"): "B08201_002E",
            ("cars", "one"): "B08201_003E",
            ("cars", "two or more"): "B08201_004E + B08201_005E + B08201_006E",
            ("workers", "none"): "B08202_002E",
            ("workers", "one"): "B08202_003E",
            ("workers", "two or more"): "B08202_004E + B08202_005E",
            ("hh_size", "one"): "B25009_003E + B25009_011E",
            ("hh_size", "two"): "B25009_004E + B25009_012E",
            ("hh_size", "three"): "B25009_005E + B25009_013E",
            ("hh_size", "four"): "B25009_006E + B25009_014E",
            ("hh_size", "five"): "B25009_007E + B25009_015E",
            ("hh_size", "six"): "B25009_008E + B25009_016E",
            ("hh_size", "seven or more"): "B25009_009E + B25009_017E"
        }, index_cols=['state', 'county', 'tract', 'block group'])

        population = ['B01001_001E']
        sex = ['B01001_002E', 'B01001_026E']
        race = ['B02001_0%02dE' % i for i in range(1, 11)]
        male_age_columns = ['B01001_0%02dE' % i for i in range(3, 26)]
        female_age_columns = ['B01001_0%02dE' % i for i in range(27, 50)]
        all_columns = population + sex + race + male_age_columns + \
            female_age_columns
        p_acs = c.block_group_query(all_columns, state, county, tract=tract)
        p_acs.to_csv('d:/acs_persons.csv')

        self.p_acs_cat = cat.categorize(p_acs, {
            ("age", "Under 5"): "B01001_003E + B01001_027E",
            ("age", "5 to 9"): "B01001_004E + B01001_028E",
            ("age", "10 to 14"): "B01001_005E + B01001_029E",
            ("age", "15 to 17"): "B01001_006E + B01001_030E",
            ("age", "18 to 24"): "B01001_007E + B01001_008E + B01001_009E + B01001_010E +  B01001_031E + B01001_032E + B01001_033E + B01001_034E",
            ("age", "25 to 34"): "B01001_011E + B01001_012E + B01001_035E + B01001_036E",
            ("age", "35 to 49"): "B01001_013E + B01001_014E + B01001_015E + B01001_037E + B01001_038E + B01001_039E",
            ("age", "50 to 64"): "B01001_016E + B01001_017E + B01001_018E + B01001_019E + B01001_040E + B01001_041E + B01001_042E + B01001_043E",
            ("age", "65 to 79"): "B01001_020E + B01001_021E + B01001_022E + B01001_023E + B01001_044E + B01001_045E + B01001_046E + B01001_047E",
            ("age", "above 80"): "B01001_024E + B01001_025E + B01001_048E + B01001_049E",
            #("race", "white"):   "B02001_002E",
            #("race", "black"):   "B02001_003E",
            #("race", "asian"):   "B02001_005E",
            #("race", "other"):   "B02001_004E + B02001_006E + B02001_007E + "
            #                     "B02001_008E",
            ("sex", "male"):     "B01001_002E",
            ("sex", "female"):   "B01001_026E"
        }, index_cols=['state', 'county', 'tract', 'block group'])

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
                return "none"
            elif r.VEH == 1:
                return "one"
            return "two or more"

        def children_cat(r):
            if r.NOC > 0:
                return "yes"
            return "no"

        def income_cat(r):
            if r.HINCP > 100000:
                return "gt100"
            elif r.HINCP > 60000:
                return "gt60-lt100"
            elif r.HINCP > 30000:
                return "gt30-lt60"
            elif r.HINCP > 15000:
                return "gt15-lt30"
            return "lt15"

        def workers_cat(r):
            if r.WIF == 3:
                return "two or more"
            elif r.WIF == 2:
                return "two or more"
            elif r.WIF == 1:
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
            {"cars": cars_cat, "children": children_cat,
             "income": income_cat, "workers": workers_cat, "hh_size": hh_size_cat}
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
            if r.AGEP < 5:
                return "under 5"
            elif r.AGEP < 10:
                return "5 to 9"
            elif r.AGEP < 15:
                return "10 to 14"
            elif r.AGEP < 18:
                return "15 to 17"
            elif r.AGEP < 25:
                return "18 to 24"
            elif r.AGEP < 35:
                return "25 to 34"
            elif r.AGEP < 50:
                return "35 to 49"
            elif r.AGEP < 65:
                return "50 to 64"
            elif r.AGEP < 80:
                return "65 to 79"
            return "above 80"

        #def race_cat(r):
        #    if r.RAC1P == 1:
        #        return "white"
        #    elif r.RAC1P == 2:
        #        return "black"
        #    elif r.RAC1P == 6:
        #        return "asian"
        #    return "other"

        def sex_cat(r):
            if r.SEX == 1:
                return "male"
            return "female"

        p_pums, jd_persons = cat.joint_distribution(
            p_pums,
            cat.category_combinations(self.p_acs_cat.columns),
            {"age": age_cat, "sex": sex_cat}
        )
        return p_pums, jd_persons