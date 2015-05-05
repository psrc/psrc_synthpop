from synthpop import categorizer as cat
from psrc_synthpop.census_helpers import Census
import pandas as pd
from numpy import logical_and

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
    def __init__(self, key, state=None, county=None, tract=None):
        self.c = c = Census(key)
        self.state = state
        self.county = county
        self.tract = tract

        #income_columns = ['B19001_0%02dE' % i for i in range(1, 18)]
        #vehicle_columns = ['B08201_0%02dE' % i for i in range(1, 7)]
        #workers_columns = ['B08202_0%02dE' % i for i in range(1, 6)]
        #families_columns = ['B11001_001E', 'B11001_002E']
        #block_group_columns = income_columns + families_columns
        #tract_columns = vehicle_columns + workers_columns
        #h_acs = c.block_group_and_tract_query(block_group_columns,
                                              #tract_columns, state, county,
                                              #merge_columns=['tract', 'county',
                                                             #'state'],
                                              #block_group_size_attr="B11001_001E",
                                              #tract_size_attr="B08201_001E",
                                              #tract=tract)
        # HS
        h_acs = pd.read_csv('data/HHmarginals.csv', dtype={
                                                  "state": "int32",
                                                  "county": "int32",
                                                  "tract": "int32",
                                                  "block group": "object"
                                              })
        p_acs = pd.read_csv('data/Personmarginals.csv', dtype={
            "state": "int32",
            "county": "int32",
            "tract": "int32",
            "block group": "object"
        })
        
        if state is not None:
            state_id, county_id = c.try_fips_lookup(state, county)
            h_ind = h_acs['state'] == int(state_id)
            p_ind = p_acs['state'] == int(state_id)
            if county is not None:
                h_ind = logical_and(h_ind, h_acs['county'] == int(county_id))
                p_ind = logical_and(p_ind, p_acs['county'] == int(county_id))
                if tract is not None:
                    h_ind = logical_and(h_ind, h_acs['tract'] == int(tract_id))
                    p_ind = logical_and(p_ind, p_acs['tract'] == int(tract_id))
            h_acs = h_acs[h_ind]
            p_acs = p_acs[p_ind]
            
        self.h_acs_cat = cat.categorize(h_acs, {
            ("HHsize", "one"):    "HH1p",
            ("HHsize", "two"):    "HH2p", 
            ("HHsize", "three"):    "HH3p",
            ("HHsize", "four"):    "HH4p",
            ("HHsize", "five"):    "HH5p",
            ("HHsize", "six"):    "HH6p",
            ("HHsize", "seven+"):    "HH7p",
            }, index_cols=['state', 'county', 'tract', 'block group'])
        
        self.p_acs_cat = cat.categorize(p_acs, {
            ("age", "category 1"):  "Age1",
            ("age", "category 2"):  "Age2",        
            }, index_cols=['state', 'county', 'tract', 'block group'])
        
        #self.h_acs_cat = cat.categorize(h_acs, {
            #("children", "yes"): "B11001_002E",
            #("children", "no"): "B11001_001E - B11001_002E",
            #("income", "lt35"): "B19001_002E + B19001_003E + B19001_004E + "
                                #"B19001_005E + B19001_006E + B19001_007E",
            #("income", "gt35-lt100"): "B19001_008E + B19001_009E + "
                                      #"B19001_010E + B19001_011E + B19001_012E"
                                      #"+ B19001_013E",
            #("income", "gt100"): "B19001_014E + B19001_015E + B19001_016E"
                                 #"+ B19001_017E",
            #("cars", "none"): "B08201_002E",
            #("cars", "one"): "B08201_003E",
            #("cars", "two or more"): "B08201_004E + B08201_005E + B08201_006E",
            #("workers", "none"): "B08202_002E",
            #("workers", "one"): "B08202_003E",
            #("workers", "two or more"): "B08202_004E + B08202_005E"
        #}, index_cols=['state', 'county', 'tract', 'block group'])
        
        #population = ['B01001_001E']
        #sex = ['B01001_002E', 'B01001_026E']
        #race = ['B02001_0%02dE' % i for i in range(1, 11)]
        #male_age_columns = ['B01001_0%02dE' % i for i in range(3, 26)]
        #female_age_columns = ['B01001_0%02dE' % i for i in range(27, 50)]
        #all_columns = population + sex + race + male_age_columns + \
            #female_age_columns
        #p_acs = c.block_group_query(all_columns, state, county, tract=tract)

        #self.p_acs_cat = cat.categorize(p_acs, {
            #("age", "19 and under"): "B01001_003E + B01001_004E + B01001_005E + "
                                     #"B01001_006E + B01001_007E + B01001_027E + "
                                     #"B01001_028E + B01001_029E + B01001_030E + "
                                     #"B01001_031E",
            #("age", "20 to 35"): "B01001_008E + B01001_009E + B01001_010E + "
                                 #"B01001_011E + B01001_012E + B01001_032E + "
                                 #"B01001_033E + B01001_034E + B01001_035E + "
                                 #"B01001_036E",
            #("age", "35 to 60"): "B01001_013E + B01001_014E + B01001_015E + "
                                 #"B01001_016E + B01001_017E + B01001_037E + "
                                 #"B01001_038E + B01001_039E + B01001_040E + "
                                 #"B01001_041E",
            #("age", "above 60"): "B01001_018E + B01001_019E + B01001_020E + "
                                 #"B01001_021E + B01001_022E + B01001_023E + "
                                 #"B01001_024E + B01001_025E + B01001_042E + "
                                 #"B01001_043E + B01001_044E + B01001_045E + "
                                 #"B01001_046E + B01001_047E + B01001_048E + "
                                 #"B01001_049E",
            #("race", "white"):   "B02001_002E",
            #("race", "black"):   "B02001_003E",
            #("race", "asian"):   "B02001_005E",
            #("race", "other"):   "B02001_004E + B02001_006E + B02001_007E + "
                                 #"B02001_008E",
            #("sex", "male"):     "B01001_002E",
            #("sex", "female"):   "B01001_026E"
        #}, index_cols=['state', 'county', 'tract', 'block group'])
        


    def get_geography_name(self):
        # this synthesis is at the block group level for most variables
        return "block group"

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

        puma = c.tract_to_puma(ind.state, ind.county, ind.tract)
        # this is cached so won't download more than once
        h_pums = self.c.download_household_pums(ind.state, puma)

        #def cars_cat(r):
            #if r.VEH == 0:
                #return "none"
            #elif r.VEH == 1:
                #return "one"
            #return "two or more"

        #def children_cat(r):
            #if r.NOC > 0:
                #return "yes"
            #return "no"

        #def income_cat(r):
            #if r.FINCP > 100000:
                #return "gt100"
            #elif r.FINCP > 35000:
                #return "gt35-lt100"
            #return "lt35"

        #def workers_cat(r):
            #if r.WIF == 3:
                #return "two or more"
            #elif r.WIF == 2:
                #return "two or more"
            #elif r.WIF == 1:
                #return "one"
            #return "none"

        def HHsize_cat(r):
            if r.HHSz == 1:
                return "one"
            if r.HHSz == 2:
                return "two"
            if r.HHSz == 3:
                return "three"
            if r.HHSz == 4:
                return "four"
            if r.HHSz == 5:
                return "five"
            if r.HHSz == 6:
                return "six"
            if r.HHSz > 6:
                return "seven+"
          
        h_pums, jd_households = cat.joint_distribution(
                h_pums,
                cat.category_combinations(self.h_acs_cat.columns),
                {"HHsize": HHsize_cat}
            )          
        #h_pums, jd_households = cat.joint_distribution(
            #h_pums,
            #cat.category_combinations(self.h_acs_cat.columns),
            #{"cars": cars_cat, "children": children_cat,
             #"income": income_cat, "workers": workers_cat}
        #)
        return h_pums, jd_households

    def get_person_joint_dist_for_geography(self, ind):
        c = self.c

        puma = c.tract_to_puma(ind.state, ind.county, ind.tract)
        # this is cached so won't download more than once
        p_pums = self.c.download_population_pums(ind.state, puma)

        #def age_cat(r):
            #if r.AGEP <= 19:
                #return "19 and under"
            #elif r.AGEP <= 35:
                #return "20 to 35"
            #elif r.AGEP <= 60:
                #return "35 to 60"
            #return "above 60"

        #def race_cat(r):
            #if r.RAC1P == 1:
                #return "white"
            #elif r.RAC1P == 2:
                #return "black"
            #elif r.RAC1P == 6:
                #return "asian"
            #return "other"

        #def sex_cat(r):
            #if r.SEX == 1:
                #return "male"
            #return "female"
# HS
        def age_cat(r):
            if r.AgeGrp == 1:
                return "category 1"
            if r.AgeGrp == 2:
                return "category 2"

        p_pums, jd_persons = cat.joint_distribution(
                p_pums,
                cat.category_combinations(self.p_acs_cat.columns),
                {"age": age_cat}
            )
        #p_pums, jd_persons = cat.joint_distribution(
            #p_pums,
            #cat.category_combinations(self.p_acs_cat.columns),
            #{"age": age_cat, "race": race_cat, "sex": sex_cat}
        #)
        return p_pums, jd_persons
